#!/usr/bin/env python3
"""
scripts/audit_refs.py
Comprehensive Bibliography Auditor and Reference Downloader for Legal NLP Thesis.

Functions:
1. Parses references.bib into structured JSON records.
2. Scans LaTeX files across CS_Undergraduate_Thesis_Template/ to detect in-text citations.
3. Automatically derives research query links (Google, Google Scholar, Semantic Scholar, Crossref, Lawphil).
4. Auto-resolves direct PDF URLs (arXiv, ACL Anthology, Open-Access DOIs, Direct links).
5. Checks local PDF storage in docs/references/<citekey>.pdf.
6. Generates docs/references_data.json and docs/references_data.js for interactive dashboard.
7. Optional --download flag to automatically fetch available open-access PDFs.
"""

import os
import re
import sys
import json
import glob
import time
import shutil
import webbrowser
import http.server
import urllib.parse
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
BIB_FILE = REPO_ROOT / "CS_Undergraduate_Thesis_Template" / "references.bib"
TEX_DIR = REPO_ROOT / "CS_Undergraduate_Thesis_Template"
DOCS_DIR = REPO_ROOT / "docs"
REFS_DIR = DOCS_DIR / "references"
JSON_OUT = DOCS_DIR / "references_data.json"
JS_OUT = DOCS_DIR / "references_data.js"


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

        # Clean value: unwrap LaTeX artifacts, double spaces, and braces
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

        # Look for \cite, \citep, \citet, \citealp, etc.
        for match in re.finditer(r'\\cite[a-zA-Z]*\*?\{([^}]+)\}', content):
            keys = [k.strip() for k in match.group(1).split(',') if k.strip()]
            for k in keys:
                if k not in citation_map:
                    citation_map[k] = {"count": 0, "files": set()}
                citation_map[k]["count"] += 1
                citation_map[k]["files"].add(rel_path)

    # Convert sets to sorted lists
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
    """Attempt to derive direct PDF link."""
    # 1. Direct eprint (arXiv)
    eprint = fields.get("eprint", "").strip()
    if eprint and (re.match(r'^\d{4}\.\d{4,5}(v\d+)?$', eprint) or 'arxiv' in eprint.lower()):
        clean_ep = re.sub(r'^arxiv:\s*', '', eprint, flags=re.IGNORECASE)
        return f"https://arxiv.org/pdf/{clean_ep}.pdf"

    # 2. Existing URL
    url = fields.get("url", "").strip()
    if url:
        if url.endswith(".pdf"):
            return url
        if "arxiv.org/abs/" in url:
            return url.replace("arxiv.org/abs/", "arxiv.org/pdf/") + ".pdf"
        if "aclanthology.org/" in url:
            clean_acl = url.rstrip("/")
            if not clean_acl.endswith(".pdf"):
                return f"{clean_acl}.pdf"
            return clean_acl

    return ""


def build_reference_records():
    """Main builder that integrates bib entries, latex citations, and search links."""
    REFS_DIR.mkdir(parents=True, exist_ok=True)

    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        bib_text = f.read()

    entries = parse_bib_entries(bib_text)
    citation_map = scan_latex_citations()

    records = []
    # Check for local pdf files in docs/references/
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

        # In-text citation status
        cite_info = citation_map.get(ck, {"count": 0, "files": []})
        is_cited = cite_info["count"] > 0

        # Category
        category = categorize_reference(ck, flds, etype)

        # Direct PDF
        direct_pdf = resolve_pdf_url(flds)

        # Local PDF check
        has_local_pdf = ck.lower() in local_files
        local_pdf_path = f"docs/references/{ck}.pdf" if has_local_pdf else ""

        # Search Query URLs
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

    # JavaScript bundle for direct file:// browser loading without CORS issues
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


