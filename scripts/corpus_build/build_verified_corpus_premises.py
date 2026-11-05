import json
import re

with open('corpus/national_laws/republic_acts.jsonl', 'r', encoding='utf-8') as f:
    laws = {}
    for line in f:
        item = json.loads(line)
        lid = item['law_id']
        parts = lid.split('_')
        if len(parts) >= 2 and parts[1].isdigit():
            laws[int(parts[1])] = item['text']

def clean(s):
    # Normalize whitespace, strip OCR noise like \ufffd or weird quotes
    s = s.replace('\ufffd', "'").replace('\u0448', "'")
    s = ' '.join(s.split())
    return s

def extract_section(law_num, start_pattern, end_pattern):
    raw_text = laws[law_num]
    m_s = re.search(start_pattern, raw_text, re.DOTALL | re.IGNORECASE)
    if not m_s:
        raise ValueError(f"Start pattern not found for RA {law_num}: {start_pattern}")
    start_pos = m_s.start()
    m_e = re.search(end_pattern, raw_text[start_pos:], re.DOTALL | re.IGNORECASE)
    if not m_e:
        raise ValueError(f"End pattern not found for RA {law_num}: {end_pattern}")
    end_pos = start_pos + m_e.start()
    extracted = clean(raw_text[start_pos:end_pos])
    return extracted

