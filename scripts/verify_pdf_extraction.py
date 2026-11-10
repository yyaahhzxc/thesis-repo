import pypdf
from pathlib import Path

pdf_dir = Path("src/demo/sample_cases/pdf")
files = [
    "01_mosqueda_aerial_spraying_ban.pdf",
    "02_evasco_billboard_regulation.pdf",
    "03_arc_investors_holding_tax.pdf",
    "04_first_meridian_payment_under_protest.pdf",
    "05_davao_gsis_property_tax.pdf",
    "06_mining_ban_watershed.pdf",
    "07_davao_anti_smoking_stricter_standard.pdf",
    "08_davao_speed_limits_traffic_code.pdf",
    "09_magtajas_casino_preemption.pdf",
    "10_city_of_manila_laguio_due_process.pdf"
]

print(f"{'PDF File':<45} | {'Pages':<6} | {'Words Extracted':<15}")
print("-" * 75)
for f in files:
    p = pdf_dir / f
    if not p.exists():
        print(f"{f:<45} | MISSING")
        continue
    reader = pypdf.PdfReader(str(p))
    total_words = sum(len(page.extract_text().split()) for page in reader.pages)
    print(f"{f:<45} | {len(reader.pages):<6} | {total_words:<15,}")

