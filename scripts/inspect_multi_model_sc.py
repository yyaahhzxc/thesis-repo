import json

with open("output/multi_model_sc_comparison.json", "r", encoding="utf-8") as f:
    d = json.load(f)

print("Keys:", list(d.keys()))
if "models" in d:
    for m in d["models"]:
        print("Model:", m.get("model_name"))
        print("  Accuracy:", m.get("overall_accuracy"))
        print("  F1:", m.get("f1_contradiction"))
elif "case_level_results" in d:
    for c in d["case_level_results"]:
        print(c.get("case_id"), c.get("gold_label"), c.get("predicted_label"))
else:
    print(str(d)[:500])

