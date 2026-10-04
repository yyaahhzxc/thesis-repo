#!/usr/bin/env python3
"""
scripts/audit_refs.py
Comprehensive Bibliography Auditor, Open-Access Downloader, and Reference Server for Legal NLP Thesis.

Functions:
1. Parses references.bib into structured JSON records.
2. Scans LaTeX files across CS_Undergraduate_Thesis_Template/ to detect in-text citations.
3. Automatically derives research query links (Google, Google Scholar, Semantic Scholar, Crossref, Lawphil).
4. Auto-resolves direct PDF URLs (arXiv, ACL Anthology, JMLR, NeurIPS, Open-Access DOIs, Direct links).
5. Checks local PDF storage in docs/references/<citekey>.pdf.
6. Generates docs/references_data.json and docs/references_data.js for interactive dashboard.
7. Automated batch downloader validating HTTP 200, length, and %PDF- magic bytes.
8. Integrated open-access resolver querying arXiv API by paper title.
9. Local HTTP API server supporting live UI interaction, 1-click downloads, and progress streaming.
"""

import os
import re
import sys
import json
import glob
import time
import shutil

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import difflib
import threading
import webbrowser
import http.server
import urllib.parse
import urllib.request
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
BIB_FILE = REPO_ROOT / "CS_Undergraduate_Thesis_Template" / "references.bib"
TEX_DIR = REPO_ROOT / "CS_Undergraduate_Thesis_Template"
DOCS_DIR = REPO_ROOT / "docs"
REFS_DIR = DOCS_DIR / "references"
JSON_OUT = DOCS_DIR / "references_data.json"
JS_OUT = DOCS_DIR / "references_data.js"
FLAGGED_FILE = DOCS_DIR / "flagged_references.json"

# Global Download State for Background Streaming
DOWNLOAD_STATE = {
    "active": False,
    "total": 0,
    "current": 0,
    "current_key": "",
    "downloaded": 0,
    "failed": 0,
    "skipped": 0,
    "message": "Idle",
    "logs": []
}


