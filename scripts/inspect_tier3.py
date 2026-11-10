import json

with open("ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        item = json.loads(line)
        print(f"--- Case {i+1} ---")
        for k, v in item.items():
            if isinstance(v, str) and len(v) > 100:
                print(f"  {k}: {v[:100]}...")
            elif isinstance(v, list):
                print(f"  {k}: list of {len(v)} items")
            else:
                print(f"  {k}: {v}")
