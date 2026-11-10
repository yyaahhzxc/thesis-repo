import json
import re

print("=== 1. Sample amendments in Davao Ordinances ===")
with open("corpus/city_ordinances/categorized_davao_ordinances.jsonl", "r", encoding="utf-8") as f:
    count = 0
    for line in f:
        data = json.loads(line)
        text = data.get("full_text", "")
        m = re.search(r"([^.\n]*?(?:hereby\s+amended|is\s+amended|hereby\s+repealed)[^.\n]*)", text, re.IGNORECASE)
        if m:
            print(f"{data.get('ordinance_number')}: {m.group(1).strip()[:140]}")
            count += 1
            if count >= 6: break

print("\n=== 2. Sample amendments in National Laws ===")
with open("corpus/categorized_national_laws.jsonl", "r", encoding="utf-8") as f:
    count = 0
    for line in f:
        data = json.loads(line)
        text = data.get("full_text", "")
        m = re.search(r"([^.\n]*?(?:hereby\s+amended|is\s+amended|hereby\s+repealed)[^.\n]*)", text, re.IGNORECASE)
        if m:
            print(f"{data.get('law_number')}: {m.group(1).strip()[:140]}")
            count += 1
            if count >= 6: break

