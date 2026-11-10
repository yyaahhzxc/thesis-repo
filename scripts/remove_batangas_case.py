import json

with open("ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl", "r", encoding="utf-8") as f:
    lines = [json.loads(line) for line in f if line.strip()]

print(f"Total cases before: {len(lines)}")
filtered = [c for c in lines if "batangas" not in c.get("ordinance_no", "").lower() and c.get("case_id") != "SC-PHIL-11"]
print(f"Total cases after: {len(filtered)}")

for i, c in enumerate(filtered, 1):
    print(f"{i}. {c.get('case_id')} | {c.get('case_name')} | {c.get('ordinance_no')}")

# Save updated jsonl without Batangas
with open("ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl", "w", encoding="utf-8") as f:
    for c in filtered:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")
print("Successfully updated tier3_jurisprudential_cases.jsonl!")

