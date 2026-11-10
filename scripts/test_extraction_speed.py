import json
import re
import time
from collections import defaultdict

t0 = time.time()

# 1. Alias index
print("Building alias index...")
alias_to_id = {}
enactment_meta = {}

# National Laws
with open("corpus/categorized_national_laws.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        lid = data["law_id"]
        cat = data.get("category", "")
        lnum = data.get("law_number", "")
        year = data.get("year")
        enactment_meta[lid] = {
            "type": "national",
            "number": lnum,
            "category": cat,
            "year": year,
            "domain": data.get("topic_label", "General Administration")
        }
        # map prefix + number
        parts = lid.split("_")
        prefix = parts[0]
        m = re.search(r'(\d+)', lnum)
        if m:
            num = int(m.group(1))
            alias_to_id[(prefix, num)] = lid

# Local Ordinances
with open("corpus/city_ordinances/categorized_davao_ordinances.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        oid = data["ordinance_id"]
        onum = data.get("ordinance_number", "").strip().lower()
        enactment_meta[oid] = {
            "type": "local",
            "number": onum,
            "category": "City Ordinance",
            "year": data.get("year"),
            "domain": data.get("functional_typology", "Administrative Routine")
        }
        if onum:
            alias_to_id[("ord", onum)] = oid
            parts = onum.split("-")
            if len(parts) == 2:
                # normalize leading zeros e.g. 002-16 vs 2-16
                p0 = str(int(parts[0])) if parts[0].isdigit() else parts[0]
                alias_to_id[("ord", f"{p0}-{parts[1]}")] = oid

print(f"Aliases built in {time.time()-t0:.2f}s! National: {sum(1 for v in enactment_meta.values() if v['type']=='national')}, Local: {sum(1 for v in enactment_meta.values() if v['type']=='local')}")

# Regex matchers
patterns = [
    ("ra", re.compile(r'(?:Republic\s+Act|R\.?\s*A\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("pd", re.compile(r'(?:Presidential\s+Decree|P\.?\s*D\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("bp", re.compile(r'(?:Batas\s+Pambansa|B\.?\s*P\.?)\s*(?:Blg\.?\s*)?(\d+)', re.IGNORECASE)),
    ("ca", re.compile(r'(?:Commonwealth\s+Act|C\.?\s*A\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("eo", re.compile(r'(?:Executive\s+Order|E\.?\s*O\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("act", re.compile(r'\bAct\s+No\.?\s*(\d+)', re.IGNORECASE)),
    ("ord", re.compile(r'(?:City\s+Ordinance|Ordinance)\s+No\.?\s*([0-9]+(?:-[0-9]+)?)', re.IGNORECASE)),
]

t1 = time.time()
print("\nExtracting citation edges from Davao Ordinances...")
ord_citations = 0
ord_to_nat = 0
ord_to_ord = 0

with open("corpus/city_ordinances/categorized_davao_ordinances.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        src_id = data["ordinance_id"]
        text = data.get("full_text", "")
        for prefix, p in patterns:
            for m in p.finditer(text):
                raw_target = m.group(1).lower()
                target_key = (prefix, int(raw_target) if prefix != "ord" else raw_target)
                target_id = alias_to_id.get(target_key)
                if target_id and target_id != src_id:
                    ord_citations += 1
                    if enactment_meta[target_id]["type"] == "national":
                        ord_to_nat += 1
                    else:
                        ord_to_ord += 1

print(f"Davao ordinances citation extraction took {time.time()-t1:.2f}s!")
print(f"  Total citation instances: {ord_citations}")
print(f"  Ordinance -> National citations: {ord_to_nat}")
print(f"  Ordinance -> Ordinance (Horizontal) citations: {ord_to_ord}")

