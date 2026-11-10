import json

with open("src/demo/sample_cases/01_mosqueda_aerial_spraying_ban.json", "r", encoding="utf-8") as f:
    d = json.load(f)

for s in d.get("sections", []):
    print(f"[{s.get('number')}] {s.get('heading')}: {s.get('text')[:80]}...")

