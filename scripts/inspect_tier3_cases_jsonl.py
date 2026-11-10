import json

with open("ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        cid = d.get("case_id")
        if cid in ["DAVAO-TIER3-05", "DAVAO-TIER3-06", "DAVAO-TIER3-03", "DAVAO-TIER3-04"]:
            print(f"=== {cid}: {d.get('case_name')} ===")
            print("Ordinance No:", d.get("ordinance_no"))
            print("Ruling:", d.get("ruling"))
            print("Controlling statute:", d.get("controlling_statute"))
            print("Challenged text snippet:", d.get("challenged_text")[:200])
            print()

