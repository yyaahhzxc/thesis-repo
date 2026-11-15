# Paper audit + chapter-by-chapter sweep (reusable `run_workflow` script).
#
# Launch:   run_workflow(ScriptPath="<repo>/scripts/workflows/paper_sweep/workflow.py",
#                        Description="Full manuscript audit and sweep", Args={...})
# Docs:     scripts/workflows/paper_sweep/README.md  and  .agents/skills/paper-sweep/SKILL.md
#
# Args (all optional):
#   mode              "apply" (default: edit files in place) | "audit_only" (no edits; proposed edits reported)
#   only_units        list limiting Phase 2, e.g. ["introduction", "methodology"]. Default: every unit.
#                     units: introduction, literature_review, methodology, results_and_discussion,
#                            conclusions, abstract, appendices_and_bib
#   slice_kb          target prose-slice size in KB (default 80). Slices break only before headings.
#   build             run build_paper.py + auto-fix loop in Phase 3 (default true; ignored if audit_only)
#   mechanical_model  model tier for the read-only structural/bib audit agent (default "flash")
#   dry_run           true = Phase 0 + slice plan only; no agents, no edits (0 LLM tokens)
import json
import os
import subprocess
import sys
from datetime import datetime

try:
    A = dict(args) if args else {}
except NameError:
    A = {}

REPO = (WORKSPACES[0] if WORKSPACES else os.getcwd()).replace("\\", "/")
TEXD = "CS_Undergraduate_Thesis_Template"
AUDIT_PY = "scripts/audit/pre_audit_paper.py"
MODE = A.get("mode", "apply")
APPLY = MODE == "apply"
SLICE_KB = float(A.get("slice_kb", 80))
DO_BUILD = bool(A.get("build", True)) and APPLY
MECH_MODEL = A.get("mechanical_model", "flash")
DRY = bool(A.get("dry_run", False))
ONLY = A.get("only_units") or None

RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
OUT = "output/paper_sweep/" + RUN_ID
os.makedirs(os.path.join(REPO, OUT), exist_ok=True)

ALL_UNITS = [
    ("introduction", "chapters/introduction.tex"),
    ("literature_review", "chapters/literature_review.tex"),
    ("methodology", "chapters/methodology.tex"),
    ("results_and_discussion", "chapters/results_and_discussion.tex"),
    ("conclusions", "chapters/conclusions.tex"),
    ("abstract", "chapters/abstract.tex"),
    ("appendices_and_bib", None),
]

RULE_FILES = [
    REPO + "/.agents/rules/paper-structure-and-chapters.md",
    REPO + "/.agents/rules/paper-voice-and-style.md",
    REPO + "/.agents/rules/paper-rigor-and-citations.md",
    REPO + "/.agents/rules/paper-latex-and-visuals.md",
    REPO + "/" + TEXD + "/AGENTS.md",
]


def P(rel):
    return REPO + "/" + TEXD + "/" + rel


def sh(cmd, timeout=600):
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def audit(out_json, files=None, lint=True):
    cmd = [sys.executable, AUDIT_PY, "--out", out_json]
    if files:
        cmd += ["--files"] + list(files)
    if not lint:
        cmd.append("--no-lint")
    return sh(cmd, 300)


