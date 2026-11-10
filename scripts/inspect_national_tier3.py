import json
from pathlib import Path

sample_cases_dir = Path("src/demo/sample_cases")
for fname in ["09_magtajas_casino_preemption.json", "10_city_of_manila_laguio_due_process.json", "11_batangas_catv_cable_regulation.json"]:
    p = sample_cases_dir / fname
    if p.exists():
        d = json.loads(p.read_text(encoding="utf-8"))
        print(f"=== {fname} ===")
        print("Title:", d.get("title"))
        for s in d.get("sections", []):
            print(f"  Sec {s.get('sec_num')}: {s.get('sec_title')} - {s.get('text')[:90]}...")

