import json

with open("corpus/city_ordinances/categorized_davao_ordinances.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        title = data.get("title", "")
        if "panigan-tamugan" in title.lower() or "recreational activities within watershed" in title.lower():
            print("="*60)
            print("Title:", title)
            print("Ordinance No:", data.get("ordinance_no"))
            print("Series:", data.get("series"))
            print("Text sample:", data.get("text", "")[:500])
            print("Total length:", len(data.get("text", "")))