def load_flagged_references() -> dict:
    """Load dictionary of flagged references from disk."""
    if FLAGGED_FILE.exists():
        try:
            with open(FLAGGED_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_flagged_references(data: dict):
    """Save dictionary of flagged references to disk."""
    FLAGGED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(FLAGGED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def parse_bib_entries(bib_text: str):
    """Robust state-machine parser for BibTeX files handling nested braces and strings."""
    entries = []
    i = 0
    n = len(bib_text)

    while i < n:
        at = bib_text.find('@', i)
        if at == -1:
            break
        brace = bib_text.find('{', at)
        if brace == -1:
            break
        entry_type = bib_text[at + 1:brace].strip().lower()

        # Find matching closing brace
        depth = 1
        j = brace + 1
        while j < n and depth > 0:
            if bib_text[j] == '{':
                depth += 1
            elif bib_text[j] == '}':
                depth -= 1
            j += 1

        body = bib_text[brace + 1:j - 1]
        first_comma = body.find(',')
        if first_comma != -1:
            key = body[:first_comma].strip()
            fields_str = body[first_comma + 1:]
            fields = parse_fields(fields_str)
            raw_bib = bib_text[at:j]
            entries.append({
                "entry_type": entry_type,
                "citekey": key,
                "fields": fields,
                "raw_bib": raw_bib
            })
        i = j

    return entries


def parse_fields(fields_str: str):
    """Extract key-value pairs from BibTeX fields string."""
    fields = {}
    i = 0
    n = len(fields_str)

    while i < n:
        eq = fields_str.find('=', i)
        if eq == -1:
            break
        name = fields_str[i:eq].strip().lower()
        name = re.sub(r'^[,\s]+', '', name)

        j = eq + 1
        while j < n and fields_str[j].isspace():
            j += 1
        if j >= n:
            break

        val = ''
        if fields_str[j] == '{':
            depth = 1
            k = j + 1
            while k < n and depth > 0:
                if fields_str[k] == '{':
                    depth += 1
                elif fields_str[k] == '}':
                    depth -= 1
                k += 1
            val = fields_str[j + 1:k - 1].strip()
            i = k
        elif fields_str[j] == '"':
            k = j + 1
            while k < n and fields_str[k] != '"':
                if fields_str[k] == '\\':
                    k += 1
                k += 1
            val = fields_str[j + 1:k].strip()
            i = k + 1
        else:
            comma = fields_str.find(',', j)
            if comma == -1:
                val = fields_str[j:].strip()
                i = n
            else:
                val = fields_str[j:comma].strip()
                i = comma + 1

        cleaned_val = re.sub(r'\s+', ' ', val).strip()
        if name:
            fields[name] = cleaned_val

    return fields


def scan_latex_citations():
    """Scan all .tex files and map citekeys to file locations and counts."""
    citation_map = {}
    tex_files = list(TEX_DIR.glob("**/*.tex"))

    for tf in tex_files:
        rel_path = tf.relative_to(REPO_ROOT).as_posix()
        try:
            with open(tf, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        for match in re.finditer(r'\\cite[a-zA-Z]*\*?\{([^}]+)\}', content):
            keys = [k.strip() for k in match.group(1).split(',') if k.strip()]
            for k in keys:
                if k not in citation_map:
                    citation_map[k] = {"count": 0, "files": set()}
                citation_map[k]["count"] += 1
                citation_map[k]["files"].add(rel_path)

    for k in citation_map:
        citation_map[k]["files"] = sorted(list(citation_map[k]["files"]))

    return citation_map


def clean_latex_markup(text: str) -> str:
    """Remove LaTeX formatting tags like \\textbf, \\textit, { }, etc."""
    if not text:
        return ""
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
    text = re.sub(r'[\{\}\\]', '', text)
    text = re.sub(r'~', ' ', text)
    text = re.sub(r'\\S', '§', text)
    return text.strip()


def categorize_reference(citekey: str, fields: dict, entry_type: str) -> str:
    """Determine domain category for filtering."""
    ck = citekey.lower()
    kw = fields.get("keywords", "").lower()
    title = fields.get("title", "").lower()
    hp = fields.get("howpublished", "").lower()

    if any(k in ck for k in ["scp", "scam", "ra", "pd", "eo", "act", "ca638", "philgov", "spdavao"]) or \
       any(k in kw for k in ["jurisprudence", "ordinance", "court_rule", "republic_act"]) or \
       "supreme court" in hp or "republic act" in title or "ordinance" in title:
        return "Philippine Law & Jurisprudence"

    if any(k in ck for k in ["mcnemar", "friedman", "fleiss", "cohen", "landis", "vabalas", "card2020", "demsar"]):
        return "Statistical & Evaluation Methods"

    if any(k in ck for k in ["davao", "lgu", "sangguniang", "motiong", "zuasola", "andaya"]):
        return "Local Governance & Field Study"

    return "Computer Science & NLP"


def resolve_pdf_url(fields: dict) -> str:
    """Attempt to derive direct PDF link from BibTeX fields."""
    # 1. Direct eprint (arXiv)
    eprint = fields.get("eprint", "").strip()
    if eprint and (re.match(r'^\d{4}\.\d{4,5}(v\d+)?$', eprint) or 'arxiv' in eprint.lower()):
        clean_ep = re.sub(r'^arxiv:\s*', '', eprint, flags=re.IGNORECASE)
        clean_ep = re.sub(r'v\d+$', '', clean_ep)
        return f"https://arxiv.org/pdf/{clean_ep}.pdf"

    # 2. Existing URL
    url = fields.get("url", "").strip()
    if url:
        if url.endswith(".pdf"):
            return url
        if "arxiv.org/abs/" in url:
            clean = re.sub(r'v\d+$', '', url.replace("arxiv.org/abs/", "arxiv.org/pdf/"))
            return f"{clean}.pdf" if not clean.endswith(".pdf") else clean
        if "aclanthology.org/" in url:
            clean_acl = url.rstrip("/")
            if not clean_acl.endswith(".pdf"):
                return f"{clean_acl}.pdf"
            return clean_acl
        if "jmlr.org/papers/v" in url:
            m = re.search(r'jmlr\.org/papers/v(\d+)/([^/]+)\.html', url)
            if m:
                vol, name = m.group(1), m.group(2)
                return f"https://www.jmlr.org/papers/volume{vol}/{name}/{name}.pdf"
        if "proceedings.neurips.cc/paper_files/paper/" in url and "-Abstract-Conference.html" in url:
            return url.replace("-Abstract-Conference.html", "-Paper-Conference.pdf").replace("/paper_files/paper/", "/paper_files/paper/").replace("/hash/", "/file/")

    return ""


def build_reference_records():
    """Main builder that integrates bib entries, latex citations, and search links."""
    REFS_DIR.mkdir(parents=True, exist_ok=True)

    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        bib_text = f.read()

    entries = parse_bib_entries(bib_text)
    citation_map = scan_latex_citations()
    flagged_data = load_flagged_references()

    records = []
    local_files = set(f.stem.lower() for f in REFS_DIR.glob("*.pdf"))

    for ent in entries:
        ck = ent["citekey"]
        flds = ent["fields"]
        etype = ent["entry_type"]

        raw_title = flds.get("title", "")
        clean_title = clean_latex_markup(raw_title)

        raw_author = flds.get("author", "")
        clean_author = clean_latex_markup(raw_author)

        year = flds.get("year", "")
        clean_year = re.sub(r'[^\d]', '', year)[:4] if year else ""

        venue = flds.get("journal") or flds.get("booktitle") or flds.get("publisher") or flds.get("howpublished") or flds.get("institution") or ""
        clean_venue = clean_latex_markup(venue)

        doi = flds.get("doi", "").strip()
        url = flds.get("url", "").strip()
        eprint = flds.get("eprint", "").strip()

        cite_info = citation_map.get(ck, {"count": 0, "files": []})
        is_cited = cite_info["count"] > 0

        category = categorize_reference(ck, flds, etype)
        direct_pdf = resolve_pdf_url(flds)

        has_local_pdf = ck.lower() in local_files
        local_pdf_path = f"docs/references/{ck}.pdf" if has_local_pdf else ""

        ck_flag = flagged_data.get(ck.lower())
        is_flagged = ck_flag is not None
        flag_reason = ck_flag.get("reason", "") if ck_flag else ""
        flag_timestamp = ck_flag.get("timestamp", "") if ck_flag else ""

        q_author = clean_author.split(" and ")[0] if clean_author else ""
        google_query = f'"{clean_title}" {q_author}'.strip()
        google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(google_query)}"
        google_scholar_url = f"https://scholar.google.com/scholar?q={urllib.parse.quote(clean_title)}"
        semantic_scholar_url = f"https://www.semanticscholar.org/search?q={urllib.parse.quote(clean_title)}"
        crossref_search_url = f"https://api.crossref.org/works?query.title={urllib.parse.quote(clean_title)}&rows=1"

        lawphil_url = ""
        if category == "Philippine Law & Jurisprudence":
            lawphil_url = f"https://www.google.com/search?q=site%3Alawphil.net+{urllib.parse.quote(clean_title)}"

        records.append({
            "citekey": ck,
            "entry_type": etype,
            "title": clean_title,
            "raw_title": raw_title,
            "author": clean_author,
            "raw_author": raw_author,
            "year": clean_year,
            "venue": clean_venue,
            "category": category,
            "doi": doi,
            "url": url,
            "eprint": eprint,
            "direct_pdf_url": direct_pdf,
            "is_cited": is_cited,
            "citation_count": cite_info["count"],
            "cited_in_files": cite_info["files"],
            "has_local_pdf": has_local_pdf,
            "local_pdf_path": local_pdf_path,
            "flagged": is_flagged,
            "flag_reason": flag_reason,
            "flag_timestamp": flag_timestamp,
            "google_search_url": google_search_url,
            "google_scholar_url": google_scholar_url,
            "semantic_scholar_url": semantic_scholar_url,
            "crossref_search_url": crossref_search_url,
            "lawphil_url": lawphil_url,
            "raw_bib": ent["raw_bib"]
        })

    return records


def export_data(records):
    """Write records to JSON and JS."""
    with open(JSON_OUT, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    js_content = f"// System generated references dataset\nwindow.REFERENCES_DATA = {json.dumps(records, indent=2, ensure_ascii=False)};\n"
    with open(JS_OUT, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"[OK] Exported {len(records)} reference records to:")
    print(f"     - {JSON_OUT}")
    print(f"     - {JS_OUT}")


def audit_summary(records):
    """Print console summary metrics."""
    total = len(records)
    cited = sum(1 for r in records if r["is_cited"])
    has_url = sum(1 for r in records if r["url"] or r["doi"] or r["direct_pdf_url"])
    has_pdf = sum(1 for r in records if r["direct_pdf_url"])
    local_cached = sum(1 for r in records if r["has_local_pdf"])

    print("\n=======================================================")
    print("      BIBLIOGRAPHY AUDIT & VERIFICATION REPORT         ")
    print("=======================================================")
    print(f" Total Entries in references.bib:    {total}")
    print(f" Actively Cited in Thesis LaTeX:     {cited} ({cited/total*100:.1f}%)")
    print(f" Entries with Recorded Link/URL:     {has_url} ({has_url/total*100:.1f}%)")
    print(f" Open-Access Direct PDF Resolvable:  {has_pdf} ({has_pdf/total*100:.1f}%)")
    print(f" Locally Downloaded to docs/refs/:   {local_cached} ({local_cached/total*100:.1f}%)")
    print("=======================================================\n")


def inject_bib_file_link(citekey: str, rel_path: str):
    """Update references.bib to include file = {<rel_path>} for the given citekey."""
    if not BIB_FILE.exists():
        return
    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        text = f.read()

    pattern = rf'(@\w+\s*\{{\s*{re.escape(citekey)}\s*,[\s\S]*?\n\}})'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        entry = match.group(1)
        cleaned = re.sub(r',\s*file\s*=\s*(?:\{[^{}]*\}|"[^"]*"|[^\s,}]+)', '', entry, flags=re.IGNORECASE)
        last_brace = cleaned.rfind('}')
        if last_brace != -1:
            base = cleaned[:last_brace].rstrip()
            if base.endswith(','):
                base = base[:-1]
            updated_entry = f"{base},\n  file = {{{rel_path}}}\n}}"
            new_text = text[:match.start()] + updated_entry + text[match.end():]
            with open(BIB_FILE, 'w', encoding='utf-8') as f:
                f.write(new_text)


def download_single_pdf(citekey: str, url: str, target_dir: Path = REFS_DIR, timeout: int = 25) -> dict:
    """Download a single PDF with proper headers, validation, and BibTeX file injection."""
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{citekey}.pdf"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'application/pdf,application/xhtml+xml,text/html;q=0.9,*/*;q=0.8'
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return {"success": False, "error": f"HTTP {resp.status}", "citekey": citekey}

            content = resp.read()
            if len(content) < 1000:
                return {"success": False, "error": "File too small (<1 KB)", "citekey": citekey}

            if b"%PDF-" not in content[:1024]:
                return {"success": False, "error": "Invalid magic bytes (not a PDF file)", "citekey": citekey}

            with open(target, "wb") as f_out:
                f_out.write(content)

            rel_path = f"docs/references/{citekey}.pdf"
            inject_bib_file_link(citekey, rel_path)

            return {
                "success": True,
                "citekey": citekey,
                "size": len(content),
                "path": str(target),
                "rel_path": rel_path
            }
    except Exception as e:
        return {"success": False, "error": str(e), "citekey": citekey}


def batch_download_all_oa(records=None, limit=None, delay=0.4, state_dict=None):
    """Batch download all available open-access PDFs, update BibTeX, and export datasets."""
    global DOWNLOAD_STATE
    if state_dict is None:
        state_dict = DOWNLOAD_STATE

    if records is None:
        records = build_reference_records()

    downloadable = [r for r in records if r["direct_pdf_url"] and not r["has_local_pdf"]]
    total_candidates = len(downloadable) if limit is None else min(len(downloadable), limit)

    state_dict["active"] = True
    state_dict["total"] = total_candidates
    state_dict["current"] = 0
    state_dict["downloaded"] = 0
    state_dict["failed"] = 0
    state_dict["message"] = f"Starting download of {total_candidates} open-access PDFs..."
    state_dict["logs"] = []

    print(f"\n=======================================================")
    print(f"      BATCH DOWNLOADING {total_candidates} OPEN-ACCESS PAPERS      ")
    print(f"=======================================================\n")

    success_count = 0
    fail_count = 0
    total_bytes = 0

    for idx, r in enumerate(downloadable[:total_candidates]):
        ck = r["citekey"]
        url = r["direct_pdf_url"]
        state_dict["current"] = idx + 1
        state_dict["current_key"] = ck
        state_dict["message"] = f"Downloading [{idx+1}/{total_candidates}] {ck}..."

        print(f"[{idx+1}/{total_candidates}] [{ck}] Fetching from {url}...")
        res = download_single_pdf(ck, url)

        if res["success"]:
            size_kb = res["size"] // 1024
            total_bytes += res["size"]
            success_count += 1
            state_dict["downloaded"] = success_count
            log_line = f"[OK] [{ck}] Saved {ck}.pdf ({size_kb:,} KB)"
            print(f"     -> {log_line}")
            state_dict["logs"].append(log_line)
        else:
            fail_count += 1
            state_dict["failed"] = fail_count
            log_line = f"[FAIL] [{ck}] Failed: {res['error']}"
            print(f"     -> {log_line}")
            state_dict["logs"].append(log_line)

        time.sleep(delay)

    state_dict["active"] = False
    state_dict["message"] = f"Finished! Downloaded {success_count} PDFs ({total_bytes // (1024*1024):.1f} MB), {fail_count} failed."
    print(f"\n[DONE] Batch download complete: {success_count} saved, {fail_count} failed.")

    # Re-export fresh datasets and print updated summary
    updated_records = build_reference_records()
    export_data(updated_records)
    audit_summary(updated_records)

    return {
        "total": total_candidates,
        "downloaded": success_count,
        "failed": fail_count,
        "total_bytes": total_bytes
    }


def resolve_open_access_for_entry(citekey: str, title: str, author: str = "", doi: str = "") -> dict:
    """Query arXiv API and Open Access repositories to find matching free PDFs."""
    clean_t = re.sub(r'[{}\\\'\":;,\.\?\!\(\)\[\]]', ' ', title)
    clean_t = re.sub(r'\s+', ' ', clean_t).strip()
    words = clean_t.split()
    query_str = ' '.join(words[:8])

    url = f"http://export.arxiv.org/api/query?search_query=ti:%22{urllib.parse.quote(query_str)}%22&max_results=1"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ThesisRefAuditor/1.0'}

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml = resp.read().decode('utf-8')
            entry_match = re.search(r'<entry>(.*?)</entry>', xml, re.DOTALL)
            if not entry_match:
                return {"found": False, "citekey": citekey}

            entry_xml = entry_match.group(1)
            m_id = re.search(r'<id>http://arxiv.org/abs/([^<]+)</id>', entry_xml)
            m_title = re.search(r'<title>([^<]+)</title>', entry_xml, re.DOTALL)

            if m_id and m_title:
                raw_id = m_id.group(1).strip()
                clean_id = re.sub(r'v\d+$', '', raw_id)
                paper_title = re.sub(r'\s+', ' ', m_title.group(1)).strip()

                sim = difflib.SequenceMatcher(None, clean_t.lower(), paper_title.lower()).ratio()
                if sim >= 0.65 or clean_t.lower() in paper_title.lower() or paper_title.lower() in clean_t.lower():
                    pdf_url = f"https://arxiv.org/pdf/{clean_id}.pdf"
                    abs_url = f"https://arxiv.org/abs/{clean_id}"
                    return {
                        "found": True,
                        "citekey": citekey,
                        "source": "arXiv",
                        "arxiv_id": clean_id,
                        "direct_pdf_url": pdf_url,
                        "abstract_url": abs_url,
                        "matched_title": paper_title,
                        "similarity": round(sim, 2)
                    }
    except Exception as e:
        return {"found": False, "citekey": citekey, "error": str(e)}

    return {"found": False, "citekey": citekey}


def apply_entry_update(citekey: str, new_url: str = None, note: str = None, verified: bool = None):
    """Update fields in references.bib and regenerate data bundles."""
    if not BIB_FILE.exists():
        return False
    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        text = f.read()

    pattern = rf'(@\w+\s*\{{\s*{re.escape(citekey)}\s*,[\s\S]*?\n\}})'
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return False

    entry = match.group(1)
    today = time.strftime('%Y-%m-%d')

    if new_url:
        entry = re.sub(r',\s*url\s*=\s*(?:\{[^{}]*\}|"[^"]*"|[^\s,}]+)', '', entry, flags=re.IGNORECASE)
        entry = re.sub(r',\s*urldate\s*=\s*(?:\{[^{}]*\}|"[^"]*"|[^\s,}]+)', '', entry, flags=re.IGNORECASE)
        last_brace = entry.rfind('}')
        if last_brace != -1:
            base = entry[:last_brace].rstrip()
            if base.endswith(','):
                base = base[:-1]
            entry = f"{base},\n  url = {{{new_url}}},\n  urldate = {{{today}}}\n}}"

    new_text = text[:match.start()] + entry + text[match.end():]
    with open(BIB_FILE, 'w', encoding='utf-8') as f:
        f.write(new_text)

    records = build_reference_records()
    export_data(records)
    return True


class RefAuditorHandler(http.server.SimpleHTTPRequestHandler):
    """Enhanced request handler serving repository files and providing API endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(REPO_ROOT), **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def send_json_error(self, code: int, message: str):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"error": message, "code": code}).encode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # GET /api/status
        if parsed.path == "/api/status":
            records = build_reference_records()
            local_pdfs = [f.stem.lower() for f in REFS_DIR.glob("*.pdf")]
            flagged_data = load_flagged_references()
            resp = {
                "status": "ok",
                "total": len(records),
                "cited": sum(1 for r in records if r["is_cited"]),
                "has_url": sum(1 for r in records if r["url"] or r["doi"] or r["direct_pdf_url"]),
                "has_pdf": sum(1 for r in records if r["direct_pdf_url"]),
                "local_cached": len(local_pdfs),
                "downloaded_citekeys": local_pdfs,
                "total_flagged": len(flagged_data),
                "flagged_citekeys": list(flagged_data.keys()),
                "download_state": DOWNLOAD_STATE
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # GET /api/flagged
        elif parsed.path == "/api/flagged":
            flagged_data = load_flagged_references()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(flagged_data).encode("utf-8"))
            return

        # GET /api/download_progress
        elif parsed.path == "/api/download_progress":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(DOWNLOAD_STATE).encode("utf-8"))
            return

        # GET /api/resolve_oa?citekey=...
        elif parsed.path == "/api/resolve_oa":
            query = urllib.parse.parse_qs(parsed.query)
            citekey = query.get("citekey", [""])[0]
            if not citekey:
                self.send_json_error(400, "Missing citekey parameter")
                return

            records = build_reference_records()
            match = next((r for r in records if r["citekey"].lower() == citekey.lower()), None)
            if not match:
                self.send_json_error(404, "Citekey not found in references.bib")
                return

            res = resolve_open_access_for_entry(
                citekey=match["citekey"],
                title=match["title"],
                author=match["author"],
                doi=match["doi"]
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)

        # POST /api/download_single?citekey=...
        if parsed.path == "/api/download_single":
            query = urllib.parse.parse_qs(parsed.query)
            citekey = query.get("citekey", [""])[0]
            custom_url = query.get("url", [""])[0]

            if not citekey:
                self.send_json_error(400, "Missing citekey parameter")
                return

            records = build_reference_records()
            match = next((r for r in records if r["citekey"].lower() == citekey.lower()), None)
            target_url = custom_url or (match["direct_pdf_url"] if match else "")

            if not target_url:
                self.send_json_error(400, f"No direct PDF URL available for [{citekey}]")
                return

            res = download_single_pdf(citekey, target_url)
            if res["success"]:
                updated_records = build_reference_records()
                export_data(updated_records)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # POST /api/download_all_oa
        elif parsed.path == "/api/download_all_oa":
            if DOWNLOAD_STATE["active"]:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "already_active", "state": DOWNLOAD_STATE}).encode("utf-8"))
                return

            # Launch background worker
            def worker():
                batch_download_all_oa()

            thread = threading.Thread(target=worker, daemon=True)
            thread.start()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "started", "message": "Batch download started in background"}).encode("utf-8"))
            return

        # POST /api/update_entry
        elif parsed.path == "/api/update_entry":
            content_length = int(self.headers.get("Content-Length", 0))
            body_data = json.loads(self.rfile.read(content_length).decode("utf-8"))

            citekey = body_data.get("citekey", "")
            new_url = body_data.get("url", "")
            note = body_data.get("note", "")
            verified = body_data.get("verified", False)

            if not citekey:
                self.send_json_error(400, "Missing citekey in payload")
                return

            success = apply_entry_update(citekey, new_url=new_url, note=note, verified=verified)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok" if success else "failed", "citekey": citekey}).encode("utf-8"))
            return

        # POST /api/save_pdf
        elif parsed.path == "/api/save_pdf":
            query = urllib.parse.parse_qs(parsed.query)
            citekey = query.get("citekey", [""])[0]
            if not citekey:
                self.send_json_error(400, "Missing citekey query parameter")
                return

            content_length = int(self.headers.get("Content-Length", 0))
            if content_length <= 0:
                self.send_json_error(400, "Empty upload body")
                return

            raw_body = self.rfile.read(content_length)
            content_type = self.headers.get("Content-Type", "")
            pdf_bytes = raw_body

            if "multipart/form-data" in content_type:
                # Search for %PDF- signature
                pdf_start = raw_body.find(b"%PDF-")
                if pdf_start != -1:
                    pdf_bytes = raw_body[pdf_start:]
                    boundary_idx = pdf_bytes.rfind(b"\r\n--")
                    if boundary_idx != -1:
                        pdf_bytes = pdf_bytes[:boundary_idx]
                elif "boundary=" in content_type:
                    boundary = content_type.split("boundary=")[1].strip().strip('"').strip("'").encode()
                    parts = raw_body.split(b"--" + boundary)
                    for part in parts:
                        if b"filename=" in part and b"\r\n\r\n" in part:
                            hdr_end = part.find(b"\r\n\r\n")
                            pdf_bytes = part[hdr_end + 4:].rstrip(b"\r\n")
                            break
            else:
                # Raw binary body
                pdf_start = raw_body.find(b"%PDF-")
                if pdf_start != -1:
                    pdf_bytes = raw_body[pdf_start:]
                else:
                    pdf_bytes = raw_body

            # Validate PDF bytes
            if b"%PDF-" not in pdf_bytes[:1024] and len(pdf_bytes) < 300:
                self.send_json_error(400, "Uploaded file is not a valid PDF (%PDF- header not found)")
                return

            REFS_DIR.mkdir(parents=True, exist_ok=True)
            target_file = REFS_DIR / f"{citekey}.pdf"
            with open(target_file, "wb") as f:
                f.write(pdf_bytes)

            rel_path = f"docs/references/{citekey}.pdf"
            inject_bib_file_link(citekey, rel_path)
            export_data(build_reference_records())

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "saved", "citekey": citekey, "size": len(pdf_bytes), "file_path": rel_path}).encode("utf-8"))
            return

        # POST /api/save_bib
        elif parsed.path == "/api/save_bib":
            content_length = int(self.headers.get("Content-Length", 0))
            bib_text = self.rfile.read(content_length).decode("utf-8")

            backup_file = BIB_FILE.parent / f"references_backup_{int(time.time())}.bib"
            if BIB_FILE.exists():
                shutil.copy2(BIB_FILE, backup_file)

            with open(BIB_FILE, "w", encoding="utf-8") as f:
                f.write(bib_text)

            export_data(build_reference_records())

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b'{"status": "bib_updated"}')
            return

        # POST /api/toggle_flag
        elif parsed.path == "/api/toggle_flag":
            content_length = int(self.headers.get("Content-Length", 0))
            payload = {}
            if content_length > 0:
                try:
                    payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
                except Exception:
                    pass

            query = urllib.parse.parse_qs(parsed.query)
            citekey = payload.get("citekey") or query.get("citekey", [""])[0]
            reason = payload.get("reason") or "PDF unobtainable - consider replacing source or revising citing text"
            force_state = payload.get("flagged")

            if not citekey:
                self.send_json_error(400, "Missing citekey parameter")
                return

            flagged_data = load_flagged_references()
            ck_lower = citekey.lower()

            if force_state is not None:
                new_state = bool(force_state)
            else:
                new_state = not (ck_lower in flagged_data)

            if new_state:
                records = build_reference_records()
                matched = next((r for r in records if r["citekey"].lower() == ck_lower), None)
                flagged_data[ck_lower] = {
                    "citekey": citekey,
                    "flagged": True,
                    "title": matched["title"] if matched else "",
                    "author": matched["author"] if matched else "",
                    "year": matched["year"] if matched else "",
                    "cited_in_files": matched["cited_in_files"] if matched else [],
                    "citation_count": matched["citation_count"] if matched else 0,
                    "reason": reason,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                if ck_lower in flagged_data:
                    del flagged_data[ck_lower]

            save_flagged_references(flagged_data)

            # Re-export fresh datasets
            updated_records = build_reference_records()
            export_data(updated_records)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "citekey": citekey,
                "flagged": new_state,
                "reason": reason if new_state else "",
                "total_flagged": len(flagged_data)
            }).encode("utf-8"))
            return

        self.send_json_error(404, "API endpoint not found")


def run_server(port=8080):
    """Run local HTTP server for interactive dashboard with zero-prompt direct disk saving."""
    server_address = ("127.0.0.1", port)
    try:
        httpd = http.server.HTTPServer(server_address, RefAuditorHandler)
    except OSError:
        port = 8081
        server_address = ("127.0.0.1", port)
        httpd = http.server.HTTPServer(server_address, RefAuditorHandler)

    url = f"http://127.0.0.1:{port}/docs/ref_auditor.html"
    print(f"\n=======================================================")
    print(f"   BIBLIOGRAPHY AUDITOR LOCAL SERVER RUNNING          ")
    print(f"=======================================================")
    print(f" Local Dashboard: {url}")
    print(f" Direct PDF Auto-Save: Enabled -> docs/references/<citekey>.pdf")
    print(f" Press Ctrl+C to terminate.")
    print(f"=======================================================\n")

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
        httpd.server_close()


def main():
    records = build_reference_records()
    export_data(records)
    audit_summary(records)

    if "--download-all" in sys.argv:
        batch_download_all_oa(records)

    elif "--download" in sys.argv:
        idx = sys.argv.index("--download")
        if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith("-"):
            target_ck = sys.argv[idx + 1]
            match = next((r for r in records if r["citekey"].lower() == target_ck.lower()), None)
            if match and match["direct_pdf_url"]:
                res = download_single_pdf(match["citekey"], match["direct_pdf_url"])
                print("Download Result:", res)
            else:
                print(f"Could not find direct PDF URL for [{target_ck}].")
        else:
            batch_download_all_oa(records)

    if "--serve" in sys.argv:
        run_server()


if __name__ == "__main__":
    main()