def download_open_access(records):
    """Attempt download of direct PDF links for references."""
    import urllib.request

    print("Beginning automated download of open-access PDFs...")
    downloadable = [r for r in records if r["direct_pdf_url"] and not r["has_local_pdf"]]
    print(f"Found {len(downloadable)} candidate open-access references with direct PDF links.\n")

    success_count = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ThesisRefAuditor/1.0'}

    for idx, r in enumerate(downloadable[:20]): # Download initial batch of up to 20
        ck = r["citekey"]
        url = r["direct_pdf_url"]
        target = REFS_DIR / f"{ck}.pdf"
        print(f"[{idx+1}/{min(len(downloadable), 20)}] Downloading {ck} from {url}...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    with open(target, 'wb') as f_out:
                        f_out.write(resp.read())
                    print(f"     -> Saved to {target.name} ({target.stat().st_size // 1024} KB)")
                    success_count += 1
                else:
                    print(f"     -> HTTP {resp.status}")
        except Exception as e:
            print(f"     -> Failed: {e}")

    print(f"\n[DONE] Successfully downloaded {success_count} PDFs to {REFS_DIR}.")


class RefAuditorHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler serving repository files and providing API endpoints for reference verification."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(REPO_ROOT), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/status":
            local_pdfs = [f.stem for f in REFS_DIR.glob("*.pdf")]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            resp = {"status": "ok", "downloaded_citekeys": local_pdfs}
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/save_pdf":
            query = urllib.parse.parse_qs(parsed.query)
            citekey = query.get("citekey", [""])[0]
            if not citekey:
                self.send_error(400, "Missing citekey query parameter")
                return

            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length)

            content_type = self.headers.get("Content-Type", "")
            pdf_bytes = raw_body

            # Extract from multipart/form-data if browser used FormData
            if "multipart/form-data" in content_type:
                boundary = content_type.split("boundary=")[1].strip().encode()
                parts = raw_body.split(b"--" + boundary)
                for part in parts:
                    if b"filename=" in part and b"\r\n\r\n" in part:
                        hdr_end = part.find(b"\r\n\r\n")
                        pdf_bytes = part[hdr_end + 4:].rstrip(b"\r\n")
                        break

            target_file = REFS_DIR / f"{citekey}.pdf"
            with open(target_file, "wb") as f:
                f.write(pdf_bytes)

            print(f"[SERVER] Saved PDF for {citekey} -> {target_file.name} ({len(pdf_bytes) // 1024} KB)")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "saved", "citekey": citekey, "size": len(pdf_bytes)}).encode("utf-8"))
            return

        elif parsed.path == "/api/save_bib":
            content_length = int(self.headers.get("Content-Length", 0))
            bib_text = self.rfile.read(content_length).decode("utf-8")

            # Create backup
            backup_file = BIB_FILE.parent / f"references_backup_{int(time.time())}.bib"
            if BIB_FILE.exists():
                shutil.copy2(BIB_FILE, backup_file)

            with open(BIB_FILE, "w", encoding="utf-8") as f:
                f.write(bib_text)

            print(f"[SERVER] Updated {BIB_FILE} (Backup: {backup_file.name})")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b'{"status": "bib_updated"}')
            return

        self.send_error(404, "API endpoint not found")


def run_server(port=8080):
    """Run local HTTP server for interactive dashboard with zero-prompt direct disk saving."""
    server_address = ("127.0.0.1", port)
    try:
        httpd = http.server.HTTPServer(server_address, RefAuditorHandler)
    except OSError:
        # Port fallback
        port = 8081
        server_address = ("127.0.0.1", port)
        httpd = http.server.HTTPServer(server_address, RefAuditorHandler)

    url = f"http://127.0.0.1:{port}/docs/ref_auditor.html"
    print(f"\n=======================================================")
    print(f"   BIBLIOGRAPHY AUDITOR LOCAL SERVER RUNNING          ")
    print(f"=======================================================")
    print(f" Local URL: {url}")
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

    if "--download" in sys.argv:
        download_open_access(records)

    if "--serve" in sys.argv:
        run_server()


if __name__ == "__main__":
    main()

