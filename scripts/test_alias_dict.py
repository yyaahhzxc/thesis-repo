import json
import re

# Build mapping from (type, number) -> canonical enactment_id
enactment_map = {}

# 1. National Laws
with open("corpus/categorized_national_laws.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        law_id = data["law_id"]
        cat = data.get("category", "")
        # law_id is like ra_7160_1991, pd_1144_1977, etc.
        parts = law_id.split("_")
        prefix = parts[0]
        # extract number from parts or law_number
        law_num = data.get("law_number", "")
        m = re.search(r'(\d+)', law_num)
        if m:
            num = int(m.group(1))
            enactment_map[(prefix, num)] = law_id

print(f"Total national laws mapped: {len(enactment_map)}")
print("Sample lookups:")
print("  ('ra', 7160) ->", enactment_map.get(('ra', 7160)))
print("  ('pd', 1144) ->", enactment_map.get(('pd', 1144)))
print("  ('bp', 129)  ->", enactment_map.get(('bp', 129)))
print("  ('eo', 292)  ->", enactment_map.get(('eo', 292)))
print("  ('ca', 473)  ->", enactment_map.get(('ca', 473)))
print("  ('act', 3815)->", enactment_map.get(('act', 3815)))

# 2. Local Ordinances
ordinance_map = {}
with open("corpus/city_ordinances/categorized_davao_ordinances.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        ord_id = data["ordinance_id"]
        ord_num = data.get("ordinance_number", "").strip().lower()
        if ord_num:
            ordinance_map[ord_num] = ord_id
            # normalize variants like 0309-07 vs 309-07
            parts = ord_num.split("-")
            if len(parts) == 2:
                norm = f"{int(parts[0]) if parts[0].isdigit() else parts[0]}-{parts[1]}"
                ordinance_map[norm] = ord_id

print(f"Total local ordinances mapped: {len(ordinance_map)}")
print("Sample lookup:")
print("  '0309-07' ->", ordinance_map.get('0309-07'))
print("  '158-05'  ->", ordinance_map.get('158-05'))
print("  '0270-23' ->", ordinance_map.get('0270-23'))