def load(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as f:
        return json.load(f)


def chunk_plan(rel):
    code, out = sh([sys.executable, AUDIT_PY, "--chunks", rel, "--target-kb", str(SLICE_KB)], 120)
    ranges = json.loads(out.strip().splitlines()[-1])
    with open(P(rel), encoding="utf-8") as f:
        lines = f.read().split("\n")
    anchors = [lines[r[0] - 1] for r in ranges[1:]]  # exact heading line that starts slices 2..n
    return ranges, anchors, len(lines)


def resolve_ranges(rel, anchors):
    """Re-locate slice boundaries by heading text (earlier edits may have shifted line numbers)."""
    with open(P(rel), encoding="utf-8") as f:
        lines = f.read().split("\n")
    pos, starts = 0, []
    for a in anchors:
        idx = next((i for i in range(pos, len(lines)) if lines[i] == a), None)
        if idx is None:
            return None
        starts.append(idx + 1)
        pos = idx + 1
    begins = [1] + starts
    ends = [s - 1 for s in starts] + [len(lines)]
    return [[b, e] for b, e in zip(begins, ends)]


# ---------------------------------------------------------------- shared prompt material

CONTEXT = (
    "PROJECT: Undergraduate CS thesis (Ateneo de Davao University): 'A Coarse-to-Fine Semantic Conflict Detection System "
    "for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference'. LaTeX sources live in "
    + REPO + "/" + TEXD + "/ (compiled with pdflatex+bibtex; chapters/ and appendices/ are included by main.tex). "
    "Shell is Windows PowerShell; use `python` for scripts. Repo root: " + REPO + ".\n"
    "CANONICAL FACTS (never contradict or silently change): 27,248 unique enactments = 25,432 national statutes + 1,816 deduplicated "
    "Davao City ordinances; 177,423 unique provisions; ground truth N=350 curated pairs (static 70/15/15 split = 245/52/53), "
    "198 unique instances in zero-leakage premise-grouped CV; calibrated threshold tau*=0.45; Stage 1 hybrid BM25 + dense retrieval, "
    "Stage 2 DeBERTa-v3 cross-encoder NLI. The study is strictly ex-ante, an assistive screening tool (not legal adjudication). "
    "Report Actual Substantive Legal Conflicts separately from System-Found Conflicts/Alarms.\n"
    "PROTECTED CONTENT (never alter): \\label/\\ref/\\cite keys, numeric results and table values, equation bodies, "
    "verbatim statutory/ordinance/case quotations (anything quoted from Lawphil or SP archives), BibTeX keys, file paths/URLs. "
    "Approved exception: the repository name 'Dulce-Odin-OCDS' may appear in a URL. "
    "If prose disagrees with a table/number elsewhere, do NOT guess which is right: flag it as CONSISTENCY.\n"
    "NO INVENTION: never add a fact, number, citation, author, DOI, or quote that is not already in the manuscript or verified from "
    "a local source. A rewrite for style must keep every claim. A claim attributed to \\cite{key} that mentions a specific number, "
    "threshold, formula, or rule must be verified against the local PDF with: python scripts/audit/ref_grep.py KEY \"phrase\" \"number\" "
    "(exit 1/2 or 'NOT FOUND' = unverified). For an unverified specific attribution: if the sentence survives without the specific "
    "figure, reword it to what the source verifiably supports; otherwise leave the text and flag CITE. Never fabricate a replacement citation.\n"
    "EDIT MECHANICS: edit_file replaces EVERY occurrence of its Target, so include enough surrounding text to make each Target unique "
    "and keep one contiguous block per edit. Preserve each line's existing structure; do not reflow whole paragraphs unnecessarily. "
    "Where something needs a human decision, insert a LaTeX comment line directly above the paragraph, e.g. '% [CITE: ...]', "
    "'% [DATA: ...]' or '% [HUMAN: ...]' (searchable, invisible in the PDF), and also report it in flags.\n"
)

SLICE_SCHEMA = {
    "type": "object",
    "required": ["summary", "edits", "flags", "handoff"],
    "properties": {
        "summary": {"type": "string", "description": "<=80 words: what you reviewed and the overall state of the slice"},
        "edits": {
            "type": "array",
            "description": "one entry per rule family you applied (or proposed, in audit_only mode)",
            "items": {"type": "object", "required": ["rule", "count", "example"],
                      "properties": {"rule": {"type": "string"}, "count": {"type": "integer"},
                                     "example": {"type": "string", "description": "one short before -> after example"}}},
        },
        "flags": {
            "type": "array",
            "items": {"type": "object", "required": ["kind", "where", "note"],
                      "properties": {"kind": {"type": "string", "enum": ["CITE", "DATA", "HUMAN", "CONSISTENCY"]},
                                     "where": {"type": "string", "description": "file:line or section label"},
                                     "note": {"type": "string"}}},
        },
        "handoff": {"type": "string", "description": "<=120 words for the NEXT slice agent: terminology decisions made, "
                                                   "recurring defects, anything it must stay consistent with"},
    },
}

FINDINGS_SCHEMA = {
    "type": "object",
    "required": ["summary", "findings"],
    "properties": {
        "summary": {"type": "string"},
        "findings": {
            "type": "array",
            "items": {"type": "object", "required": ["file", "severity", "note"],
                      "properties": {"file": {"type": "string", "description": "path relative to the template dir, e.g. chapters/introduction.tex"},
                                     "line": {"type": "integer"},
                                     "severity": {"type": "string", "enum": ["error", "warn", "info"]},
                                     "note": {"type": "string"}}},
        },
    },
}

BUILD_FIX_SCHEMA = {
    "type": "object",
    "required": ["summary", "fixed"],
    "properties": {"summary": {"type": "string"}, "fixed": {"type": "boolean"}},
}


def rules_block():
    return ("STEP 0 - LOAD ALL RULES IN FULL (do not skim, do not prioritise one over another): read each of these files completely:\n  - "
            + "\n  - ".join(RULE_FILES) + "\n")


def slice_prompt(unit, rel, lo, hi, k, n, ledger_json, handoffs, xfind):
    mode_line = (
        "MODE = APPLY: edit the .tex file in place with edit_file. Edit prose only inside your line range."
        if APPLY else
        "MODE = AUDIT_ONLY: DO NOT modify any file. Put each proposed change in `edits` (rule, count, one before->after example) and in flags."
    )
    ho = "\n".join("- " + h for h in handoffs[-3:]) if handoffs else "(none; this is the first slice processed)"
    xf = "\n".join("- [%s] L%s %s" % (f.get("severity", ""), f.get("line", "?"), f.get("note", "")) for f in xfind) if xfind else "(none)"
    return (
        "THESIS SWEEP AGENT - " + unit + " slice " + str(k) + "/" + str(n) + " (" + rel + ", lines " + str(lo) + "-" + str(hi) + ")\n\n"
        + CONTEXT + "\n" + mode_line + "\n\n" + rules_block() + "\n"
        "STEP 1 - LEDGER. Run: python " + AUDIT_PY + " --slice " + rel + " " + str(lo) + " " + str(hi) + " --audit " + ledger_json + "\n"
        "These are regex/linter CANDIDATES for your line range (line numbers match the current file). Also run: python " + AUDIT_PY +
        " --outline --files " + rel + " to see the heading structure. Candidates are not verdicts: judge each in context.\n\n"
        "STEP 2 - READ EVERYTHING in your range, in order, with consecutive read_file calls on " + P(rel) + " (StartLine/EndLine; each read returns at most ~46 KB, "
        "so continue until you have covered every line from " + str(lo) + " to " + str(hi) + "). Never skip lines or only sample. Long lines are normal: each line is usually one paragraph.\n\n"
        "STEP 3 - ANALYSE every paragraph, table, figure, equation and list in range against ALL FOUR rule files. Checklist (non-exhaustive): "
        "structure (heading depth <=3, no orphan subsections, simple single-line titles, paragraph-driven prose, no hindsight leakage: "
        "Ch.1-2 must not announce chosen models/results, Ch.3 must not report results, Ch.4 maps to the research questions/objectives); "
        "voice (undergraduate tone, anonymity: no personal names - refer to 'the thesis adviser'/'the proponents'; plain literal names; "
        "no triads, participle tails, copula avoidance, inanimate agency, staged reveals, em-dash drama, 'not just X but Y', flat-certainty adverbs, "
        "banned buzzwords incl. protocol/bottleneck/leverage/utilize/crucial; 4-6 sentence paragraphs - expand or merge micro-paragraphs, split >10-sentence ones; "
        "vocabulary at Chapter 1-2 level; Davao City is a Highly Urbanized City: say local/city ordinance, not municipal); "
        "rigor (every substantial claim, threshold, parameter or design choice has a verifiable citation or a plain stated rationale; "
        "verify specific numeric attributions with ref_grep.py; contingency/McNemar/Friedman/Wilcoxon/PPV arithmetic and sample sizes are consistent: N=53, 198, 350; "
        "no verbatim legal text altered); "
        "LaTeX/visuals (non-breaking ties Figure~\\ref, word~\\cite; ``LaTeX'' quotes; booktabs only, no |, captions above tables, value-only cells, no \\textit{Note:} under tables, "
        "no (Proposed) tags, roman model names in running prose; Setup -> Visual -> Dedicated Exposition with brief captions; no back-to-back float walls; "
        "every figure/table/equation cited in text near its placement; appendices cited with Appendix~\\ref).\n\n"
        "CROSS-CHAPTER FINDINGS for this file (from the Phase 1 structural audit; address if they fall in your range):\n" + xf + "\n\n"
        "HANDOFF NOTES from previous slices (stay consistent with them):\n" + ho + "\n\n"
        "STEP 4 - " + ("APPLY edits now (surgical, claim-preserving). Fix every genuine defect you found, not only the ledger candidates."
                       if APPLY else "Do not edit. Record proposed edits.") + "\n\n"
        "STEP 5 - VERIFY. " + ("Re-run: python " + AUDIT_PY + " --files " + rel + " --out " + OUT + "/verify_" + unit + "_" + str(k) +
                               ".json then python " + AUDIT_PY + " --slice " + rel + " " + str(lo) + " " + str(hi + 400) + " --audit " + OUT + "/verify_" + unit + "_" + str(k) +
                               ".json and make sure you introduced no severity=error hit. Do NOT run build_paper.py (the workflow builds once at the end)."
                               if APPLY else "No verification run needed.") + "\n\n"
        "STEP 6 - Call finish with the schema: concise summary, edits grouped by rule family, flags for anything needing a human, and a handoff (<=120 words)."
    )


# ---------------------------------------------------------------- Phase 0

phase("Phase 0: deterministic pre-audit (0 LLM tokens)")
PRE = OUT + "/pre_audit.json"
code, out = audit(PRE)
log("pre-audit exit", code)
if code != 0:
    raise RuntimeError("pre-audit failed:\n" + out[-2000:])
pre = load(PRE)
for rel_, d in pre["files"].items():
    errs = sum(1 for h in d["hits"] if h["severity"] == "error")
    if d["hits"]:
        log("%-44s hits=%-5d errors=%d" % (rel_, len(d["hits"]), errs))
g0 = pre["global"]
log("undefined refs=%d cites=%d orphan appendices=%d bib issues=%d overfull(>=1pt)=%d" % (
    len(g0["undefined_refs"]), len(g0["undefined_cites"]), len(g0["orphan_appendices"]),
    len(g0["bib"]["issues"]), len(g0["log"]["overfull_ge_1pt"])))

units = [u for u in ALL_UNITS if not ONLY or u[0] in ONLY]
plans = {}
for name, rel in units:
    if rel:
        ranges, anchors, total = chunk_plan(rel)
        plans[name] = {"rel": rel, "anchors": anchors, "n": len(ranges)}
        log("slice plan %-24s %d slice(s): %s" % (name, len(ranges), ranges))

if DRY:
    log("dry_run: stopping before any agent runs. Output dir:", OUT)
    print(json.dumps({"out": OUT, "units": [u[0] for u in units], "slices": {k: v["n"] for k, v in plans.items()}}))
else:
    # ---------------------------------------------------------------- Phase 1
    phase("Phase 1: cross-chapter and structural audit (read-only)")
    cross_prompt = (
        "CROSS-CHAPTER STRUCTURAL AUDITOR (read-only; do NOT edit any file)\n\n" + CONTEXT + "\n" + rules_block() + "\n"
        "Goal: find defects that only show up ACROSS chapters, so the per-chapter sweep agents (which see one slice at a time) can fix them. "
        "Do not read whole chapters; use the tools below and read only targeted line ranges.\n"
        "1. Run: python " + AUDIT_PY + " --outline   (heading outline of every active file with line numbers). Read " + P("chapters/introduction.tex") +
        " Problem Statement and Objectives sections fully, plus " + P("chapters/abstract.tex") + " and the opening of " + P("chapters/conclusions.tex") + ".\n"
        "2. Mapping: do the 5 research questions and 5 objectives of Chapter 1 each have a dedicated, identifiable section in Chapter 4 (Results and Discussion) "
        "and a matching conclusion in Chapter 5? Report gaps or mismatched numbering/wording.\n"
        "3. Curse of Knowledge: use Select-String (PowerShell) on chapters/introduction.tex, chapters/literature_review.tex and chapters/methodology.tex for result-like content "
        "(measured percentages, F1/accuracy values such as 86.44, 0.8945, 92.45, 12.69, 'achieved', 'outperform', Tier results, chosen-winner announcements) and report each leak with file and line. "
        "Chapter 2 must also not say 'our pipeline'/'the researchers chose'.\n"
        "4. Canonical counts: Select-String all active chapters for 27,248 / 25,432 / 1,816 / 177,423 / 27,357 / 27,096 / 1,925 / 1,660 / 176,421 and report inconsistent or stale uses "
        "(176,421 is the demo's serialized index size and may be legitimate only when explicitly framed so).\n"
        "5. Abstract: count words precisely (target <= 250, single paragraph) and check each numeric anchor in it (86.44% +/- 6.05%, 0.8945, 12.69 s, 1,416.4 MB, 27,248, 177,423, Tier 2 counts) against Chapter 4/5 text.\n"
        "6. Appendix citation: every \\label{app:...} should be cited from Chapters 1-5 (see global section of " + PRE + ").\n"
        "Return findings (file relative to the template dir, line, severity, concise note)."
    )
    bib_prompt = (
        "APPENDIX + BIBLIOGRAPHY STRUCTURAL AUDITOR (read-only; do NOT edit any file)\n\n" + CONTEXT + "\n" + rules_block() + "\n"
        "Inputs: the deterministic audit " + REPO + "/" + PRE + " (open it; look at files under 'appendices/' and the 'global' section: bib issues, unreferenced floats, log). "
        "For each appendix hit and each BibTeX issue, open the relevant lines and decide if it is a real defect against the rules (appendix artifacts-only format, "
        "short chapter titles >35 chars, no \\textit{Note:} blocks, brief captions, +45pt header clearance; BibTeX completeness and brace-protected acronyms/model names). "
        "Do NOT open appendices/appendix_n.tex or appendices/appendix_tier3_results.tex beyond the specific lines in the ledger (they are very large verbatim/tabular archives). "
        "For each real defect return a finding with the exact file/line and the precise fix that should be applied (e.g. the replacement caption or the corrected BibTeX title with braces). "
        "Do not rename BibTeX keys. Do not invent DOIs; if a DOI/URL is missing, mark it as needing human verification."
    )
    jobs = [
        {"role": "Cross-chapter auditor", "prompt": cross_prompt, "model": "inherit"},
        {"role": "Appendix and bib auditor", "prompt": bib_prompt, "model": MECH_MODEL},
    ]
    p1 = await parallel(jobs, lambda j: agent(j["prompt"], schema=FINDINGS_SCHEMA, role=j["role"], model=j["model"]))
    findings = []
    for r in p1:
        log(r["summary"][:300])
        findings += r["findings"]
    with open(os.path.join(REPO, OUT, "phase1_findings.json"), "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=1)
    log("phase 1 findings:", len(findings))

    # ---------------------------------------------------------------- Phase 2
    results = []
    handoffs = []
    for name, rel in units:
        phase("Phase 2: " + name)
        xf = [x for x in findings if (rel and x["file"] == rel) or (not rel and (x["file"].startswith("appendices/") or x["file"].endswith(".bib") or x["file"] == "main.tex"))]
        if rel is None:
            prompt = (
                "THESIS SWEEP AGENT - appendices, main.tex and references.bib\n\n" + CONTEXT + "\n" +
                ("MODE = APPLY: edit files in place with edit_file.\n" if APPLY else "MODE = AUDIT_ONLY: DO NOT modify any file; report proposed edits.\n") + "\n" + rules_block() + "\n"
                "SCOPE (stay inside it): the defects in these sources, and nothing else:\n"
                "  (a) Phase 1 findings below, (b) severity=error and warn hits for files under appendices/ and 'bib-*' issues in " + REPO + "/" + PRE +
                ", (c) appendix titles > 35 chars need \\chapter[Short]{Full}, appendix captions must be brief factual descriptions, appendices contain no analytical discussion or \\textit{Note:} blocks "
                "(before deleting a Note block, check that its content is already stated in the body chapters, e.g. with Select-String; if it is not, keep the content by flagging HUMAN instead of deleting it), "
                "(d) BibTeX: add missing brace protection on acronyms/model names in titles, fix missing required fields ONLY when the value is already present elsewhere in the entry or can be verified; never rename keys; never invent DOIs or authors; "
                "list unverifiable entries as CITE flags.\n"
                "Do NOT open appendices/appendix_n.tex or appendices/appendix_tier3_results.tex except at ledger lines. Do NOT run build_paper.py.\n\n"
                "PHASE 1 FINDINGS for these files:\n" + ("\n".join("- %s L%s [%s] %s" % (x["file"], x.get("line", "?"), x["severity"], x["note"]) for x in xf) if xf else "(none)") + "\n\n"
                "HANDOFF NOTES from chapter slices:\n" + ("\n".join("- " + h for h in handoffs[-4:]) if handoffs else "(none)") + "\n\n"
                "Call finish with the schema (summary, edits grouped by rule family, flags, handoff)."
            )
            try:
                r = await agent(prompt, schema=SLICE_SCHEMA, role="Sweep: appendices and bib")
            except Exception as exc:  # keep the sweep alive
                r = {"summary": "FAILED: " + str(exc)[:300], "edits": [], "flags": [{"kind": "HUMAN", "where": "appendices_and_bib", "note": "agent failed: " + str(exc)[:200]}], "handoff": ""}
            results.append({"unit": name, "file": "appendices/*, references.bib", "range": "-", **r})
            log(name, "->", r["summary"][:200])
            continue

        plan = plans[name]
        for k in range(1, plan["n"] + 1):
            ranges = resolve_ranges(rel, plan["anchors"])
            if ranges is None:
                ranges, _, _ = chunk_plan(rel)  # anchor lost (heading edited): fall back to a fresh plan
                log("anchor lost; re-planned slices for", rel, ranges)
            lo, hi = ranges[min(k, len(ranges)) - 1]
            ledger = OUT + "/ledger_" + name + "_" + str(k) + ".json"
            audit(ledger, files=[rel])  # fresh ledger => line numbers match the current file
            prompt = slice_prompt(name, rel, lo, hi, k, plan["n"], ledger, handoffs, xf)
            try:
                r = await agent(prompt, schema=SLICE_SCHEMA, role="Sweep: " + name + " " + str(k) + "/" + str(plan["n"]))
            except Exception as exc:
                r = {"summary": "FAILED: " + str(exc)[:300], "edits": [], "flags": [{"kind": "HUMAN", "where": rel + ":" + str(lo) + "-" + str(hi), "note": "agent failed: " + str(exc)[:200]}], "handoff": ""}
            results.append({"unit": name, "file": rel, "range": "%d-%d" % (lo, hi), **r})
            if r.get("handoff"):
                handoffs.append(name + " " + str(k) + "/" + str(plan["n"]) + ": " + r["handoff"])
            log(name, str(k) + "/" + str(plan["n"]), "->", r["summary"][:200])
        with open(os.path.join(REPO, OUT, "slice_results.json"), "w", encoding="utf-8") as f:
            json.dump(results, f, indent=1)

    with open(os.path.join(REPO, OUT, "slice_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)

    # ---------------------------------------------------------------- Phase 3
    phase("Phase 3: re-audit, build, report")
    POST = OUT + "/post_audit.json"
    audit(POST)
    build_info = {"ran": False}
    if DO_BUILD:
        for attempt in (1, 2):
            code, bout = sh([sys.executable, "scripts/build_paper.py"], 3000)
            audit(POST)  # after the build so main.log reflects this attempt
            post = load(POST)
            gl = post["global"]
            bad = (code != 0) or gl["undefined_refs"] or gl["undefined_cites"] or gl["log"]["undefined"]
            build_info = {"ran": True, "attempt": attempt, "exit": code, "tail": bout[-1500:],
                          "undefined_refs": gl["undefined_refs"], "undefined_cites": gl["undefined_cites"],
                          "log_undefined": gl["log"]["undefined"][:20], "overfull_ge_1pt": len(gl["log"]["overfull_ge_1pt"])}
            log("build attempt", attempt, "exit", code, "undef refs", len(gl["undefined_refs"]), "undef cites", len(gl["undefined_cites"]))
            if not bad or attempt == 2:
                break
            fixer = (
                "BUILD FIXER\n\n" + CONTEXT + "\nThe manuscript sweep finished editing, but the LaTeX build is not clean. Fix ONLY what breaks the build: "
                "LaTeX errors, undefined references/citations, malformed environments introduced by the sweep (use `git diff` on " + TEXD + " to see what changed). "
                "Do not restyle prose. Do not change numbers or citations' meaning. Build output tail:\n" + bout[-3000:] + "\n"
                "Undefined refs: " + str(gl["undefined_refs"][:20]) + " Undefined cites: " + str(gl["undefined_cites"][:20]) + " Log undefined: " + str(gl["log"]["undefined"][:20]) + "\n"
                "Also read " + P("main.log") + " around the first '!' error. Do NOT run build_paper.py yourself; the workflow rebuilds. Finish with fixed=true if you made fixes."
            )
            try:
                fx = await agent(fixer, schema=BUILD_FIX_SCHEMA, role="Build fixer")
                log("fixer:", fx["summary"][:200])
            except Exception as exc:
                log("fixer failed:", str(exc)[:200])
                break

    cmp_code, cmp_out = sh([sys.executable, AUDIT_PY, "--compare", PRE, POST], 120)

    # report
    L = ["# Manuscript Audit and Sweep Report", "", "- Run: " + RUN_ID + " | mode: " + MODE + " | slice_kb: " + str(SLICE_KB),
         "- Units: " + ", ".join(u[0] for u in units), "", "## Slice results", "",
         "| Unit | File | Lines | Edits (rule x count) | Flags | Summary |", "| :-- | :-- | :-- | :-- | --: | :-- |"]
    for r in results:
        ed = "; ".join("%s x%s" % (e["rule"], e["count"]) for e in r["edits"]) or "-"
        L.append("| %s | %s | %s | %s | %d | %s |" % (r["unit"], r["file"], r["range"], ed.replace("|", "/"), len(r["flags"]), r["summary"].replace("|", "/").replace("\n", " ")))
    L += ["", "## Items needing a human decision", ""]
    for kind in ("CITE", "DATA", "CONSISTENCY", "HUMAN"):
        items = [(r["unit"], r["range"], f) for r in results for f in r["flags"] if f["kind"] == kind]
        L.append("### " + kind + " (" + str(len(items)) + ")")
        L += ["- [%s %s] %s: %s" % (u, rg, f["where"], f["note"]) for u, rg, f in items] or ["- none"]
        L.append("")
    L += ["## Phase 1 cross-chapter findings", ""]
    L += ["- [%s] %s%s: %s" % (x["severity"], x["file"], (":" + str(x["line"])) if x.get("line") else "", x["note"]) for x in findings] or ["- none"]
    L += ["", "## Candidate-defect counts before vs after (deterministic audit)", "", "```", cmp_out.strip(), "```", "", "## Build", "",
          "```json", json.dumps(build_info, indent=1)[:2500], "```", ""]
    report = "\n".join(L)
    with open(os.path.join(REPO, OUT, "report.md"), "w", encoding="utf-8") as f:
        f.write(report)
    with open(os.path.join(REPO, "output", "paper_sweep_report.md"), "w", encoding="utf-8") as f:
        f.write(report)
    log("report written:", OUT + "/report.md", "and output/paper_sweep_report.md")
    print(json.dumps({"out": OUT, "report": "output/paper_sweep_report.md", "slices": len(results),
                      "flags": sum(len(r["flags"]) for r in results), "build": build_info.get("exit")}))
