import json
import pypdf
from pathlib import Path

pdf_dir = Path("ground_truth/tier3_sc_cases/tier3_landmark_ordinances_pdf")
sample_json_dir = Path("src/demo/sample_cases")

print("=" * 80)
print("AUDIT OF ALL 10 AUTHENTIC TIER 3 ENROLLED DOCUMENTS")
print("=" * 80)

files = [
    ("DAVAO-01", "01_mosqueda_aerial_spraying_ban.pdf", "01_mosqueda_aerial_spraying_ban.json"),
    ("DAVAO-02", "02_evasco_billboard_regulation.pdf", "02_evasco_billboard_regulation.json"),
    ("DAVAO-03", "03_arc_investors_holding_tax.pdf", "03_arc_investors_holding_tax.json"),
    ("DAVAO-04", "04_first_meridian_payment_under_protest.pdf", "04_first_meridian_payment_under_protest.json"),
    ("DAVAO-05", "05_davao_gsis_property_tax.pdf", "05_davao_gsis_property_tax.json"),
    ("DAVAO-06", "06_mining_ban_watershed.pdf", "06_mining_ban_watershed.json"),
    ("DAVAO-07", "07_davao_anti_smoking_stricter_standard.pdf", "07_davao_anti_smoking_stricter_standard.json"),
    ("DAVAO-08", "08_davao_speed_limits_traffic_code.pdf", "08_davao_speed_limits_traffic_code.json"),
    ("SC-PHIL-09", "09_magtajas_casino_preemption.pdf", "09_magtajas_casino_preemption.json"),
    ("SC-PHIL-10", "10_city_of_manila_laguio_due_process.pdf", "10_city_of_manila_laguio_due_process.json")
]

for cid, pdf_name, json_name in files:
    pdf_path = pdf_dir / pdf_name
    json_path = sample_json_dir / json_name
    
    pages = 0
    chars = 0
    if pdf_path.exists():
        reader = pypdf.PdfReader(str(pdf_path))
        pages = len(reader.pages)
        chars = len("".join(p.extract_text() or "" for p in reader.pages))
        
    secs = 0
    if json_path.exists():
        jd = json.loads(json_path.read_text(encoding="utf-8"))
        secs = len(jd.get("sections", []))
        
    print(f"{cid:<12} | {pdf_name:<42} | Pages: {pages:>3} | Chars: {chars:>7,} | Sections: {secs:>3}")
print("=" * 80)

