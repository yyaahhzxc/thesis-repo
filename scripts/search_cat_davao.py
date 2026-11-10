import json

with open("corpus/city_ordinances/categorized_davao_ordinances.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        title = data.get("title", "")
        ord_no = data.get("ordinance_no", "")
        if "watershed" in title.lower() or "0310" in ord_no or "aerial" in title.lower():
            print(f"Match: ord_no={ord_no} | title={title[:80]}")

