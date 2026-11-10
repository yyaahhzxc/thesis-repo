import json

for name in ["05_davao_gsis_property_tax.json", "06_mining_ban_watershed.json", "10_city_of_manila_laguio_due_process.json", "11_batangas_catv_cable_regulation.json"]:
    with open(f"src/demo/sample_cases/{name}", "r", encoding="utf-8") as f:
        d = json.load(f)
    print(f"=== {name} ===")
    for s in d.get("sections", []):
        print(f"[{s.get('number')}] {s.get('heading')}: {s.get('text')}")

