from pathlib import Path

p1 = Path("ground_truth/tier3_sc_cases/davao_city_tier3_ordinances/Ordinance_No._0309-07.txt")
p2 = Path("ground_truth/tier3_sc_cases/davao_city_tier3_ordinances/Ordinance_No._0310-07.txt")

if p1.exists():
    print("=== Ordinance_No._0309-07.txt ===")
    print(p1.read_text(encoding="utf-8")[:1200])

if p2.exists():
    print("\n=== Ordinance_No._0310-07.txt ===")
    print(p2.read_text(encoding="utf-8")[:1200])

