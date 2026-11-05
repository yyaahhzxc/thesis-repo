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

def clean_txt(t):
    t = t.replace('\ufffd', ' ').replace('\u0448', ' ')
    return ' '.join(t.split())

def find_snippet(law_num, pattern, max_len=600):
    txt = laws.get(law_num, "")
    m = re.search(pattern, txt, re.DOTALL | re.IGNORECASE)
    if m:
        c = clean_txt(m.group(0))
        return c[:max_len]
    return "NOT FOUND"

queries = {
    "RA 7581 Sec 6": (7581, r'Section 6\.\s*Automatic Price Control\..*?(?=Section 7\.)'),
    "RA 10121 Sec 12": (10121, r'Section 12\.\s*Local Disaster Risk Reduction and Management Office.*?(?=\(c\)\s*The Provincial)'),
    "RA 11032 Sec 9(b)": (11032, r'\(b\)\s*Action of Offices\..*?(?=\(c\)\s*Citizen)'),
    "RA 10931 Sec 4": (10931, r'Section 4\.\s*Free Higher Education in SUCs and LUCs\..*?(?=Section 5\.)'),
    "RA 9165 Sec 36(c)": (9165, r'\(c\)\s*Students of secondary and tertiary schools\..*?(?=\(d\)\s*Officers and members)'),
    "RA 11314 Sec 4": (11314, r'Section 4\.\s*Student Fare Discount Privileges\..*?(?=Section 5\.)'),
    "RA 7160 Sec 458(a)(1)(v)": (7160, r'\(v\)\s*Approve ordinances imposing a fine.*?(?=\(2\) Generate and maximize)'),
    "RA 9344 Sec 6": (9344, r'Section 6\.\s*Minimum Age of Criminal Responsibility\..*?(?=Section 7\.)'),
    "RA 7160 Sec 152(c)": (7160, r'\(c\)\s*Barangay Clearance\..*?(?=Section 153)'),
    "RA 4136 Sec 35": (4136, r'Section 35\.\s*Restriction as to speed\..*?(?=Section 36)'),
    "RA 7925 Sec 4": (7925, r'Section 4\.\s*Declaration of National Policy\..*?(?=Section 5\.)'),
    "RA 9136 Sec 43(f)": (9136, r'\(f\)\s*The ERC shall have the original and exclusive.*?(?=\(g\)\s*The ERC)'),
    "RA 11223 Sec 6": (11223, r'Section 6\.\s*Service Coverage\..*?(?=Section 7\.)'),
    "RA 11332 Sec 9": (11332, r'Section 9\.\s*Prohibited Acts\..*?(?=Section 10\.)'),
    "RA 9211 Sec 5": (9211, r'Section 5\.\s*Smoking in Public Places\..*?(?=Section 6\.)'),
    "RA 7942 Sec 70": (7942, r'Section 70\.\s*Environmental Impact Assessment.*?(?=Section 71\.)'),
    "RA 8550 Sec 18": (8550, r'Section 18\.\s*Users of Municipal Waters\..*?(?=Section 19\.)'),
    "RA 10591 Sec 31": (10591, r'Section 31\.\s*Absence of Permit to Carry Outside of Residence\..*?(?=Section 32\.)'),
    "RA 7160 Sec 287": (7160, r'Section 287\.\s*Local Development Projects\..*?(?=Section 288\.)'),
    "RA 10121 Sec 21": (10121, r'Section 21\.\s*Local Disaster Risk Reduction and Management Fund.*?(?=Section 22\.)'),
    "RA 7160 Sec 233": (7160, r'Section 233\.\s*Rates of Levy\..*?(?=Section 234\.)'),
    "RA 7160 Sec 140": (7160, r'Section 140\.\s*Amusement Tax\..*?(?=Section 141\.)')
}

for name, (num, pat) in queries.items():
    res = find_snippet(num, pat)
    print(f"=== {name} ===")
    print(res)
    print()
