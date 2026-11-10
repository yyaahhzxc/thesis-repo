import json

targets = ["0309-07", "092-2000", "0158-05", "158-05", "0310-07", "0367-12", "0270-23", "3353", "7783", "210", "GSIS"]
counts = {t: 0 for t in targets}
examples = {t: [] for t in targets}

with open("data/unified_dual_statutory_provisions.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        for t in targets:
            if t in line:
                counts[t] += 1
                if len(examples[t]) < 2:
                    d = json.loads(line)
                    examples[t].append(d.get("citation") or d.get("id"))

print("Occurrences in data/unified_dual_statutory_provisions.jsonl:")
for t, c in counts.items():
    print(f"Target '{t}': {c} provisions | Examples: {examples[t]}")

