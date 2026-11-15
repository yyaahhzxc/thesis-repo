#!/usr/bin/env python3
"""Deterministic (zero-LLM-token) pre-audit of the thesis manuscript.

Scans every ACTIVE .tex file in CS_Undergraduate_Thesis_Template/ (files pulled
in by main.tex through \\include/\\input) plus references.bib and main.log, and
reports candidate defects against the four .agents/rules/paper-*.md rules.

Everything reported is a CANDIDATE. Regexes find; agents/humans decide.
Line numbers always refer to the ORIGINAL .tex source.

Usage
-----
    python scripts/audit/pre_audit_paper.py                       # full audit -> output/paper_pre_audit.json (+ .md)
    python scripts/audit/pre_audit_paper.py --out output/x.json   # custom output path
    python scripts/audit/pre_audit_paper.py --files chapters/introduction.tex chapters/abstract.tex
    python scripts/audit/pre_audit_paper.py --slice chapters/methodology.tex 1 780   # print ledger for a line range
    python scripts/audit/pre_audit_paper.py --compare output/before.json output/after.json
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEX_DIR = ROOT / "CS_Undergraduate_Thesis_Template"
DECLAUDE = ROOT / ".agents" / "skills" / "declauding" / "scripts" / "declaude_lint.py"
REFS_DIR = ROOT / "docs" / "references"

CANON = {"enactments": "27,248", "national": "25,432", "local": "1,816", "provisions": "177,423"}

# Prose-linted files: manuscript chapters only. Appendices are artifact archives
# (structural checks only); verbatim legal text must never be rewritten anyway.
PROSE_PREFIXES = ("chapters/",)

STALE_COUNTS = {
    "27,096": "stale enactment count (canonical 27,248)",
    "27,357": "stale enactment count (canonical 27,248)",
    "1,925": "stale local ordinance count (canonical 1,816)",
    "1,660": "approximate/stale local archive count (canonical 1,816) - review context",
    "176,421": "serialized demo index size, not canonical corpus size (177,423) - review context",
    "176,423": "stale provision count (canonical 177,423)",
    "178,494": "stale provision count (canonical 177,423)",
    "164,621": "demo index offset - review context",
}

BANNED_WORDS = [
    "tapestry", "delve", "underscore", "underscores", "underscored", "testament to", "beacon",
    "delicate dance", "dynamic interplay", "cornerstone", "multifaceted", "paramount", "pivotal",
    "overarching", "nuanced", "mastery of", "vibrant", "intricate web", "holistic symphony",
    "revolutionary", "groundbreaking", "remarkable", "astounding", "paradigm shift",
    "leverage", "leverages", "leveraged", "leveraging", "utilize", "utilizes", "utilized", "utilizing",
    "foster", "fosters", "fostered", "fostering", "crucially", "crucial",
    "protocol", "protocols", "bottleneck", "bottlenecks",
    "super-hub", "central anchor hub", "core backbone", "reasoning ceiling", "gold-standard pillar",
]

STAGED_PHRASES = [
    r"here is where it gets interesting", r"what the researchers did not expect",
    r"it turns out that", r"the real problem was not", r"the real problem is not",
    r"it is worth noting that", r"interestingly,", r"importantly,", r"in addition,",
]

NAME_RE = re.compile(r"\b(Yahyah|Yah|Ralph|Dulce|Odin|Ogs|Tacadao|Valmores|Paterno|Alfoja|Pelobello|Lumapas|Corpuz|Lamsin|Nuril)\b")
ABLAZO_RE = re.compile(r"Ablazo(?!~?\\cite|\s*\\cite|\s*\(\d{4}\)|\s*et\s+al|\s+\d{4})")
FOURTH_WALL_RE = re.compile(r"\b(milestone|syllabus|rubric|the professor|course requirement|Ma'am|Sir Ogs|per the instructor)\b", re.I)

MODEL_TT_RE = re.compile(r"\\texttt\{[^}]*(DeBERTa|ModernBERT|MiniLM|BGE|mpnet|PoL-BERT|RoBERTa|BERT)[^}]*\}")

# --------------------------------------------------------------------------- utils

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def blank_keep_lines(m: re.Match) -> str:
    return "\n" * m.group(0).count("\n")


def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*$", "", text, flags=re.M)


def active_files() -> list[str]:
    """Relative paths (to TEX_DIR) of files actually compiled into main.pdf."""
    main = strip_comments(read(TEX_DIR / "main.tex"))
    rels = ["main.tex"]
    for m in re.finditer(r"\\(?:include|input)\{([^}]+)\}", main):
        rel = m.group(1)
        if not rel.endswith(".tex"):
            rel += ".tex"
        if (TEX_DIR / rel).exists():
            rels.append(rel)
    return rels


FLOAT_ENVS = ["table", "table\\*", "figure", "figure\\*", "longtable", "tabular\\*", "tabularx", "tabular",
              "xltabular", "lstlisting", "verbatim", "equation", "equation\\*", "align", "align\\*", "gather",
              "gather\\*", "multline", "multline\\*", "algorithm", "algorithm2e", "eqnarray", "tikzpicture"]


def to_prose(src: str) -> str:
    """LaTeX -> plain prose, preserving the original line count."""
    t = strip_comments(src)
    for env in FLOAT_ENVS:
        t = re.sub(r"\\begin\{%s\}.*?\\end\{%s\}" % (env, env), blank_keep_lines, t, flags=re.S)
    t = re.sub(r"\\\[.*?\\\]", blank_keep_lines, t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$", blank_keep_lines, t, flags=re.S)
    t = re.sub(r"(?<!\\)\$[^$]{0,400}?(?<!\\)\$", lambda m: "X" + "\n" * m.group(0).count("\n"), t, flags=re.S)
    # headings and captions become paragraph separators
    t = re.sub(r"\\(?:chapter|section|subsection|subsubsection|caption)\*?(?:\[[^\]]*\])?\{(?:[^{}]|\{[^{}]*\})*\}",
               blank_keep_lines, t, flags=re.S)
    t = re.sub(r"\\(?:cite|citeauthor|citep|citet|nocite)[a-z]*\*?(?:\[[^\]]*\])*\{[^}]*\}", "", t)
    t = re.sub(r"\\(?:label|ref|eqref|autoref|pageref|index|eqcaption|phantomsection|vspace\*?|hspace\*?|addcontentsline|"
               r"setlength|renewcommand|newcommand|chaptermark|thispagestyle|pagestyle)\{[^}]*\}(?:\{[^}]*\})*", "", t)
    for _ in range(4):
        t = re.sub(r"\\(?:textit|textbf|emph|texttt|textsc|underline|text|mathrm|mathbf|textrm|url|href)\{([^{}]*)\}", r"\1", t)
    t = t.replace("---", "\u2014").replace("--", "\u2013")
    t = t.replace("``", '"').replace("''", '"').replace("~", " ")
    t = re.sub(r"\\begin\{[^}]*\}|\\end\{[^}]*\}", "", t)
    t = re.sub(r"\\item(?:\[[^\]]*\])?", "", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", "", t)
    t = t.replace("{", "").replace("}", "").replace("\\\\", " ")
    return t


ABBREV = [("No.", "No"), ("Nos.", "Nos"), ("et al.", "et al"), ("vs.", "vs"), ("e.g.", "eg"), ("i.e.", "ie"),
          ("Fig.", "Fig"), ("Sec.", "Sec"), ("Inc.", "Inc"), ("Ord.", "Ord"), ("Art.", "Art"), ("Sec ", "Sec "),
          ("R.A.", "RA"), ("St.", "St"), ("Mr.", "Mr"), ("Ms.", "Ms"), ("Dr.", "Dr"), ("cf.", "cf"), ("etc.", "etc"),
          ("Ph.D.", "PhD"), ("G.R.", "GR"), ("Co.", "Co"), ("Jr.", "Jr"), ("Eq.", "Eq")]


def split_sentences(par: str) -> list[str]:
    p = par
    for a, b in ABBREV:
        p = p.replace(a, b)
    p = re.sub(r"(\d)\.(\d)", r"\1_\2", p)
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"(\[])", p.strip()) if s.strip()]


def paragraphs(prose: str):
    """Yield (start_line, text) for blank-line separated prose blocks."""
    lines = prose.split("\n")
    buf, start = [], None
    for i, ln in enumerate(lines, 1):
        if ln.strip():
            if start is None:
                start = i
            buf.append(ln.strip())
        else:
            if buf:
                yield start, " ".join(buf)
            buf, start = [], None
    if buf:
        yield start, " ".join(buf)


def load_declaude():
    if not DECLAUDE.exists():
        return None
    spec = importlib.util.spec_from_file_location("declaude_lint", DECLAUDE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def hit(line, category, note, match="", severity="warn"):
    return {"line": line, "category": category, "severity": severity, "note": note, "match": match[:160]}

# --------------------------------------------------------------------------- per-file checks

def check_prose(rel: str, src: str, prose: str, declaude) -> list[dict]:
    hits: list[dict] = []
    plines = prose.split("\n")
    for i, ln in enumerate(plines, 1):
        low = ln.lower()
        for w in BANNED_WORDS:
            for m in re.finditer(r"\b" + re.escape(w) + r"\b", low):
                hits.append(hit(i, "banned-word", f"banned/overused AI vocabulary: '{w}'", ln[max(0, m.start() - 30):m.end() + 30]))
        for ph in STAGED_PHRASES:
            for m in re.finditer(ph, low):
                hits.append(hit(i, "staged-phrase", "staged reveal / mechanical opener", ln[max(0, m.start() - 20):m.end() + 40]))
        for m in re.finditer(r"\b(serves as|stands as|acts as|boasts|represents a turning point)\b", low):
            hits.append(hit(i, "copula-avoidance", "use direct is/are/has", ln[max(0, m.start() - 30):m.end() + 40]))
        for m in re.finditer(r"\b(plainly|merely|quietly)\b", low):
            hits.append(hit(i, "flat-certainty-adverb", "adverb standing in for evidence", ln[max(0, m.start() - 30):m.end() + 30]))
        for m in re.finditer(r"\bnot only\b.{0,90}\bbut\b|\bnot just\b.{0,60}\bbut\b|\bis not just\b", low):
            hits.append(hit(i, "not-just-x-but-y", "'not just X but Y' construction", ln[max(0, m.start() - 10):m.end() + 20]))
        for m in re.finditer(r",\s+(?:\w+ly\s+)?(?:achieving|ensuring|highlighting|enabling|preventing|demonstrating|reflecting|"
                             r"underscoring|allowing|providing|resulting|confirming|establishing|illustrating|reducing|"
                             r"increasing|maintaining|offering|yielding|exposing|revealing)\b[^.;:]{3,140}[.;]", ln):
            hits.append(hit(i, "participle-tail", "sentence-final participle tail (candidate)", m.group(0)))
        if ln.count("\u2014") >= 2:
            hits.append(hit(i, "em-dash", f"{ln.count(chr(0x2014))} em-dashes on one line", ln))
        ln_names = ln.replace("Dulce-Odin-OCDS", "")  # approved public repository name
        if NAME_RE.search(ln_names):
            hits.append(hit(i, "personal-name", "personal name in chapter prose (anonymity rule)", NAME_RE.search(ln_names).group(0), "error"))
        if FOURTH_WALL_RE.search(ln):
            hits.append(hit(i, "fourth-wall", "course/milestone/professor reference in prose", FOURTH_WALL_RE.search(ln).group(0), "error"))
        if re.search(r"\bmunicipal ordinance", low):
            hits.append(hit(i, "municipal-term", "Davao City is an HUC: prefer 'local/city ordinance' (review context)", ln[:140], "info"))
    # raw-source tells on the original text (comment-stripped)
    raw = strip_comments(src).split("\n")
    for i, ln in enumerate(raw, 1):
        am = ABLAZO_RE.search(ln)
        if am:
            hits.append(hit(i, "personal-name", "'Ablazo' not directly followed by a formal \\cite (cite by surname + BibTeX key only)", ln.strip()[max(0, am.start() - 40):am.end() + 40], "error"))
        for m in re.finditer(r"(?<!\\)\b(Figure|Table|Section|Appendix|Equation|Algorithm|Chapter|Listing)\s+\\(?:ref|eqref|autoref)\{", ln):
            hits.append(hit(i, "missing-nbsp-ref", "use Figure~\\ref{...} (non-breaking tie)", ln[m.start():m.end() + 20]))
        if re.search(r"[A-Za-z0-9)]\s+\\cite", ln):
            hits.append(hit(i, "space-before-cite", "use word~\\cite{...} (non-breaking tie, no space)", re.search(r"[A-Za-z0-9)]\s+\\cite", ln).group(0)))
        stripped = re.sub(r"\\(?:url|href|texttt|lstinline|verb)\{[^}]*\}", "", ln)
        stripped = re.sub(r"\$[^$]*\$", "", stripped)
        if '"' in stripped and "lstlisting" not in ln:
            hits.append(hit(i, "straight-quote", "use ``double'' LaTeX quotes", ln.strip()[:120]))
        if re.search(r"\\(paragraph|subparagraph)\*?\{", ln):
            hits.append(hit(i, "level4-heading", "\\paragraph/\\subparagraph headers are prohibited", ln.strip()[:100], "error"))
        if MODEL_TT_RE.search(ln) and "&" not in ln:
            hits.append(hit(i, "texttt-model-in-prose", "write model names in roman text in running prose", MODEL_TT_RE.search(ln).group(0), "info"))
    # paragraph cadence (prose blocks only)
    for start, par in paragraphs(prose):
        words = len(par.split())
        if words < 12:
            continue
        n = len(split_sentences(par))
        if n <= 3 and words < 90:
            hits.append(hit(start, "micro-paragraph", f"{n}-sentence / {words}-word paragraph (target 4-6 sentences)", par[:90], "info"))
        elif n >= 11:
            hits.append(hit(start, "long-paragraph", f"{n}-sentence paragraph (consider splitting beyond ~10)", par[:90], "info"))
    # item usage (paragraph-driven flow rule)
    n_items = len(re.findall(r"\\item\b", strip_comments(src)))
    if n_items:
        hits.append(hit(0, "list-usage", f"{n_items} \\item entries in file (avoid unnecessary lists / inline headings)", "", "info"))
    # declaude lexical + density scan on plain prose
    if declaude is not None:
        try:
            dh = declaude.scan_lines(prose, statement_headers=True) + declaude.scan_density(prose)
            dh += declaude.scan_reuse(dh)
            for h in dh:
                hits.append(hit(h.get("line", 0), "declaude:" + h["category"], h["note"], h.get("match", ""), "info"))
        except Exception as exc:  # linter issues must never kill the audit
            hits.append(hit(0, "declaude-error", str(exc), "", "info"))
    return hits


def check_latex(rel: str, src: str) -> list[dict]:
    hits: list[dict] = []
    nc = strip_comments(src)
    first = src.split("\n", 1)[0].strip()
    if (rel.startswith("chapters/") or rel.startswith("appendices/")) and not first.startswith("% !TeX root = ../main.tex"):
        hits.append(hit(1, "root-header", "missing '% !TeX root = ../main.tex' on line 1", first[:60], "error"))
    lines = nc.split("\n")

    def line_of(pos: int) -> int:
        return nc.count("\n", 0, pos) + 1

    # table-level checks
    for m in re.finditer(r"\\begin\{(table\*?|longtable|xltabular)\}.*?\\end\{\1\}", nc, flags=re.S):
        body, ln = m.group(0), line_of(m.start())
        if "\\toprule" not in body:
            hits.append(hit(ln, "table-no-booktabs", "table without \\toprule/\\midrule/\\bottomrule", body[:70], "error"))
        if "\\hline" in body:
            hits.append(hit(ln, "table-hline", "use booktabs rules, not \\hline", "", "error"))
        for cm in re.finditer(r"\\begin\{(?:tabular\*?|tabularx|longtable|xltabular)\}(?:\{[^}]*\})?(?:\[[^\]]*\])?\{([^}]*(?:\{[^{}]*\}[^}]*)*)\}", body):
            if "|" in cm.group(1):
                hits.append(hit(ln, "table-vbar", "vertical bars in column spec", cm.group(1)[:60], "error"))
        if re.search(r"\\textit\{Notes?:?\}|\\textit\{Note\b", body):
            hits.append(hit(ln, "table-note", "\\textit{Note:} under a table (put context in body prose)", "", "error"))
        if re.search(r"\(\s*Proposed\s*\)|\bProposed\)", body):
            hits.append(hit(ln, "proposed-tag", "'(Proposed)' tag on a model in a table", "", "error"))
        cap, tab = body.find("\\caption"), min([i for i in (body.find("\\begin{tabular"), body.find("\\begin{longtable"), body.find("\\begin{xltabular")) if i >= 0] or [10**9])
        if m.group(1) == "table*" or m.group(1) == "table":
            if cap < 0:
                hits.append(hit(ln, "table-no-caption", "table without \\caption", "", "error"))
            elif cap > tab:
                hits.append(hit(ln, "caption-below-table", "caption must be ABOVE the table", "", "error"))
        if "\\label{" not in body and (m.group(1).startswith("table") or "\\caption" in body):
            hits.append(hit(ln, "table-no-label", "captioned table without \\label", "", "error"))
    for m in re.finditer(r"\\begin\{figure\*?\}.*?\\end\{figure\*?\}", nc, flags=re.S):
        body, ln = m.group(0), line_of(m.start())
        if "\\caption" not in body or "\\label{" not in body:
            hits.append(hit(ln, "figure-no-caption-label", "figure missing \\caption or \\label", "", "error"))
        cap = re.search(r"\\caption(?:\[[^\]]*\])?\{((?:[^{}]|\{[^{}]*\})*)\}", body)
        if cap and len(cap.group(1).split()) > 70:
            hits.append(hit(ln, "long-caption", f"caption is {len(cap.group(1).split())} words (captions describe, never argue)", cap.group(1)[:80], "info"))
    # float stacking
    ends = [(m.end(), m.start()) for m in re.finditer(r"\\end\{(?:figure|table|algorithm)\*?\}", nc)]
    begins = [m.start() for m in re.finditer(r"\\begin\{(?:figure|table|algorithm)\*?\}", nc)]
    for e, _ in ends:
        nxt = next((b for b in begins if b >= e), None)
        if nxt is None:
            continue
        gap = re.sub(r"\\(?:begin|end)\{(?:landscape|center)\}|\\(?:label|clearpage|newpage|vspace)\{?[^}]*\}?|\s+", " ", nc[e:nxt]).strip()
        if len(gap) < 60:
            hits.append(hit(line_of(e), "float-stack", "back-to-back floats without intervening explanatory prose", gap[:60]))
    # heading structure
    heads = []
    for m in re.finditer(r"\\(chapter|section|subsection|subsubsection)(\*?)(?:\[([^\]]*)\])?\{((?:[^{}]|\{[^{}]*\})*)\}", nc):
        heads.append((m.group(1), m.group(2), m.group(3), m.group(4), line_of(m.start())))
    lvl = {"chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3}
    for idx, (kind, star, short, title, ln) in enumerate(heads):
        if star:
            continue
        if kind != "chapter":
            plain = re.sub(r"\$[^$]*\$|\\[a-zA-Z]+", "", title)
            if len(plain) > 62 or "(" in plain or ":" in plain:
                hits.append(hit(ln, "long-title", f"title '{plain[:70]}' ({len(plain)} chars): keep single-line & simple", plain, "info"))
        if kind == "chapter" and rel.startswith("appendices/") and len(re.sub(r"\\[a-zA-Z]+", "", title)) > 35 and not short:
            hits.append(hit(ln, "appendix-title-long", "appendix title > 35 chars without short \\chapter[..] title", title[:70], "error"))
        if kind in ("section", "subsection"):
            child = "subsection" if kind == "section" else "subsubsection"
            n = 0
            for k2, s2, _, _, _ in heads[idx + 1:]:
                if lvl[k2] <= lvl[kind]:
                    break
                if k2 == child and not s2:
                    n += 1
            if n == 1:
                hits.append(hit(ln, "orphan-heading", f"{kind} '{title[:50]}' has exactly 1 {child} (needs >= 2)", title[:60], "error"))
    # appendix narrative / Note blocks
    if rel.startswith("appendices/") and re.search(r"\\textit\{Note:?\}", nc):
        hits.append(hit(1, "appendix-note-block", "\\textit{Note:} in appendix (artifacts-only rule)", "", "error"))
    return hits


def abstract_check(src: str) -> list[dict]:
    body = to_prose(src)
    words = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'%.,\-]*", body))
    sev = "error" if words > 250 else "info"
    return [hit(0, "abstract-words", f"abstract has ~{words} words (limit 250)", "", sev)]


def check_stale(rel: str, src: str) -> list[dict]:
    hits = []
    for i, ln in enumerate(strip_comments(src).split("\n"), 1):
        for token, why in STALE_COUNTS.items():
            if token in ln:
                hits.append(hit(i, "stale-count", f"'{token}': {why}", ln.strip()[:130], "warn"))
    return hits

# --------------------------------------------------------------------------- global checks

def parse_bib() -> tuple[dict, list[dict]]:
    path = TEX_DIR / "references.bib"
    text = read(path)
    entries, issues = {}, []
    starts = [(m.start(), m.group(1), m.group(2)) for m in re.finditer(r"^@(\w+)\s*\{\s*([^,\s]+)\s*,", text, flags=re.M)]
    for idx, (pos, etype, key) in enumerate(starts):
        end = starts[idx + 1][0] if idx + 1 < len(starts) else len(text)
        body = text[pos:end]
        line = text.count("\n", 0, pos) + 1
        if etype.lower() in ("comment", "string", "preamble"):
            continue
        fields = {m.group(1).lower() for m in re.finditer(r"^\s*(\w+)\s*=", body, flags=re.M)}
        entries[key] = {"type": etype.lower(), "line": line, "fields": sorted(fields)}
        req = ("title", "year") if etype.lower() == "proceedings" else ("author", "title", "year")
        miss = [f for f in req if f not in fields]
        if etype.lower() == "proceedings" and not fields & {"editor", "author", "organization"}:
            miss.append("editor/organization")
        if miss:
            issues.append(hit(line, "bib-missing-field", f"{key}: missing {', '.join(miss)}", key, "error"))
        if not fields & {"journal", "booktitle", "publisher", "howpublished", "school", "institution", "note", "organization", "eprint"}:
            issues.append(hit(line, "bib-no-venue", f"{key}: no journal/booktitle/publisher/howpublished", key, "warn"))
        if not fields & {"doi", "url", "eprint"}:
            issues.append(hit(line, "bib-no-doi-url", f"{key}: no doi/url (verify against source)", key, "info"))
        tm = re.search(r"^\s*title\s*=\s*", body, flags=re.M | re.I)
        if tm:
            seg = body[tm.end():]
            depth, out = 0, []
            for ch in seg:
                if ch == "{":
                    depth += 1
                    if depth > 1:
                        continue
                    continue
                if ch == "}":
                    depth -= 1
                    if depth < 0:
                        break
                    continue
                if depth == 1:
                    out.append(ch)
                if depth == 0 and ch == ",":
                    break
            unprotected = " ".join(out)
            ac = re.findall(r"\b(?:[A-Z]{2,}[A-Za-z0-9]*|[A-Za-z]+[A-Z][A-Za-z]*)\b", unprotected)
            ac = [a for a in ac if a not in ("A", "I")]
            if ac:
                issues.append(hit(line, "bib-unprotected-title-caps", f"{key}: acronyms/model names not brace-protected: {', '.join(sorted(set(ac))[:6])}", key, "warn"))
        if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            issues.append(hit(line, "bib-key-style", f"{key}: key should be lowercase surnameYearKeyword", key, "info"))
    return entries, issues


def global_checks(files: dict[str, str]) -> dict:
    labels, label_file = set(), {}
    refs: dict[str, set] = defaultdict(set)
    cites: dict[str, set] = defaultdict(set)
    for rel, src in files.items():
        nc = strip_comments(src)
        for m in re.finditer(r"\\label\{([^}]*)\}", nc):
            labels.add(m.group(1))
            label_file[m.group(1)] = rel
        for m in re.finditer(r"\\begin\{lstlisting\}\[[^\]]*?label\s*=\s*\{?([A-Za-z0-9_:\-]+)", nc):
            labels.add(m.group(1))
            label_file[m.group(1)] = rel
        for m in re.finditer(r"\\(?:ref|eqref|autoref|pageref|cref|Cref)\{([^}]*)\}", nc):
            for k in m.group(1).split(","):
                refs[k.strip()].add(rel)
        for m in re.finditer(r"\\hyperref\[([^\]]*)\]", nc):
            refs[m.group(1).strip()].add(rel)
        for m in re.finditer(r"\\(?:cite[a-z]*|nocite)\*?(?:\[[^\]]*\])*\{([^}]*)\}", nc):
            for k in m.group(1).split(","):
                if k.strip():
                    cites[k.strip()].add(rel)
    entries, bib_issues = parse_bib()
    undefined_refs = sorted(k for k in refs if k not in labels)
    undefined_cites = sorted(k for k in cites if k not in entries)
    chapter_refs = {k for k, fs in refs.items() if any(f.startswith("chapters/") for f in fs)}
    unref = []
    for lab in sorted(labels):
        if lab.startswith(("fig:", "tab:", "eq:", "alg:", "lst:")) and lab not in refs:
            sev = "info" if label_file[lab].startswith("appendices/") else "warn"
            unref.append({"label": lab, "file": label_file[lab], "severity": sev})
    orphan_apps = sorted(l for l in labels if l.startswith("app:") and l not in chapter_refs)
    unused_bib = sorted(k for k in entries if k not in cites)
    pdf_stems = {p.stem.lower() for p in REFS_DIR.glob("*.pdf")} if REFS_DIR.exists() else set()
    cited_no_pdf = sorted(k for k in cites if k in entries and k.lower() not in pdf_stems)
    log = parse_log()
    return {
        "undefined_refs": undefined_refs, "undefined_cites": undefined_cites,
        "unreferenced_floats": unref, "orphan_appendices": orphan_apps,
        "bib": {"entries": len(entries), "issues": bib_issues, "unused_keys": unused_bib,
                "cited_keys": len(cites), "cited_without_local_pdf": cited_no_pdf, "local_pdf_count": len(pdf_stems)},
        "log": log,
    }


def parse_log() -> dict:
    p = TEX_DIR / "main.log"
    out = {"present": p.exists(), "overfull_ge_1pt": [], "undefined": [], "overfull_total": 0}
    if not p.exists():
        return out
    text = p.read_text(encoding="latin1", errors="ignore")
    for m in re.finditer(r"Overfull \\hbox \(([\d.]+)pt too wide\)[^\n]*", text):
        out["overfull_total"] += 1
        if float(m.group(1)) >= 1.0:
            out["overfull_ge_1pt"].append({"pt": float(m.group(1)), "where": m.group(0)[:110]})
    out["overfull_ge_1pt"].sort(key=lambda d: -d["pt"])
    for m in re.finditer(r"LaTeX Warning: (?:Reference|Citation) `([^']+)' on page \d+ undefined", text):
        out["undefined"].append(m.group(1))
    return out

# --------------------------------------------------------------------------- driver

def run_audit(only: list[str] | None, lint: bool) -> dict:
    rels = active_files()
    sources = {rel: read(TEX_DIR / rel) for rel in rels}
    declaude = load_declaude() if lint else None
    report: dict = {"generated": datetime.now().isoformat(timespec="seconds"), "canonical": CANON,
                    "active_files": rels, "files": {}}
    totals: Counter = Counter()
    for rel in rels:
        if only and rel not in only:
            continue
        src = sources[rel]
        prose = to_prose(src)
        hits = check_latex(rel, src) + check_stale(rel, src)
        if rel.startswith(PROSE_PREFIXES):
            hits += check_prose(rel, src, prose, declaude)
            if rel.endswith("abstract.tex"):
                hits += abstract_check(src)
        hits.sort(key=lambda h: (h["line"], h["category"]))
        counts = Counter(h["category"] for h in hits)
        totals.update(counts)
        report["files"][rel] = {
            "lines": src.count("\n") + 1, "words_prose": len(prose.split()),
            "prose_linted": rel.startswith(PROSE_PREFIXES), "counts": dict(counts.most_common()), "hits": hits,
        }
    report["global"] = global_checks(sources)
    report["totals"] = dict(totals.most_common())
    return report


def write_markdown(report: dict, path: Path) -> None:
    g = report["global"]
    L = [f"# Manuscript Pre-Audit Summary ({report['generated']})", "",
         "Candidates only; every hit still needs reading in context.", "",
         "## Per-file candidate counts", "", "| File | Lines | Prose words | Total hits | Errors | Top categories |", "| :-- | --: | --: | --: | --: | :-- |"]
    for rel, d in report["files"].items():
        errs = sum(1 for h in d["hits"] if h["severity"] == "error")
        top = ", ".join(f"{k}:{v}" for k, v in list(d["counts"].items())[:5])
        L.append(f"| {rel} | {d['lines']} | {d['words_prose']} | {len(d['hits'])} | {errs} | {top} |")
    L += ["", "## Global integrity", "",
          f"- Undefined `\\ref` targets: {len(g['undefined_refs'])} {g['undefined_refs'][:15]}",
          f"- Undefined `\\cite` keys: {len(g['undefined_cites'])} {g['undefined_cites'][:15]}",
          f"- Unreferenced fig/tab/eq labels: {len(g['unreferenced_floats'])} (chapters: {sum(1 for u in g['unreferenced_floats'] if u['severity']=='warn')})",
          f"- Appendices never cited from chapters: {g['orphan_appendices']}",
          f"- BibTeX: {g['bib']['entries']} entries, {g['bib']['cited_keys']} cited keys, {len(g['bib']['unused_keys'])} unused, "
          f"{len(g['bib']['issues'])} structural issues, {len(g['bib']['cited_without_local_pdf'])} cited keys without a `docs/references/<key>.pdf`",
          f"- main.log: {g['log']['overfull_total']} overfull hboxes ({len(g['log']['overfull_ge_1pt'])} >= 1pt), {len(g['log']['undefined'])} undefined refs/cites", ""]
    path.write_text("\n".join(L), encoding="utf-8")


def cmd_slice(args) -> int:
    audit_path = Path(args.audit)
    data = json.loads(audit_path.read_text(encoding="utf-8"))
    rel, lo, hi = args.slice[0], int(args.slice[1]), int(args.slice[2])
    d = data["files"].get(rel)
    if d is None:
        print(f"no such file in audit: {rel}")
        return 2
    rows = [h for h in d["hits"] if lo <= h["line"] <= hi]
    whole = [h for h in d["hits"] if h["line"] == 0]
    print(f"# {rel} lines {lo}-{hi}: {len(rows)} candidates (+{len(whole)} whole-file notes)")
    for h in whole:
        print(f"  [file] {h['category']}: {h['note']}")
    for h in rows:
        print(f"L{h['line']:>5} [{h['severity']}] {h['category']}: {h['note']} | {h['match']}")
    return 0


def cmd_compare(args) -> int:
    a = json.loads(Path(args.compare[0]).read_text(encoding="utf-8"))
    b = json.loads(Path(args.compare[1]).read_text(encoding="utf-8"))
    cats = sorted(set(a["totals"]) | set(b["totals"]))
    print(f"{'category':<34}{'before':>8}{'after':>8}{'delta':>8}")
    for c in cats:
        x, y = a["totals"].get(c, 0), b["totals"].get(c, 0)
        print(f"{c:<34}{x:>8}{y:>8}{y - x:>+8}")
    ga, gb = a["global"], b["global"]
    for k in ("undefined_refs", "undefined_cites", "orphan_appendices"):
        print(f"{k:<34}{len(ga[k]):>8}{len(gb[k]):>8}{len(gb[k]) - len(ga[k]):>+8}")
    return 0


def cmd_outline(args) -> int:
    """Heading outline (with original line numbers) for every active chapter/appendix."""
    for rel in active_files():
        if args.files and rel not in args.files:
            continue
        nc = strip_comments(read(TEX_DIR / rel))
        print(f"## {rel}")
        for m in re.finditer(r"\\(chapter|section|subsection|subsubsection)(\*?)(?:\[[^\]]*\])?\{((?:[^{}]|\{[^{}]*\})*)\}", nc):
            ln = nc.count("\n", 0, m.start()) + 1
            ind = {"chapter": "", "section": "  ", "subsection": "    ", "subsubsection": "      "}[m.group(1)]
            print(f"L{ln:>5} {ind}{m.group(1)} {re.sub(r'[$\\\\]', '', m.group(3))[:90]}")
    return 0


def chunk_ranges(rel: str, target_bytes: int) -> list[list[int]]:
    """Split a file into line ranges of ~target_bytes, breaking only just before a heading."""
    lines = read(TEX_DIR / rel).split("\n")
    total = len(lines)
    heading = re.compile(r"^\s*\\(?:chapter|section|subsection|subsubsection)\b")
    ranges, start, acc = [], 1, 0
    for i, ln in enumerate(lines, 1):
        if acc >= target_bytes and heading.match(ln) and i > start:
            ranges.append([start, i - 1])
            start, acc = i, 0
        acc += len(ln.encode("utf-8")) + 1
    if ranges and acc < 0.35 * target_bytes:  # avoid a tiny tail slice: fold it into the previous one
        ranges[-1][1] = total
    else:
        ranges.append([start, total])
    return ranges


def cmd_chunks(args) -> int:
    rel = args.chunks
    print(json.dumps(chunk_ranges(rel, int(args.target_kb * 1024))))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "output" / "paper_pre_audit.json"))
    ap.add_argument("--files", nargs="*", help="limit to these files (relative to CS_Undergraduate_Thesis_Template)")
    ap.add_argument("--no-lint", action="store_true", help="skip the declaude lexical scan")
    ap.add_argument("--slice", nargs=3, metavar=("FILE", "START", "END"))
    ap.add_argument("--audit", default=str(ROOT / "output" / "paper_pre_audit.json"), help="audit JSON used by --slice")
    ap.add_argument("--compare", nargs=2, metavar=("BEFORE", "AFTER"))
    ap.add_argument("--outline", action="store_true", help="print heading outline with line numbers")
    ap.add_argument("--chunks", metavar="FILE", help="print JSON line ranges splitting FILE at headings")
    ap.add_argument("--target-kb", type=float, default=80.0)
    args = ap.parse_args()
    if args.slice:
        return cmd_slice(args)
    if args.compare:
        return cmd_compare(args)
    if args.outline:
        return cmd_outline(args)
    if args.chunks:
        return cmd_chunks(args)
    report = run_audit(args.files, lint=not args.no_lint)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    write_markdown(report, out.with_suffix(".md"))
    print(f"wrote {out} and {out.with_suffix('.md')}")
    for rel, d in report["files"].items():
        errs = sum(1 for h in d["hits"] if h["severity"] == "error")
        print(f"  {rel:<46} hits={len(d['hits']):>5} errors={errs:>4}")
    g = report["global"]
    print(f"  undefined refs={len(g['undefined_refs'])} cites={len(g['undefined_cites'])} orphan appendices={len(g['orphan_appendices'])}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
