import json
import re

# Load aliases
alias_to_id = {}
with open("corpus/categorized_national_laws.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        lid = data["law_id"]
        parts = lid.split("_")
        prefix = parts[0]
        m = re.search(r'(\d+)', data.get("law_number", ""))
        if m:
            alias_to_id[(prefix, int(m.group(1)))] = lid

with open("corpus/city_ordinances/categorized_davao_ordinances.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        oid = data["ordinance_id"]
        onum = data.get("ordinance_number", "").strip().lower()
        if onum:
            alias_to_id[("ord", onum)] = oid
            parts = onum.split("-")
            if len(parts) == 2:
                p0 = str(int(parts[0])) if parts[0].isdigit() else parts[0]
                alias_to_id[("ord", f"{p0}-{parts[1]}")] = oid

# Regex for amend/repeal clauses
amend_clause_pat = re.compile(r'([^.\n;]+(?:hereby\s+amended|is\s+amended|are\s+amended|amending|as\s+amended\s+by)[^.\n;]*)', re.IGNORECASE)
repeal_clause_pat = re.compile(r'([^.\n;]+(?:hereby\s+repealed|is\s+repealed|are\s+repealed|repealing)[^.\n;]*)', re.IGNORECASE)

# Citation extractors
patterns = [
    ("ra", re.compile(r'(?:Republic\s+Act|R\.?\s*A\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("pd", re.compile(r'(?:Presidential\s+Decree|P\.?\s*D\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("bp", re.compile(r'(?:Batas\s+Pambansa|B\.?\s*P\.?)\s*(?:Blg\.?\s*)?(\d+)', re.IGNORECASE)),
    ("ca", re.compile(r'(?:Commonwealth\s+Act|C\.?\s*A\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("eo", re.compile(r'(?:Executive\s+Order|E\.?\s*O\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("act", re.compile(r'\bAct\s+No\.?\s*(\d+)', re.IGNORECASE)),
    ("ord", re.compile(r'(?:City\s+Ordinance|Ordinance)\s+No\.?\s*([0-9]+(?:-[0-9]+)?)', re.IGNORECASE)),
]

def extract_target_from_clause(clause):
    targets = []
    for prefix, p in patterns:
        for m in p.finditer(clause):
            raw = m.group(1).lower()
            key = (prefix, int(raw) if prefix != "ord" else raw)
            tid = alias_to_id.get(key)
            if tid:
                targets.append(tid)
    return targets

# Test on Davao Ordinances
amends_davao = []
repeals_davao = []

with open("corpus/city_ordinances/categorized_davao_ordinances.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        src = data["ordinance_id"]
        text = data.get("full_text", "")
        # Amend clauses
        for m in amend_clause_pat.finditer(text):
            clause = m.group(1)
            for tid in extract_target_from_clause(clause):
                if tid != src:
                    amends_davao.append((src, tid, clause[:80]))
        # Repeal clauses
        for m in repeal_clause_pat.finditer(text):
            clause = m.group(1)
            for tid in extract_target_from_clause(clause):
                if tid != src:
                    repeals_davao.append((src, tid, clause[:80]))

print(f"Davao Ordinances - Specific AMENDS edges: {len(amends_davao)}")
for a in amends_davao[:5]:
    print(" ", a[0], "AMENDS ->", a[1], "|", a[2])

print(f"Davao Ordinances - Specific REPEALS edges: {len(repeals_davao)}")
for r in repeals_davao[:5]:
    print(" ", r[0], "REPEALS ->", r[1], "|", r[2])

