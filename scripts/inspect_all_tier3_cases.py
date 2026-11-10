import json
from pathlib import Path

cases_path = Path("ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl")
if not cases_path.exists():
    cases_path = Path("data/tier3_jurisprudential_cases.jsonl")

cases = []
with open(cases_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            cases.append(json.loads(line))

print(f"Loaded {len(cases)} cases from {cases_path}:")
for c in cases:
    cid = c.get("case_id")
    cname = c.get("case_name") or c.get("title")
    ord_no = c.get("ordinance_no")
    stat = c.get("controlling_statute") or c.get("superior_national_law")
    gold = c.get("gold_nli_label") or c.get("gold_label")
    ruling = c.get("ruling") or c.get("judicial_reference")
    print(f"[{cid}] {ord_no} | {cname[:40]} | Gold: {gold} | Statute: {stat}")

