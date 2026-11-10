"""
sync_full_tier3_revenue_code.py
===============================
Synchronizes the complete unabridged 434-section text of Ordinance No. 0158-05
into:
1. `src/demo/sample_cases/03_arc_investors_holding_tax.json`
2. `src/demo/sample_cases/04_first_meridian_payment_under_protest.json`
3. Copies `03_davao_revenue_code_2005_full.pdf` (129 pages) to the PDF directories:
   - `src/demo/sample_cases/pdf/`
   - `ground_truth/tier3_sc_cases/tier3_landmark_ordinances_pdf/`
   - `data/tier3_landmark_ordinances_pdf/`
"""

import re
import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TXT_SOURCE = REPO_ROOT / "corpus" / "cleaned" / "local" / "cleaned_transcriptions" / "landmark_ordinances" / "Ordinance No. 0158-05.txt"
FULL_PDF_SOURCE = REPO_ROOT / "ground_truth" / "tier3_sc_cases" / "tier3_landmark_ordinances_pdf" / "03_davao_revenue_code_2005_full.pdf"

def extract_all_sections():
    raw_text = TXT_SOURCE.read_text(encoding="utf-8")
    sec_pattern = re.compile(r'(?:^|\n)(?:SECTION|Section|SEC\.)\s+(\d+[A-Za-z]?)\.?\s*([^\n\-\–\—]+)?\s*[\-\–\—\.]?\s*', re.MULTILINE)
    matches = list(sec_pattern.finditer(raw_text))
    
    sections = []
    for idx, m in enumerate(matches):
        sec_num_str = m.group(1)
        sec_title = (m.group(2) or "").strip().rstrip(".-–— ")
        start_pos = m.end()
        end_pos = matches[idx + 1].start() if idx + 1 < len(matches) else len(raw_text)
        body_text = raw_text[start_pos:end_pos].strip()
        
        # Clean page headers / footers
        body_text = re.sub(r'---\s*\[Page\s*\d+\]\s*---', '', body_text)
        body_text = re.sub(r'The 2005 Revenue Code of the City of Davao', '', body_text)
        body_text = re.sub(r'Page\s*\d+', '', body_text)
        body_text = body_text.strip()
        
        sections.append({
            "sec_num": int(sec_num_str) if sec_num_str.isdigit() else sec_num_str,
            "sec_title": sec_title if sec_title else "OPERATIVE PROVISION",
            "text": body_text
        })
    return sections

def sync():
    sections = extract_all_sections()
    print(f"Extracted {len(sections)} sections from authentic Ordinance No. 0158-05 transcript.")
    
    # Base metadata
    base_meta = {
        "ordinance_no": "Ordinance No. 0158-05",
        "series": "2005",
        "title": "THE 2005 REVENUE CODE OF THE CITY OF DAVAO (FULL UNABRIDGED CODIFIED ENACTMENT)",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "total_sections": len(sections),
        "total_words": sum(len(s["text"].split()) for s in sections),
        "sections": sections
    }
    
    # 1. Update 03_arc_investors_holding_tax.json
    arc_json_path = REPO_ROOT / "src" / "demo" / "sample_cases" / "03_arc_investors_holding_tax.json"
    arc_data = {
        "filename_prefix": "03_arc_investors_holding_tax",
        "case_id": "DAVAO-TIER3-03",
        "case_name": "City of Davao and Tanjili v. ARC Investors, Inc.",
        "docket_no": "G.R. No. 249668 (July 13, 2022)",
        "challenged_section": 69,
        "challenged_subject": "Local Business Tax on Dividends of Corporate Holding Entities",
        **base_meta
    }
    arc_json_path.write_text(json.dumps(arc_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated {arc_json_path} ({arc_data['total_sections']} sections, {arc_data['total_words']:,} words)")
    
    # 2. Update 04_first_meridian_payment_under_protest.json
    fm_json_path = REPO_ROOT / "src" / "demo" / "sample_cases" / "04_first_meridian_payment_under_protest.json"
    fm_data = {
        "filename_prefix": "04_first_meridian_payment_under_protest",
        "case_id": "DAVAO-TIER3-04",
        "case_name": "City of Davao and Dureza v. First Meridian Development, Inc.",
        "docket_no": "G.R. No. 240078 (October 19, 2022)",
        "challenged_section": 423,
        "challenged_subject": "Mandatory Prior Payment Under Protest for Local Tax Invalidation",
        **base_meta
    }
    fm_json_path.write_text(json.dumps(fm_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated {fm_json_path} ({fm_data['total_sections']} sections, {fm_data['total_words']:,} words)")
    
    # 3. Synchronize PDF files
    pdf_destinations = [
        REPO_ROOT / "src" / "demo" / "sample_cases" / "pdf" / "03_arc_investors_holding_tax.pdf",
        REPO_ROOT / "src" / "demo" / "sample_cases" / "pdf" / "04_first_meridian_payment_under_protest.pdf",
        REPO_ROOT / "ground_truth" / "tier3_sc_cases" / "tier3_landmark_ordinances_pdf" / "03_arc_investors_holding_tax.pdf",
        REPO_ROOT / "ground_truth" / "tier3_sc_cases" / "tier3_landmark_ordinances_pdf" / "04_first_meridian_payment_under_protest.pdf",
        REPO_ROOT / "data" / "tier3_landmark_ordinances_pdf" / "03_arc_investors_holding_tax.pdf",
        REPO_ROOT / "data" / "tier3_landmark_ordinances_pdf" / "04_first_meridian_payment_under_protest.pdf",
    ]
    
    for dest in pdf_destinations:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(FULL_PDF_SOURCE, dest)
        print(f"Copied full 129-page PDF to: {dest}")

if __name__ == "__main__":
    sync()

