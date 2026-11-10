import json
from collections import Counter

categories = Counter()
law_id_prefixes = Counter()

with open("corpus/categorized_national_laws.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        cat = data.get("category")
        categories[cat] += 1
        law_id = data.get("law_id", "")
        prefix = law_id.split("_")[0] if "_" in law_id else "unknown"
        law_id_prefixes[prefix] += 1

print("Categories in categorized_national_laws:")
for c, cnt in categories.most_common():
    print(f"  {c}: {cnt}")

print("\nLaw ID prefixes:")
for p, cnt in law_id_prefixes.most_common():
    print(f"  {p}: {cnt}")
