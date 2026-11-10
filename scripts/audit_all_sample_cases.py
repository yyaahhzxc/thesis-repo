import json, os

cases_dir = "src/demo/sample_cases"
files = sorted([f for f in os.listdir(cases_dir) if f.endswith(".json")])

print(f"{'File':<40} | {'Sections':<8} | {'Total Words':<12} | {'Avg Words/Sec':<14} | {'Status'}")
print("-" * 90)

for f in files:
    path = os.path.join(cases_dir, f)
    with open(path, "r", encoding="utf-8") as fp:
        d = json.load(fp)
    sections = d.get("sections", [])
    total_words = sum(len(s.get("text", "").split()) for s in sections)
    avg_words = total_words / max(1, len(sections))
    status = "REAL FULL TEXT" if total_words > 1000 and len(sections) > 8 else "SYNTHETIC / TRUNCATED"
    print(f"{f:<40} | {len(sections):<8} | {total_words:<12} | {avg_words:<14.1f} | {status}")