corpus_premises = {
    # -------------------------------------------------------------
    # Domain 00: Executive Issuances & Policy Reorganization
    # -------------------------------------------------------------
    "RA_7581_Sec_6": {
        "statute": "Republic Act No. 7581 (The Price Act)",
        "citation": "Section 6",
        "text": extract_section(7581, r'Section 6\.\s*Automatic Price Control\.', r'Section 7\.')
    },
    "RA_10121_Sec_12": {
        "statute": "Republic Act No. 10121 (Philippine Disaster Risk Reduction and Management Act of 2010)",
        "citation": "Section 12",
        "text": extract_section(10121, r'Section 12\.\s*Local Disaster Risk Reduction', r'\(c\)\s*The Provincial')
    },
    "RA_11032_Sec_9": {
        "statute": "Republic Act No. 11032 (Ease of Doing Business and Efficient Government Service Delivery Act of 2018)",
        "citation": "Section 9(b)(1)",
        "text": extract_section(11032, r'Sec\.\s*9\.\s*Accessing Government Services', r'\(2\)\s*No application')
    },

    # -------------------------------------------------------------
    # Domain 01: Education & Academic Institutions
    # -------------------------------------------------------------
    "RA_10931_Sec_4": {
        "statute": "Republic Act No. 10931 (Universal Access to Quality Tertiary Education Act)",
        "citation": "Section 4",
        "text": extract_section(10931, r'Section 4\.\s*Free Higher Education', r'Section 5\.')
    },
    "RA_9165_Sec_36c": {
        "statute": "Republic Act No. 9165 (Comprehensive Dangerous Drugs Act of 2002)",
        "citation": "Section 36(c)",
        "text": extract_section(9165, r'Section 36\.\s*Authorized Drug Testing', r'\(d\)\s*Officers and employees')
    },
    "RA_11314_Sec_5": {
        "statute": "Republic Act No. 11314 (Student Fare Discount Act)",
        "citation": "Section 5",
        "text": extract_section(11314, r'Section 5\.\s*Student Fare Discount Privilege\.', r'Section 6\.')
    },

    # -------------------------------------------------------------
    # Domain 02: Local Government & Territorial Boundaries
    # -------------------------------------------------------------
    "RA_7160_Sec_458": {
        "statute": "Republic Act No. 7160 (The Local Government Code of 1991)",
        "citation": "Section 458(a)(1)(iii)",
        "text": extract_section(7160, r'Section 458\.\s*Powers,\s*Duties', r'\(iv\)\s*Adopt measures')
    },
    "RA_9344_Sec_6": {
        "statute": "Republic Act No. 9344 (Juvenile Justice and Welfare Act of 2006)",
        "citation": "Section 6",
        "text": extract_section(9344, r'SEC\.\s*6\.\s*Minimum Age of Criminal Responsibility\.', r'SEC\.\s*7\.')
    },
    "RA_7160_Sec_152c": {
        "statute": "Republic Act No. 7160 (The Local Government Code of 1991)",
        "citation": "Section 152(c)",
        "text": extract_section(7160, r'Section 152\.\s*Scope of Taxing Powers', r'\(d\)\s*Other fees')
    },

    # -------------------------------------------------------------
    # Domain 03: Public Utilities & Telecom Franchises
    # -------------------------------------------------------------
    "RA_4136_Sec_35": {
        "statute": "Republic Act No. 4136 (Land Transportation and Traffic Code)",
        "citation": "Section 35",
        "text": extract_section(4136, r'Section 35\.\s*Restriction as to speed\.', r'Section 36\.')
    },
    "RA_7925_Sec_4": {
        "statute": "Republic Act No. 7925 (Public Telecommunications Policy Act of 1995)",
        "citation": "Section 4",
        "text": extract_section(7925, r'Section 4\.\s*Declaration of National Policy\.', r'Section 5\.')
    },
    "RA_9136_Sec_43u": {
        "statute": "Republic Act No. 9136 (Electric Power Industry Reform Act of 2001)",
        "citation": "Section 43(u)",
        "text": clean(
            re.search(r'Section 43\.\s*Functions of the ERC\..*?restuctured industry:', laws[9136], re.DOTALL | re.IGNORECASE).group(0) +
            " ... " +
            re.search(r'\(u\)\s*The ERC shall have the original and exclusive.*?energy sector\.', laws[9136], re.DOTALL | re.IGNORECASE).group(0)
        )
    },

    # -------------------------------------------------------------
    # Domain 04: Public Health, Hospitals & Medical Services
    # -------------------------------------------------------------
    "RA_11223_Sec_6": {
        "statute": "Republic Act No. 11223 (Universal Health Care Act)",
        "citation": "Section 6",
        "text": extract_section(11223, r'Section 6\.\s*Service Coverage\.', r'Section 7\.')
    },
    "RA_11332_Sec_9": {
        "statute": "Republic Act No. 11332 (Mandatory Reporting of Notifiable Diseases and Health Events of Public Health Concern Act)",
        "citation": "Section 9",
        "text": extract_section(11332, r'Section 9\.\s*Prohibited Acts\.', r'Section 10\.')
    },
    "RA_9211_Sec_5": {
        "statute": "Republic Act No. 9211 (Tobacco Regulation Act of 2003)",
        "citation": "Section 5",
        "text": extract_section(9211, r'Section 5\.\s*Smoking in Public Places', r'Section 6\.')
    },

    # -------------------------------------------------------------
    # Domain 05: Statutory Codes & General Legal Amendments
    # -------------------------------------------------------------
    "RA_7942_Sec_70": {
        "statute": "Republic Act No. 7942 (Philippine Mining Act of 1995)",
        "citation": "Section 70",
        "text": extract_section(7942, r'Section 70\s*Environmental Impact Assessment', r'Section 71\s*Rehabilitation')
    },
    "RA_8550_Sec_18": {
        "statute": "Republic Act No. 8550 (The Philippine Fisheries Code of 1998)",
        "citation": "Section 18",
        "text": extract_section(8550, r'Section 18\.\s*Users of Municipal Waters\.', r'Section 19\.')
    },
    "RA_10591_Sec_31": {
        "statute": "Republic Act No. 10591 (Comprehensive Firearms and Ammunition Regulation Act)",
        "citation": "Section 31",
        "text": extract_section(10591, r'Section 31\.\s*Absence of Permit to Carry', r'Section 32\.')
    },

    # -------------------------------------------------------------
    # Domain 06: Public Finance & General Appropriations
    # -------------------------------------------------------------
    "RA_7160_Sec_287": {
        "statute": "Republic Act No. 7160 (The Local Government Code of 1991)",
        "citation": "Section 287",
        "text": extract_section(7160, r'Section 287\.\s*Local Development Projects\.', r'Section 288\.')
    },
    "RA_10121_Sec_21": {
        "statute": "Republic Act No. 10121 (Philippine Disaster Risk Reduction and Management Act of 2010)",
        "citation": "Section 21",
        "text": extract_section(10121, r'Section 21\.\s*Local Disaster Risk', r'Section 22\.')
    },

    # -------------------------------------------------------------
    # Domain 07: Taxation, Tariffs & Revenue Administration
    # -------------------------------------------------------------
    "RA_7160_Sec_233": {
        "statute": "Republic Act No. 7160 (The Local Government Code of 1991)",
        "citation": "Section 233",
        "text": extract_section(7160, r'Section 233\.\s*Rates of Levy\.', r'Section 234\.')
    },
    "RA_7160_Sec_140": {
        "statute": "Republic Act No. 7160 (The Local Government Code of 1991)",
        "citation": "Section 140",
        "text": extract_section(7160, r'Section 140\.\s*Amusement Tax\.', r'Section 141\.')
    }
}

print(f"Successfully extracted all {len(corpus_premises)} verbatim statutory sections from corpus!")
for k, v in corpus_premises.items():
    print(f"{k} [{v['statute']} - {v['citation']}]: {len(v['text'])} chars")

with open("data/corpus_statute_premises.json", "w", encoding="utf-8") as out:
    json.dump(corpus_premises, out, indent=2, ensure_ascii=False)
print("Saved to data/corpus_statute_premises.json")
