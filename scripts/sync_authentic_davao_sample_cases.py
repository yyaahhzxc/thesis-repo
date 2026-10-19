import re
import json
from pathlib import Path

BASE_DIR = Path("c:/Users/SHRIMP/Documents/thesis-repo")

def clean_ocr_artifacts(s: str) -> str:
    s = re.sub(r"---\s*\[Page \d+\]\s*---", "", s)
    s = re.sub(r"\*?\*?Page \d+ of \d+\*?\*?\s*\n\s*\*?\*?Ord\. No\. [^\n]+\*?\*?", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\*\*Page \d+ of \d+\*\*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\*\*", "", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

# =========================================================================
# 1. PROCESS ORDINANCE NO. 092-2000 (SIGNAGE & BILLBOARD REGULATION)
# =========================================================================
print("Processing Ordinance No. 092-2000 (Billboard Regulation)...")
with open(BASE_DIR / "cleaned_transcriptions/Ordinance No. 000092-00.txt", "r", encoding="utf-8") as f:
    text_092 = f.read()

# Strip page markers
text_092 = clean_ocr_artifacts(text_092)
enacting_092 = re.search(r"Be it ordained by the Sangguniang Panlungsod.*?:", text_092, re.IGNORECASE | re.DOTALL)
body_092 = text_092[enacting_092.end():].strip()

sec_specs_092 = [
    (1, "TITLE", r"SECTION\s+1\.\s*TITLE"),
    (2, "STATEMENT OF POLICY", r"SECTION\s+2\s*[\-\.]\s*STATEMENT OF POLICY"),
    (3, "SCOPE", r"SECTION\s+3\.\s*SCOPE"),
    (4, "APPLICABILITY", r"SECTION\s+4\s*[\-\.]\s*APPLICABILITY"),
    (5, "DEFINITION OF TERMS", r"SECTION\s+5\s*[\-\.]\s*DEFINITION"),
    (6, "GENERAL PROVISIONS", r"SECTION\s+1\.\s*\(a\)\s*Signs shall promote"),
    (7, "BILLBOARDS AND SIGNAGES", r"SECTION\s+7\s*[\-\.]\s*BILLBOARD"),
    (8, "REGULATED SCENIC AREAS", r"SECTION\s+8\s*[\-\.]\s*REGULATED AREAS"),
    (9, "ALLOWABLE HEIGHT FOR SIGN STRUCTURES IN REGULATED AREAS", r"SECTION\s+9\s*[\-\.]\s*ALLOWABLE HEIGHT FOR SIGN STRUCTURES"),
    (10, "ALLOWABLE SIZE FOR BUSINESS SIGNS", r"SECTION\s+10\s*[\-\.]\s*ALLOWABLE SIZE FOR BUSINESS SIGNS"),
    (11, "SIGNS ON BUILDING", r"SECTION\s+11\s*[\-\.]\s*SIGNS ON BUILDING"),
    (12, "SIGNS IN HIGHLY BUILT-UP URBAN AREAS", r"SECTION\s+12\.\s*SIGNS IN HIGHLY BUILT"),
    (13, "CONSTRUCTION OF ROOF SIGNS", r"SECTION\s+13\s*[\-\.]\s*CONSTRUCTION OF ROOF SIGNS"),
    (14, "ALLOWABLE HEIGHT FOR GROUND SIGNS", r"SECTION\s+14\.\s*ALLOWABLE HEIGHT FOR GROUND SIGNS"),
    (15, "LIMITATIONS ON GROUND SIGNS", r"SECTION\s+15\s*[\-\.]\s*LIMITATIONS"),
    (16, "PROJECTING SIGNS, IN GENERAL", r"SECTION\s+16\s*[\-\.]\s*PROJECTING SIGNS,\s*IN GENERAL"),
    (17, "INSTALLATION OF PROJECTING SIGNS", r"SECTION\s+17\.\s*INSTALLATION OF PROJECTING SIGNS"),
    (18, "WALL SIGNS ATTACHED ON BUILDINGS", r"SECTION\s+18\s*[\-\.]\s*WALL SIGNS ATTACHED ON BUILDINGS"),
    (19, "LIMITATION ON WALL SIGNS AND DISPLAY WINDOWS", r"SECTION\s+19\s*[\-\.]\s*LIMITATION"),
    (20, "TEMPORARY SIGNS", r"SECTION\s+20\s*[\-\.]\s*TEMPORARY SIGNS"),
    (21, "DISPLAY OF STREAMERS", r"SECTION\s+21\s*[\-\.]\s*DISPLAY OF STREAMERS"),
    (22, "LOADS AND STRESSES, IN GENERAL", r"SECTION\s+22\s*[\-\.]\s*LOADS AND STRESSES"),
    (23, "WIND LOADS", r"SECTION\s+72\s*[\-\.]\s*MINI LOADS"),
    (24, "SEISMIC LOADS", r"SECTION\s+73\s*[\-\.]\s*SEISMIC LOADS"),
    (25, "COMBINED LOADS", r"SECTION\s+74\s*[\-\.]\s*COMBINED LOADS"),
    (26, "ALLOWABLE STRESSES", r"SECTION\s+75\s*[\-\.]\s*ALLOWABLE STRESSES"),
    (27, "CONSTRUCTION, IN GENERAL", r"SECTION\s+76\s*[\-\.]\s*CONSTRUCTION,\s*IN GENERAL"),
    (28, "MATERIALS", r"SECTION\s+77\s*[\-\.]\s*MATERIALS"),
    (29, "ANCHORAGE, IN GENERAL", r"SECTION\s+29\s*[\-\.]\s*ANNEXA"),
    (30, "SIGNS ATTACHED TO BASE", r"SECTION\s+30\s*[\-\.]\s*SIGNS ATTACHED TO BASE"),
    (31, "SIGNS ATTACHED TO CONCRETE", r"SECTION\s+31\s*[\-\.]\s*SIGNS ATTACHED TO CONCRETE"),
    (32, "SIGNS ATTACHED TO WOOD", r"SECTION\s+32\s*[\-\.]\s*SIGNS ATTACHED TO WOOD"),
    (33, "ISSUANCE OF SIGN PERMITS", r"SECTION\s+33\s*[\-\.]\s*ISSUANCE OF SIGN PERMITS"),
    (34, "EFFECTIVITY OF SIGN PERMIT", r"SECTION\s+34\s*[\-\.]\s*EFFECTIVITY OF SIGN PERMIT"),
    (35, "EXTENSION OF SIGN PERMITS", r"SECTION\s+35\s*[\-\.]\s*EXTENSION OF SIGN PERMITS"),
    (36, "EXEMPTION FROM SIGN PERMIT", r"SECTION\s+36\s*[\-\.]\s*EXEMPTION FROM SIGN PERMIT"),
    (37, "SIGN PERMIT FEES", r"SECTION\s+37\s*[\-\.]\s*FEES"),
    (38, "EXEMPTION FROM SIGN FEE", r"SECTION\s+3A\s*[\-\.]\s*EXEMPTION FROM SIGN FEE"),
    (39, "MARKING REQUIREMENTS", r"SECTION\s+39\s*[\-\.]\s*MARKING REQUIREMENTS"),
    (40, "EXEMPTION FROM MARKING REQUIREMENT", r"SECTION\s+40\s*[\-\.]\s*EXEMPTION FROM THE MARKING REQUIREMENT"),
    (41, "RESTRICTED AREAS", r"SECTION\s+41\s*[\-\.]\s*RESTRICTED AREAS"),
    (42, "EXEMPTION FROM RESTRICTED AREA PROHIBITIONS", r"SECTION\s+42\s*[\-\.]\s*EXEMPTION"),
    (43, "MONITORING OFFICIAL", r"SECTION\s+43\s*[\-\.]\s*MONITORING OFFICIAL"),
    (44, "SIGNS AND SIGN STRUCTURES INSPECTION", r"SECTION\s+44\s*[\-\.]\s*SIGNS & SIGN STRUCTURES"),
    (45, "REMOVAL OF ILLEGAL ADVERTISING MATERIALS", r"SECTION\s+45\s*[\-\.]\s*REMOVAL"),
    (46, "PENALTIES", r"SECTION\s+16\.\s*PENALTY"),
    (47, "EXISTING SIGNS, IN GENERAL", r"SECTION\s+47\s*[\-\.]\s*FIXING SIGNS"),
    (48, "VALIDATING PERMIT", r"SECTION\s+48\s*[\-\.]\s*VALIDATING PERMIT"),
    (49, "NON-OBSERVANCE OF THIS ORDINANCE", r"SECTION\s+49\s*[\-\.]\s*NON-OBSERVANCE OF THIS ORDINANCE"),
    (50, "SEPARABILITY CLAUSE", r"SECTION\s+50\s*[\-\.]\s*SEPARABILITY CLAUSE"),
    (51, "REPEALING CLAUSE", r"SECTION\s+51\s*[\-\.]\s*REPEALING FLAWS"),
    (52, "EFFECTIVITY CLAUSE", r"SECTION\s+3:\s*EFFECTIVITY CLAUSE")
]

matches_092 = []
for sec_num, sec_title, pat in sec_specs_092:
    m = re.search(pat, body_092, re.IGNORECASE)
    if m:
        matches_092.append((sec_num, sec_title, m.start(), m.end()))
    else:
        print(f"Warning: Failed to match Sec {sec_num}: {sec_title}")

matches_092.sort(key=lambda x: x[2])
sections_092 = []
for i in range(len(matches_092)):
    sec_num, sec_title, start, end = matches_092[i]
    next_start = matches_092[i+1][2] if i + 1 < len(matches_092) else len(body_092)
    chunk = body_092[end:next_start].strip()
    # clean leading separators
    chunk = re.sub(r"^[\.\-\:\s\,]+", "", chunk).strip()
    
    # Fix minor OCR artifact text in section 6
    if sec_num == 6 and not chunk.startswith("(a)"):
        chunk = "(a) " + chunk
        
    sections_092.append({
        "sec_num": sec_num,
        "sec_title": sec_title,
        "text": chunk
    })

print(f"Ordinance 092-2000 parsed: {len(sections_092)} sections.")

# Build 092 JSON
data_092 = {
    "filename_prefix": "02_evasco_billboard_regulation",
    "case_id": "DAVAO-TIER3-02",
    "case_name": "Hon. Leoncio Evasco, Jr. v. Alex P. Montañez",
    "docket_no": "G.R. No. 199172 (February 21, 2018)",
    "ordinance_no": "Ordinance No. 092-2000",
    "title": "AN ORDINANCE REGULATING THE CONSTRUCTION, REPAIR, RENOVATION, ERECTION, INSTALLATION AND MAINTENANCE OF OUTDOOR ADVERTISING MATERIALS AND STRUCTURES IN DAVAO CITY",
    "enacting_lgu": "City of Davao",
    "enacting_clause": "Be it ordained by the Sangguniang Panlungsod of Davao City in session assembled:",
    "sections": sections_092
}

# Build 092 TXT
txt_092 = f"""=== Ordinance No. 092-2000 ===
Title: AN ORDINANCE REGULATING THE CONSTRUCTION, REPAIR, RENOVATION, ERECTION, INSTALLATION AND MAINTENANCE OF OUTDOOR ADVERTISING MATERIALS AND STRUCTURES IN DAVAO CITY
Enacting LGU: City of Davao
Judicial Reference: Hon. Leoncio Evasco, Jr. v. Alex P. Montañez (G.R. No. 199172 (February 21, 2018; 856 SCRA 320))
Judicial Ruling: Constitutional and Valid Exercise of Delegated Police Power (Upheld)
Gold NLI Label: Entailment
Superior National Law: Republic Act No. 7160 §458(a)(4)(iv); Presidential Decree No. 1096 §301

Be it ordained by the Sangguniang Panlungsod of Davao City in session assembled:

"""
for s in sections_092:
    txt_092 += f"SECTION {s['sec_num']}. {s['sec_title']} - {s['text']}\n\n"

# Save 092
with open(BASE_DIR / "demo/sample_cases/02_evasco_billboard_regulation.json", "w", encoding="utf-8") as f:
    json.dump(data_092, f, indent=2, ensure_ascii=False)
with open(BASE_DIR / "demo/sample_cases/02_evasco_billboard_regulation.txt", "w", encoding="utf-8") as f:
    f.write(txt_092)
with open(BASE_DIR / "corpus/davao_city_tier3_ordinances/Ordinance_No._092-2000.json", "w", encoding="utf-8") as f:
    json.dump(data_092, f, indent=2, ensure_ascii=False)
with open(BASE_DIR / "corpus/davao_city_tier3_ordinances/Ordinance_No._092-2000.txt", "w", encoding="utf-8") as f:
    f.write(txt_092)

# =========================================================================
# 2. PROCESS ORDINANCE NO. 0367-12 (ANTI-SMOKING ORDINANCE)
# =========================================================================
print("\nProcessing Ordinance No. 0367-12 (Anti-Smoking)...")
with open(BASE_DIR / "cleaned_transcriptions/Ordinance No. 0367-12.txt", "r", encoding="utf-8") as f:
    text_0367 = f.read()

text_0367 = clean_ocr_artifacts(text_0367)
enacting_0367 = re.search(r"Be it ordained by the Sangguniang Panlungsod.*?:", text_0367, re.IGNORECASE | re.DOTALL)
body_0367 = text_0367[enacting_0367.end():].strip()

sec_specs_0367 = [
    (1, "TITLE", r"SECTION\s+(?:I|1)\.\s*TITLE\."),
    (2, "COVERAGE", r"SECTION\s+2\.\s*COVERAGE\."),
    (3, "DEFINITION OF TERMS", r"SECTION\s+3\.\s*DEFINITION OF TERMS"),
    (4, "PROHIBITED ACTS", r"SECTION\s+4\.\s*PROHIBITED ACTS"),
    (5, "MANDATORY DUTIES AND OBLIGATIONS", r"SECTION\s+5\.\s*MANDATORY DUTIES AND OBLIGATIONS"),
    (6, "PERSONS LIABLE", r"SECTION\s+6\.\s*PERSONS LIABLE"),
    (7, "ANTI-SMOKING TASK FORCE", r"SECTION\s+7\.\s*An Anti-Smoking Task Force"),
    (8, "PENALTIES", r"SECTION\s+8\.\s*PENALTIES"),
    (9, "CITATION TICKETS", r"SECTION\s+9\.\s*CITATION TICKETS"),
    (10, "NO CONTEST PROVISION", r"SECTION\s+10\.\s*NO CONTEST PROVISION"),
    (11, "IMPLEMENTING RULES AND REGULATIONS", r"SECTION\s+11\.\s*IMPLEMENTING RULES AND REGULATIONS"),
    (12, "FUNDING", r"SECTION\s+12\.\s*FUNDING"),
    (13, "REPEALING CLAUSE", r"SECTION\s+13\.\s*REPEALING CLAUSE"),
    (14, "SEPARABILITY CLAUSE", r"SECTION\s+14\.\s*SEPARABILITY CLAUSE"),
    (15, "EFFECTIVITY CLAUSE", r"SECTION\s+15\.\s*EFFECTIVITY CLAUSE")
]

matches_0367 = []
for sec_num, sec_title, pat in sec_specs_0367:
    m = re.search(pat, body_0367, re.IGNORECASE)
    if m:
        matches_0367.append((sec_num, sec_title, m.start(), m.end()))
    else:
        print(f"Warning: Failed to match Sec {sec_num}: {sec_title}")

matches_0367.sort(key=lambda x: x[2])
sections_0367 = []
for i in range(len(matches_0367)):
    sec_num, sec_title, start, end = matches_0367[i]
    next_start = matches_0367[i+1][2] if i + 1 < len(matches_0367) else len(body_0367)
    chunk = body_0367[end:next_start].strip()
    chunk = re.sub(r"^[\.\-\:\s\,]+", "", chunk).strip()
    sections_0367.append({
        "sec_num": sec_num,
        "sec_title": sec_title,
        "text": chunk
    })

print(f"Ordinance 0367-12 parsed: {len(sections_0367)} sections.")

data_0367 = {
    "filename_prefix": "07_davao_anti_smoking_stricter_standard",
    "case_id": "DAVAO-TIER3-07",
    "case_name": "Davao City Comprehensive Anti-Smoking Ordinance vs. National Standards",
    "docket_no": "Promulgated as Ord. No. 0367-12 (September 25, 2012)",
    "ordinance_no": "Ordinance No. 0367-12",
    "title": "THE NEW COMPREHENSIVE ANTI-SMOKING ORDINANCE OF DAVAO CITY",
    "enacting_lgu": "City of Davao",
    "enacting_clause": "Be it ordained by the Sangguniang Panlungsod of Davao City, in session assembled that:",
    "sections": sections_0367
}

txt_0367 = f"""=== Ordinance No. 0367-12 ===
Title: THE NEW COMPREHENSIVE ANTI-SMOKING ORDINANCE OF DAVAO CITY
Enacting LGU: City of Davao
Judicial Reference: Davao City Comprehensive Anti-Smoking Ordinance vs. National Standards (Ord. No. 0367-12)
Judicial Ruling: Constitutional and Valid Exercise of Delegated Police Power (Upheld)
Gold NLI Label: Entailment
Superior National Law: Republic Act No. 7160 §16; Republic Act No. 9211 §5

Be it ordained by the Sangguniang Panlungsod of Davao City, in session assembled that:

"""
for s in sections_0367:
    txt_0367 += f"SECTION {s['sec_num']}. {s['sec_title']} - {s['text']}\n\n"

with open(BASE_DIR / "demo/sample_cases/07_davao_anti_smoking_stricter_standard.json", "w", encoding="utf-8") as f:
    json.dump(data_0367, f, indent=2, ensure_ascii=False)
with open(BASE_DIR / "demo/sample_cases/07_davao_anti_smoking_stricter_standard.txt", "w", encoding="utf-8") as f:
    f.write(txt_0367)
with open(BASE_DIR / "corpus/davao_city_tier3_ordinances/Ordinance_No._0367-12.json", "w", encoding="utf-8") as f:
    json.dump(data_0367, f, indent=2, ensure_ascii=False)
with open(BASE_DIR / "corpus/davao_city_tier3_ordinances/Ordinance_No._0367-12.txt", "w", encoding="utf-8") as f:
    f.write(txt_0367)

# =========================================================================
# 3. PROCESS ORDINANCE NO. 0270-23 (SPEED LIMIT ORDINANCE)
# =========================================================================
print("\nProcessing Ordinance No. 0270-23 (Speed Limits)...")
with open(BASE_DIR / "cleaned_transcriptions/Ordinance No. 0270-23 Speed Limits.txt", "r", encoding="utf-8") as f:
    text_0270 = f.read()

text_0270 = clean_ocr_artifacts(text_0270)
enacting_0270 = re.search(r"Be it ordained by the Sangguniang Panlungsod.*?:", text_0270, re.IGNORECASE | re.DOTALL)
body_0270 = text_0270[enacting_0270.end():].strip()

sec_specs_0270 = [
    (1, "TITLE", r"SECTION\s+1\.\s*TITLE"),
    (2, "DECLARATION OF POLICY", r"SECTION\s+2\.\s*DECLARATION OF POLICY"),
    (3, "COVERAGE", r"SECTION\s+3\.\s*COVERAGE"),
    (4, "INTERPRETATION", r"SECTION\s+4\.\s*INTERPRETATION"),
    (5, "DEFINITION OF TERMS", r"SECTION\s+5\.\s*DEFINITION OF TERMS"),
    (6, "OVERSPEEDING AND RECKLESS DRIVING", r"SECTION\s+6\.\s*OVERSPEEDING AND RECKLESS DRIVING"),
    (7, "SPEED LIMITS", r"SECTION\s+7\.\s*SPEED LIMITS"),
    (8, "TEMPORARY SPEED LIMIT", r"SECTION\s+8\.\s*TEMPORARY SPEED LIMIT"),
    (9, "EXEMPTIONS", r"SECTION\s+9\.\s*EXEMPTIONS"),
    (10, "LEAD AND SUPPORT AGENCIES", r"SECTION\s+10\.\s*LEAD AND SUPPORT AGENCIES"),
    (11, "RESPONSIBILITIES OF THE CTTMO", r"SECTION\s+11\.\s*RESPONSIBILITIES OF THE CITY TRANSPORT"),
    (12, "ENFORCEMENT PROCEDURE", r"SECTION\s+12\.\s*ENFORCEMENT PROCEDURE"),
    (13, "PROTEST ADJUDICATION", r"SECTION\s+13\.\s*PROTEST ADJUDICATION"),
    (14, "ADMINISTRATIVE FINES", r"SECTION\s+14\.\s*ADMINISTRATIVE FINES"),
    (15, "FAILURE TO SETTLE ADMINISTRATIVE FINES", r"SECTION\s+15\.\s*EFFECT OF FAILURE TO SETTLE"),
    (16, "APPROPRIATION", r"SECTION\s+16\.\s*APPROPRIATION"),
    (17, "REVIEW OF SPEED LIMITS", r"SECTION\s+17\.\s*REVIEW OF SPEED LIMITS"),
    (18, "INFORMATION, EDUCATION, AND COMMUNICATION CAMPAIGN", r"SECTION\s+18\.\s*INFORMATION"),
    (19, "REPEALING CLAUSE", r"SECTION\s+19\.\s*REPEALING CLAUSE"),
    (20, "SEPARABILITY CLAUSE", r"SECTION\s+20\.\s*SEPARABILITY CLAUSE"),
    (21, "EFFECTIVITY", r"SECTION\s+21\.\s*EFFECTIVITY")
]

matches_0270 = []
for sec_num, sec_title, pat in sec_specs_0270:
    m = re.search(pat, body_0270, re.IGNORECASE)
    if m:
        matches_0270.append((sec_num, sec_title, m.start(), m.end()))
    else:
        print(f"Warning: Failed to match Sec {sec_num}: {sec_title}")

matches_0270.sort(key=lambda x: x[2])
sections_0270 = []
for i in range(len(matches_0270)):
    sec_num, sec_title, start, end = matches_0270[i]
    next_start = matches_0270[i+1][2] if i + 1 < len(matches_0270) else len(body_0270)
    chunk = body_0270[end:next_start].strip()
    chunk = re.sub(r"^[\.\-\:\s\,]+", "", chunk).strip()
    sections_0270.append({
        "sec_num": sec_num,
        "sec_title": sec_title,
        "text": chunk
    })

print(f"Ordinance 0270-23 parsed: {len(sections_0270)} sections.")

data_0270 = {
    "filename_prefix": "08_davao_speed_limits_traffic_code",
    "case_id": "DAVAO-TIER3-08",
    "case_name": "Davao City Comprehensive Speed Limit Ordinance under Joint JAO 2018-01",
    "docket_no": "Promulgated as Ord. No. 0270-23 (October 2023)",
    "ordinance_no": "Ordinance No. 0270-23",
    "title": "THE COMPREHENSIVE SPEED LIMIT ORDINANCE OF DAVAO CITY",
    "enacting_lgu": "City of Davao",
    "enacting_clause": "Be it ordained by the Sangguniang Panlungsod of Davao City, in session assembled, that:",
    "sections": sections_0270
}

txt_0270 = f"""=== Ordinance No. 0270-23 ===
Title: THE COMPREHENSIVE SPEED LIMIT ORDINANCE OF DAVAO CITY
Enacting LGU: City of Davao
Judicial Reference: Davao City Comprehensive Speed Limit Ordinance under Joint JAO 2018-01 (Ord. No. 0270-23)
Judicial Ruling: Constitutional and Valid Delegated Rate-Setting Exercise (Upheld)
Gold NLI Label: Entailment
Superior National Law: Republic Act No. 4136 §35, §38; Joint DILG-DOTr-DPWH JAO 2018-01

Be it ordained by the Sangguniang Panlungsod of Davao City, in session assembled, that:

"""
for s in sections_0270:
    txt_0270 += f"SECTION {s['sec_num']}. {s['sec_title']} - {s['text']}\n\n"

with open(BASE_DIR / "demo/sample_cases/08_davao_speed_limits_traffic_code.json", "w", encoding="utf-8") as f:
    json.dump(data_0270, f, indent=2, ensure_ascii=False)
with open(BASE_DIR / "demo/sample_cases/08_davao_speed_limits_traffic_code.txt", "w", encoding="utf-8") as f:
    f.write(txt_0270)
with open(BASE_DIR / "corpus/davao_city_tier3_ordinances/Ordinance_No._0270-23.json", "w", encoding="utf-8") as f:
    json.dump(data_0270, f, indent=2, ensure_ascii=False)
with open(BASE_DIR / "corpus/davao_city_tier3_ordinances/Ordinance_No._0270-23.txt", "w", encoding="utf-8") as f:
    f.write(txt_0270)

print("\nSUCCESS: All authentic Davao City ordinances synchronized across corpus and sample_cases!")
