import json
import re
import time
from collections import defaultdict

t0 = time.time()
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
        parts = lid.split("_")
        prefix = parts[0]
        m = re.search(r'(\d+)', lnum)
        if m:
            num = int(m.group(1))
            alias_to_id[(prefix, num)] = lid

patterns = [
    ("ra", re.compile(r'(?:Republic\s+Act|R\.?\s*A\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("pd", re.compile(r'(?:Presidential\s+Decree|P\.?\s*D\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("bp", re.compile(r'(?:Batas\s+Pambansa|B\.?\s*P\.?)\s*(?:Blg\.?\s*)?(\d+)', re.IGNORECASE)),
    ("ca", re.compile(r'(?:Commonwealth\s+Act|C\.?\s*A\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("eo", re.compile(r'(?:Executive\s+Order|E\.?\s*O\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("act", re.compile(r'\bAct\s+No\.?\s*(\d+)', re.IGNORECASE)),
]

t1 = time.time()
print("Extracting citation edges from 25,432 National Laws...")
nat_citations = 0
unique_edges = set()

with open("corpus/categorized_national_laws.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        src_id = data["law_id"]
        text = data.get("full_text", "")
        for prefix, p in patterns:
            for m in p.finditer(text):
                num = int(m.group(1))
                target_id = alias_to_id.get((prefix, num))
                if target_id and target_id != src_id:
                    nat_citations += 1
                    unique_edges.add((src_id, target_id))

t2 = time.time()
print(f"National laws extraction took {t2-t1:.2f}s!")
print(f"  Total citation occurrences: {nat_citations}")
print(f"  Unique directed citation edges: {len(unique_edges)}")

