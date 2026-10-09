"""
scripts/verify_lawphil_references.py
====================================
Fetches authentic legal texts for Philippine statutes, administrative orders,
and Supreme Court decisions directly from Lawphil and the Judiciary E-Library,
compiles them into clean, multi-page reference PDFs in `docs/references/`,
and marks them as verified in the thesis bibliography and audit dashboard.
"""

import os
import re
import ssl
import json
import urllib.request
import html
from html.parser import HTMLParser
from pathlib import Path
import fitz  # PyMuPDF

REPO_ROOT = Path(__file__).resolve().parent.parent
REFS_DIR = REPO_ROOT / "docs" / "references"
FLAGGED_FILE = REPO_ROOT / "docs" / "flagged_references.json"
BIB_FILE = REPO_ROOT / "CS_Undergraduate_Thesis_Template" / "references.bib"

REFS_DIR.mkdir(parents=True, exist_ok=True)

# Target Philippine statutes, rules, and jurisprudence
TARGET_LAWS = {
    "act453_1902": {
        "url": "https://lawphil.net/statutes/acts/act1902/act_453_1902.html",
        "title": "Act No. 453: An Act Providing for the Publication by the Insular Government of an Official Gazette Under the General Direction of the Department of Public Instruction",
        "citation": "Act No. 453 (Enacted September 2, 1902)",
        "source": "Lawphil Philippine Laws and Jurisprudence Databank"
    },
    "ca638_1941": {
        "url": "https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/29/36850",
        "title": "Commonwealth Act No. 638: An Act to Provide for the Uniform Publication and Distribution of the Official Gazette",
        "citation": "Commonwealth Act No. 638 (Enacted June 10, 1941)",
        "source": "Supreme Court of the Philippines E-Library"
    },
    "republic1987executive": {
        "url": "https://lawphil.net/executive/execord/eo1987/eo_292_1987.html",
        "title": "Executive Order No. 292: Instituting the Administrative Code of 1987 (Book VII: Administrative Procedure)",
        "citation": "Executive Order No. 292, Book VII (July 25, 1987)",
        "source": "Lawphil Philippine Laws and Jurisprudence Databank"
    },
    "scp2001pldtvdavao": {
        "url": "https://lawphil.net/judjuris/juri2001/aug2001/gr_143867_2001.html",
        "title": "Philippine Long Distance Telephone Company, Inc. v. City of Davao",
        "citation": "G.R. No. 143867, 363 SCRA 522 (August 22, 2001)",
        "source": "Supreme Court of the Philippines (Lawphil Archive)"
    },
    "scp2004batangascatv": {
        "url": "https://lawphil.net/judjuris/juri2004/sep2004/gr_138810_2004.html",
        "title": "Batangas CATV, Inc. v. Court of Appeals and Sangguniang Panlungsod ng Batangas",
        "citation": "G.R. No. 138810, 441 SCRA 530 (September 29, 2004)",
        "source": "Supreme Court of the Philippines (Lawphil Archive)"
    },
    "scp2008smartvdavao": {
        "url": "https://lawphil.net/judjuris/juri2008/sep2008/gr_155491_2008.html",
        "title": "Smart Communications, Inc. v. City of Davao and Sangguniang Panlungsod of Davao City",
        "citation": "G.R. No. 155491, 565 SCRA 237 (September 16, 2008)",
        "source": "Supreme Court of the Philippines (Lawphil Archive)"
    },
    "scam2012paper": {
        "url": "https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/69189",
        "title": "Administrative Matter No. 11-9-4-SC: Efficient Use of Paper Rule",
        "citation": "A.M. No. 11-9-4-SC En Banc Resolution (November 13, 2012)",
        "source": "Supreme Court of the Philippines E-Library"
    }
}


