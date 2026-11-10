import json
import re
import time

t0 = time.time()
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

amend_trigger = re.compile(r'\b(?:hereby\s+amended|is\s+amended|are\s+amended|amending|as\s+amended\s+by)\b', re.IGNORECASE)
repeal_trigger = re.compile(r'\b(?:hereby\s+repealed|is\s+repealed|are\s+repealed|repealing)\b', re.IGNORECASE)

patterns = [
    ("ra", re.compile(r'(?:Republic\s+Act|R\.?\s*A\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("pd", re.compile(r'(?:Presidential\s+Decree|P\.?\s*D\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("bp", re.compile(r'(?:Batas\s+Pambansa|B\.?\s*P\.?)\s*(?:Blg\.?\s*)?(\d+)', re.IGNORECASE)),
    ("ca", re.compile(r'(?:Commonwealth\s+Act|C\.?\s*A\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("eo", re.compile(r'(?:Executive\s+Order|E\.?\s*O\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("act", re.compile(r'\bAct\s+No\.?\s*(\d+)', re.IGNORECASE)),
    ("ord", re.compile(r'(?:City\s+Ordinance|Ordinance)\s+No\.?\s*([0-9]+(?:-[0-9]+)?)', re.IGNORECASE)),
]

def find_targets_in_window(window):
    targets = []
    for prefix, p in patterns:
        for m in p.finditer(window):
            raw = m.group(1).lower()
            key = (prefix, int(raw) if prefix != "ord" else raw)
            tid = alias_to_id.get(key)
            if tid:
                targets.append(tid)
    return targets

t1 = time.time()
amends_davao = []
repeals_davao = []

with open("corpus/city_ordinances/categorized_davao_ordinances.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        src = data["ordinance_id"]
        text = data.get("full_text", "")
        # Find amends
        for m in amend_trigger.finditer(text):
            start = max(0, m.start() - 150)
            end = min(len(text), m.end() + 150)
            window = text[start:end]
            for tid in find_targets_in_window(window):
                if tid != src:
                    amends_davao.append((src, tid))
        # Find repeals
        for m in repeal_trigger.finditer(text):
            start = max(0, m.start() - 150)
            end = min(len(text), m.end() + 150)
            window = text[start:end]
            for tid in find_targets_in_window(window):
                if tid != src:
                    repeals_davao.append((src, tid))

t2 = time.time()
print(f"Safe window extraction on Davao ordinances took {t2-t1:.2f}s!")
print(f"  AMENDS edges found: {len(set(amends_davao))}")
print(f"  REPEALS edges found: {len(set(repeals_davao))}")

