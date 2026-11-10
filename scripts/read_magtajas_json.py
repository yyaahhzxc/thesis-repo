import json

with open("src/demo/sample_cases/09_magtajas_casino_preemption.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Title:", data.get("title"))
print("File:", data.get("file"))
for s in data.get("sections", []):
    print(f"[{s.get('number')}] {s.get('heading')}: {s.get('text')}")

