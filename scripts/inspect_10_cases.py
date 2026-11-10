import json

with open("ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        c = json.loads(line)
        print(f"{i}. [{c.get('case_id')}] {c.get('case_name')}")
        print(f"   Ord: {c.get('ordinance_no')}")
        print(f"   Challenged: {c.get('challenged_text')[:90]}...")
        print(f"   Controlling: {c.get('controlling_statute')}")
        print(f"   Gold Label: {c.get('gold_nli_label')}")

