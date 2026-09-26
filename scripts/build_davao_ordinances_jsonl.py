"""
build_davao_ordinances_jsonl.py
================================
Compiles all 1,664 cleaned Davao City local ordinances into a standardized
JSONL archive: corpus/city_ordinances/categorized_davao_ordinances.jsonl
matching the structural schema of corpus/categorized_national_laws.jsonl.
"""

import os
import re
import sys
import json
from pathlib import Path
import numpy as np

# Ensure UTF-8 standard encoding
sys.stdout.reconfigure(encoding='utf-8')

CLEANED_DIR = Path("cleaned_transcriptions")
VLM_DIR = Path("vlm_transcriptions")
OUTPUT_DIR = Path("corpus/city_ordinances")
OUTPUT_FILE = OUTPUT_DIR / "categorized_davao_ordinances.jsonl"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Regex patterns
SECTION_PATTERN = re.compile(
    r'(?:\n|^)(SECTION\s+\d+|Sec\.\s+\d+)\b([^\n]*)\n(.*?)(?=(?:\n(?:SECTION\s+\d+|Sec\.\s+\d+)\b|\n(?:ENACTED|PASSED|CERTIFIED|ATTESTED|APPROVED)\b|\Z))',
    re.DOTALL | re.IGNORECASE
)

BOILERPLATE_KEYWORDS = ["TITLE", "SEPARABILITY", "REPEALING", "EFFECTIVITY"]

def extract_year(text, filename, parent_folder):
    if parent_folder.isdigit() and len(parent_folder) == 4:
        return int(parent_folder)
    m_enacted = re.search(r'(?:ENACTED|PASSED|APPROVED)[\s,:]+([A-Za-z]+\s+\d{1,2},?\s+)?(19\d\d|20\d\d)', text, re.IGNORECASE)
    if m_enacted:
        return int(m_enacted.group(2))
    m_series = re.search(r'Series\s+of\s+(19\d\d|20\d\d)', text, re.IGNORECASE)
    if m_series:
        return int(m_series.group(1))
    m_fn = re.search(r'-(\d{2,4})\b', filename)
    if m_fn:
        val = int(m_fn.group(1))
        if 50 < val < 100:
            return 1900 + val
        elif val <= 50:
            return 2000 + val
        elif 1900 <= val <= 2030:
            return val
    return 2021 # Fallback median year

def classify_typology(title, text):
    combined = (title + " " + text[:1500]).upper()
    if any(k in combined for k in ["ROAD CLOSURE", "CLOSURE OF ROAD", "TEMPORARY CLOSURE", "VEHICULAR TRAFFIC", "TRAFFIC REROUTING"]):
        return "Temporary Road Closures & Traffic Management", 5
    elif any(k in combined for k in ["CALAMITY", "QUICK RESPONSE FUND", "QRF", "DISASTER RISK REDUCTION", "LDRRMF"]):
        return "Disaster Risk Reduction, Calamity & QRF Funds", 3
    elif any(k in combined for k in ["DEED OF DONATION", "DEED OF ACCEPTANCE", "DONATION", "USUFRUCT", "REAL PROPERTY OF THE CITY"]):
        return "Deeds of Donation & Property Usufruct", 4
    elif any(k in combined for k in ["ZONING", "RECLASSIFICATION", "HOMEOWNERS ASSOCIATION", "SUBDIVISION", "DEVELOPMENT PERMIT", "LAND USE"]):
        return "Zoning Reclassifications & Subdivision Development", 6
    elif any(k in combined for k in ["ENTER INTO AND SIGN", "MEMORANDUM OF AGREEMENT", "MEMORANDUM OF UNDERSTANDING", "MOA", "MOU", "AUTHORIZING THE CITY MAYOR TO SIGN", "ACCEPT AND SIGN"]):
        return "Inter-Agency Agreements & Institutional MOAs/MOUs", 2
    else:
        return "Substantive Regulatory, Health & Penal Ordinances", 1

