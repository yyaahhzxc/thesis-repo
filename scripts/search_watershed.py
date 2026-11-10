import json

with open('corpus/city_ordinances/categorized_davao_ordinances.jsonl', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if any(k in line for k in ["0310-07", "0310_07", "Panigan-Tamugan", "Watershed Protection", "mining"]):
            try:
                d = json.loads(line)
                print(f"Line {idx+1}: ID={d.get('ordinance_id')} | Title={d.get('title')[:75]} | Secs={len(d.get('sections', []))}")
            except Exception:
                pass

