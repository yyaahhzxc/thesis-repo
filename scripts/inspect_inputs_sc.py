import sys
sys.path.insert(0, ".")
import json
from pathlib import Path
from src.demo.app import resolve_statute_passage

cases = []
with open("ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            cases.append(json.loads(line))

for c in cases[:4]:
    cid = c.get("case_id")
    target_statute = c.get("controlling_statute") or c.get("superior_national_law")
    premise_text = c.get("premise_text", "")
    hypo_text = c.get("challenged_text", "")
    
    primary_stat = target_statute.split(";")[0].strip()
    t_title, stat_passage = resolve_statute_passage(primary_stat, premise_text)
    
    print(f"=== {cid} ===")
    print("Controlling statute:", primary_stat)
    print("premise_text in jsonl:", premise_text[:100])
    print("Resolved premise text snippet:", (stat_passage or premise_text)[:120])
    print("Hypothesis text snippet:", hypo_text[:120])
    print()