def determine_era(year):
    if year <= 1991:
        return "Pre-LGC Era (1950–1991)"
    elif 1992 <= year <= 2015:
        return "Post-LGC Historical Era (1992–2015)"
    elif 2016 <= year <= 2020:
        return "Pre-Pandemic Era (2016–2020)"
    else:
        return "LISSP Digital Era (2021–2025)"

all_files = sorted(list(CLEANED_DIR.rglob("*.txt")), key=lambda p: str(p))
print(f"Compiling {len(all_files)} cleaned ordinances to JSONL...")

records = []
total_sections = 0
total_operative = 0
total_boilerplate = 0

with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
    for idx, p in enumerate(all_files):
        rel_path = p.relative_to(CLEANED_DIR)
        vlm_p = VLM_DIR / rel_path
        
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            cl_text = f.read()
            
        vlm_text = ""
        if vlm_p.exists():
            with open(vlm_p, "r", encoding="utf-8", errors="replace") as f:
                vlm_text = f.read()
                
        # Clean title extraction
        m_title = re.search(r'AN\s+ORDINANCE\s+([^.\n]+(?:\n[^.\n]+)*)', cl_text, re.IGNORECASE)
        if m_title:
            raw_title = " ".join(m_title.group(1).split())[:300]
            title = f"AN ORDINANCE {raw_title}".strip()
        else:
            title = p.stem.replace("Ordinance No. ", "Ordinance No. ")
            
        # Enactment number
        m_ord_no = re.search(r'ORDINANCE\s+NO\.?\s*([0-9A-Za-z\-_]+)', cl_text, re.IGNORECASE)
        ord_num = m_ord_no.group(1).strip() if m_ord_no else p.stem
        
        year = extract_year(cl_text, p.name, p.parent.name)
        era = determine_era(year)
        typology_label, typology_id = classify_typology(title, cl_text)
        
        # Parse sections
        sec_matches = list(SECTION_PATTERN.finditer(cl_text))
        sections = []
        for s_idx, sm in enumerate(sec_matches):
            marker = sm.group(1).strip()
            sec_title = sm.group(2).strip().strip('.:- ')
            body = sm.group(3).strip()
            
            is_bp = any(kw in sec_title.upper() or kw in marker.upper() for kw in BOILERPLATE_KEYWORDS)
            words = len(body.split())
            est_tokens = int(np.round(words * 1.33))
            
            if is_bp:
                total_boilerplate += 1
            else:
                total_operative += 1
            total_sections += 1
            
            sections.append({
                "section_index": s_idx + 1,
                "section_marker": marker,
                "section_title": sec_title,
                "raw_text": body,
                "is_boilerplate": is_bp,
                "word_count": words,
                "est_tokens": est_tokens,
                "fits_512": est_tokens <= 512
            })
            
        cl_words = len(cl_text.split())
        cl_chars = len(cl_text)
        vlm_words = len(vlm_text.split()) if vlm_text else cl_words
        vlm_chars = len(vlm_text) if vlm_text else cl_chars
        
        doc_record = {
            "ordinance_id": f"davao_{p.stem.lower().replace(' ', '_').replace('.', '').replace('-', '_')}",
            "ordinance_number": ord_num,
            "filename": str(rel_path).replace("\\", "/"),
            "year": year,
            "era": era,
            "title": title,
            "functional_typology_id": typology_id,
            "functional_typology": typology_label,
            "word_count": cl_words,
            "char_count": cl_chars,
            "vlm_raw_word_count": vlm_words,
            "vlm_raw_char_count": vlm_chars,
            "chars_pruned": vlm_chars - cl_chars,
            "words_pruned": vlm_words - cl_words,
            "total_sections": len(sections),
            "operative_sections": sum(1 for s in sections if not s["is_boilerplate"]),
            "boilerplate_sections": sum(1 for s in sections if s["is_boilerplate"]),
            "sections": sections,
            "full_text": cl_text
        }
        
        out_f.write(json.dumps(doc_record, ensure_ascii=False) + "\n")
        records.append(doc_record)

print(f"\n[DONE] Successfully generated {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size / (1024*1024):.2f} MB)")
print(f"Total Enactments: {len(records)}")
print(f"Total Provisions: {total_sections} (Operative: {total_operative}, Boilerplate: {total_boilerplate})")
