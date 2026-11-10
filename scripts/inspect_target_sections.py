import json

with open("ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        c = json.loads(line)
        print(f"Case: {c.get('case_id')} | {c.get('case_name')[:40]} | Target: {c.get('target_section_no')} | Label: {c.get('gold_nli_label')}")

