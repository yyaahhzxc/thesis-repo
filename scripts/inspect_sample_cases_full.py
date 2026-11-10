import json
from pathlib import Path

sample_cases_dir = Path("src/demo/sample_cases")
for jf in sorted(sample_cases_dir.glob("*.json")):
    with open(jf, "r", encoding="utf-8") as f:
        d = json.load(f)
    secs = d.get("sections", [])
    sec_nums = [s.get("sec_num") for s in secs]
    total_words = sum(len(s.get("text", "").split()) for s in secs)
    print(f"File: {jf.name}")
    print(f"  Title: {d.get('title', '')[:70]}")
    print(f"  Total sections: {len(secs)} | Sec nums: {sec_nums}")
    print(f"  Total words: {total_words}")
    print("-" * 60)

