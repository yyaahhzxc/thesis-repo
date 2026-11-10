import json

with open("output/tier2_system_level_test_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== 7 GOLD PLANTED CONTRADICTIONS IN BASELINE RUN ===")
for doc in data.get("document_level_results", []):
    for s in doc.get("sections", []):
        if s.get("gold_label") == "Contradiction":
            print(f"Doc: {s.get('doc_id')} | Sec: {s.get('sec_num')} ({s.get('sec_title')})")
            print(f"  Gold Target Statute: {s.get('gold_target_statute')}")
            print(f"  Predicted Label:     {s.get('predicted_label')} (Prob: {s.get('conflict_probability')})")
            print(f"  Retrieved Top Law:   {s.get('retrieved_top_statute')}")
            print(f"  Correct:             {s.get('is_correct')}")
            print(f"  Snippet:             {s.get('text_snippet')[:120]}")
            print("-" * 75)