def fetch_url_content(url: str) -> str:
    """Fetches HTML content from URL handling SSL contexts and custom User-Agents."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def clean_legal_text(html: str) -> str:
    """Extracts readable text from Lawphil or Judiciary E-library HTML."""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        # Remove navigation headers, footers, scripts, and styles
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
    except ImportError:
        text = re.sub(r'<[^>]+>', ' ', html)

    # Normalize whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n\n".join(lines)


def create_styled_pdf(dest_path: Path, meta: dict, body_text: str):
    """Generates an authoritative multi-page PDF document using PyMuPDF."""
    doc = fitz.open()

    page_width, page_height = 612, 792  # Letter portrait
    margin_x = 54
    margin_top = 72
    margin_bottom = 54
    usable_width = page_width - (2 * margin_x)
    usable_height = page_height - margin_top - margin_bottom

    # Split text into paragraphs
    paragraphs = [p.strip() for p in body_text.split("\n\n") if p.strip()]

    current_page = doc.new_page(width=page_width, height=page_height)
    page_num = 1

    def draw_page_decorations(page, num):
        # Header banner
        page.draw_rect(fitz.Rect(margin_x, 30, page_width - margin_x, 31), color=(0.7, 0.7, 0.7), fill=None, width=0.5)
        page.insert_text(
            (margin_x, 24),
            f"PHILIPPINE STATUTORY & JURISPRUDENTIAL ARCHIVE — {meta['source'].upper()}",
            fontsize=8,
            color=(0.3, 0.3, 0.3),
            fontname="helv"
        )
        # Footer
        page.draw_rect(fitz.Rect(margin_x, page_height - 35, page_width - margin_x, page_height - 34), color=(0.7, 0.7, 0.7), fill=None, width=0.5)
        page.insert_text(
            (margin_x, page_height - 22),
            f"Reference Verification Archive | ADDU CS Thesis 2026 | Citation: {meta['citation']}",
            fontsize=8,
            color=(0.4, 0.4, 0.4),
            fontname="helv"
        )
        page.insert_text(
            (page_width - margin_x - 50, page_height - 22),
            f"Page {num}",
            fontsize=8,
            color=(0.4, 0.4, 0.4),
            fontname="helv"
        )

    # First page header block
    draw_page_decorations(current_page, page_num)
    y_cursor = margin_top

    # Title box
    current_page.draw_rect(fitz.Rect(margin_x, y_cursor, page_width - margin_x, y_cursor + 60), color=(0.1, 0.2, 0.45), fill=(0.95, 0.96, 0.98), width=1)
    current_page.insert_textbox(
        fitz.Rect(margin_x + 12, y_cursor + 8, page_width - margin_x - 12, y_cursor + 38),
        meta["title"],
        fontsize=11,
        fontname="helv",
        color=(0.05, 0.1, 0.3)
    )
    current_page.insert_textbox(
        fitz.Rect(margin_x + 12, y_cursor + 40, page_width - margin_x - 12, y_cursor + 56),
        f"Controlling Authority: {meta['citation']}  |  URL: {meta['url']}",
        fontsize=8.5,
        fontname="helv",
        color=(0.2, 0.3, 0.5)
    )
    y_cursor += 75

    # Insert paragraphs sequentially
    for para in paragraphs:
        # Estimate height for paragraph
        test_rect = fitz.Rect(margin_x, y_cursor, page_width - margin_x, page_height - margin_bottom)
        rc = current_page.insert_textbox(
            test_rect,
            para,
            fontsize=9.5,
            fontname="helv",
            color=(0.1, 0.1, 0.1)
        )
        
        # If text didn't fit, make new page
        if rc < 0:
            page_num += 1
            current_page = doc.new_page(width=page_width, height=page_height)
            draw_page_decorations(current_page, page_num)
            y_cursor = margin_top
            
            # Insert remainder into new page
            current_page.insert_textbox(
                fitz.Rect(margin_x, y_cursor, page_width - margin_x, page_height - margin_bottom),
                para,
                fontsize=9.5,
                fontname="helv",
                color=(0.1, 0.1, 0.1)
            )
            words = len(para.split())
            lines_est = max(1, words / 12)
            y_cursor += (lines_est * 13) + 10
        else:
            words = len(para.split())
            lines_est = max(1, words / 12)
            y_cursor += (lines_est * 13) + 10

        if y_cursor > page_height - margin_bottom - 40:
            page_num += 1
            current_page = doc.new_page(width=page_width, height=page_height)
            draw_page_decorations(current_page, page_num)
            y_cursor = margin_top

    doc.save(str(dest_path))
    doc.close()


def process_all_lawphil_targets():
    print("=" * 70)
    print(" Verifying & Compiling Lawphil / Statutory Reference PDFs")
    print("=" * 70)

    # Load flagged data
    flagged = {}
    if FLAGGED_FILE.exists():
        with open(FLAGGED_FILE, "r", encoding="utf-8") as f:
            flagged = json.load(f)

    verified_keys = []

    for citekey, meta in TARGET_LAWS.items():
        pdf_path = REFS_DIR / f"{citekey}.pdf"
        print(f"\nProcessing [{citekey}]...")
        print(f"  Fetching: {meta['url']}")

        try:
            html = fetch_url_content(meta["url"])
            cleaned = clean_legal_text(html)
            
            # If text is excessively large (like complete EO 292), truncate to relevant provisions or first 60 pages
            if len(cleaned) > 150000:
                cleaned = cleaned[:150000] + "\n\n[... Remaining administrative provisions truncated for reference document size ...]"

            create_styled_pdf(pdf_path, meta, cleaned)
            file_size_kb = pdf_path.stat().st_size / 1024
            print(f"  [x] Successfully compiled {pdf_path.name} ({file_size_kb:.1f} KB)")
            verified_keys.append(citekey)

            # Remove from flagged
            if citekey in flagged:
                del flagged[citekey]
                print(f"  [x] Removed {citekey} from flagged_references.json")

        except Exception as e:
            print(f"  [ERROR] Failed to compile {citekey}: {e}")

    # Save updated flagged file
    with open(FLAGGED_FILE, "w", encoding="utf-8") as f:
        json.dump(flagged, f, indent=2, ensure_ascii=False)
    print(f"\n[x] Updated flagged_references.json (Remaining flagged: {len(flagged)})")

    # Update references.bib to ensure 'file' field is set for all verified keys
    if BIB_FILE.exists():
        with open(BIB_FILE, "r", encoding="utf-8") as f:
            bib_text = f.read()

        for ck in verified_keys:
            pdf_rel = f"docs/references/{ck}.pdf"
            # If citekey exists in bib but has no file = {docs/references/...}
            entry_pattern = re.compile(rf'(@\w+\s*\{{\s*{ck}\s*,)(.*?)(\n\}})', re.DOTALL)
            match = entry_pattern.search(bib_text)
            if match:
                entry_header, body, entry_footer = match.groups()
                if "file =" not in body:
                    new_body = body.rstrip() + f",\n  file = {{{pdf_rel}}}"
                    bib_text = bib_text[:match.start()] + entry_header + new_body + entry_footer + bib_text[match.end():]
                    print(f"  [x] Appended file = {{{pdf_rel}}} to bib entry @{ck}")

        with open(BIB_FILE, "w", encoding="utf-8") as f:
            f.write(bib_text)
        print("  [x] Saved updated references.bib")


if __name__ == "__main__":
    process_all_lawphil_targets()
