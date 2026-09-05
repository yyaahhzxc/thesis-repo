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
    # Normalize whitespace and common encoding artifacts
    s = s.replace('\ufffd', "'").replace('\u0448', "'").replace('', "'")
    s = ' '.join(s.split())
    return s

def extract_between(text, start_pat, end_pat):
    m_s = re.search(start_pat, text, re.DOTALL | re.IGNORECASE)
    if not m_s:
        return "START PATTERN NOT FOUND: " + start_pat
    start_pos = m_s.start()
    m_e = re.search(end_pat, text[start_pos:], re.DOTALL | re.IGNORECASE)
    if not m_e:
        return clean(text[start_pos:start_pos+1200])
    end_pos = start_pos + m_e.start()
    return clean(text[start_pos:end_pos])

specs = {
    # DOMAIN 00
    "RA 7581 Sec 6": (7581, r'Section 6\.\s*Automatic Price Control\.', r'Section 7\.'),
    "RA 10121 Sec 12": (10121, r'Section 12\.\s*Local Disaster Risk Reduction', r'\(c\)\s*The Provincial'),
    "RA 11032 Sec 9": (11032, r'\(b\)\s*Action of Offices\.', r'\(c\)\s*Citizen'),
    
    # DOMAIN 01
    "RA 10931 Sec 4": (10931, r'Section 4\.\s*Free Higher Education', r'Section 5\.'),
    "RA 9165 Sec 36(c)": (9165, r'\(c\)\s*Students of secondary and tertiary schools\.', r'\(d\)\s*Officers and members'),
    "RA 11314 Sec 5": (11314, r'Section 5\.\s*Student Fare Discount Privilege\.', r'Section 6\.'),
    
    # DOMAIN 02
    "RA 7160 Sec 458": (7160, r'\(v\)\s*Approve ordinances imposing a fine', r'\(2\)\s*Generate and maximize'),
    "RA 9344 Sec 6": (9344, r'SEC\.\s*6\.\s*Minimum Age of Criminal Responsibility\.', r'SEC\.\s*7\.'),
    "RA 7160 Sec 152": (7160, r'\(c\)\s*Barangay Clearance\.', r'\(d\)\s*Other fees'),
    
    # DOMAIN 03
    "RA 4136 Sec 35": (4136, r'Section 35\.\s*Restriction as to speed\.', r'Section 36\.'),
    "RA 7925 Sec 4": (7925, r'Section 4\.\s*Declaration of National Policy\.', r'Section 5\.'),
    "RA 9136 Sec 43": (9136, r'\(f\)\s*The ERC shall have the original and exclusive', r'\(g\)\s*The ERC shall exercise'),
    
    # DOMAIN 04
    "RA 11223 Sec 6": (11223, r'Section 6\.\s*Service Coverage\.', r'Section 7\.'),
    "RA 11332 Sec 9": (11332, r'Section 9\.\s*Prohibited Acts\.', r'Section 10\.'),
    "RA 9211 Sec 5": (9211, r'Section 5\.\s*Smoking in Public Places', r'Section 6\.'),
    
    # DOMAIN 05
    "RA 7942 Sec 70": (7942, r'Section 70\s*Environmental Impact Assessment', r'Section 71\.'),
    "RA 8550 Sec 18": (8550, r'Section 18\.\s*Users of Municipal Waters\.', r'Section 19\.'),
    "RA 10591 Sec 31": (10591, r'Section 31\.\s*Absence of Permit to Carry', r'Section 32\.'),
    
    # DOMAIN 06
    "RA 7160 Sec 287": (7160, r'Section 287\.\s*Local Development Projects\.', r'Section 288\.'),
    "RA 10121 Sec 21": (10121, r'Section 21\.\s*Local Disaster Risk', r'Section 22\.'),
    
    # DOMAIN 07
    "RA 7160 Sec 233": (7160, r'Section 233\.\s*Rates of Levy\.', r'Section 234\.'),
    "RA 7160 Sec 140": (7160, r'Section 140\.\s*Amusement Tax\.', r'Section 141\.')
}

results = {}
for label, (law_id, s_pat, e_pat) in specs.items():
    raw_t = laws[law_id]
    ext = extract_between(raw_t, s_pat, e_pat)
    results[label] = ext
    print(f"=== {label} ===")
    print(ext[:300] + ("..." if len(ext) > 300 else ""))
    print()

with open("data/verbatim_statutory_sections.json", "w", encoding="utf-8") as out_f:
    json.dump(results, out_f, indent=2, ensure_ascii=False)
print("Saved all extracted verbatim sections to data/verbatim_statutory_sections.json")
