import json

with open("ground_truth/tier2_synthetic_drafts/tier2_draft_ordinances_benchmark.jsonl", "r", encoding="utf-8") as f:
    for doc_idx, line in enumerate(f, 1):
        data = json.loads(line)
        doc_id = data.get("doc_id")
        auth = data.get("statutory_authority", "")
        print(f"\n[{doc_id}] Authority: {auth}")
        for s in data["sections"]:
            if s.get("label") == "Contradiction":
                print(f"  -> Sec {s['sec_num']}: [{s['sec_title']}]")
                print(f"     Target Statute: {s.get('target_statute')}")
                print(f"     Rationale: {s.get('legal_rationale')}")
                print(f"     Text snippet: {s.get('text')[:100]}...")
