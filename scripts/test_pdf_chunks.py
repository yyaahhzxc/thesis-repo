import pypdf
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
from src.demo.app import chunk_ordinance_sections

cases = [
    ("DAVAO-TIER3-01", "01_mosqueda_aerial_spraying_ban.pdf"),
    ("DAVAO-TIER3-02", "02_evasco_billboard_regulation.pdf"),
    ("DAVAO-TIER3-03", "03_arc_investors_holding_tax.pdf"),
    ("DAVAO-TIER3-04", "04_first_meridian_payment_under_protest.pdf"),
    ("DAVAO-TIER3-05", "05_davao_gsis_property_tax.pdf"),
    ("DAVAO-TIER3-06", "06_mining_ban_watershed.pdf"),
    ("DAVAO-TIER3-07", "07_davao_anti_smoking_stricter_standard.pdf"),
    ("DAVAO-TIER3-08", "08_davao_speed_limits_traffic_code.pdf"),
    ("SC-PHIL-09", "09_magtajas_casino_preemption.pdf"),
    ("SC-PHIL-10", "10_city_of_manila_laguio_due_process.pdf"),
]

for cid, name in cases:
    p = REPO_ROOT / "src" / "demo" / "sample_cases" / "pdf" / name
    reader = pypdf.PdfReader(str(p))
    raw = "\n\n".join(page.extract_text() or "" for page in reader.pages).strip()
    title, chunks = chunk_ordinance_sections(raw, name)
    sub = [c for c in chunks if not c.get("is_boilerplate")]
    print(f"{cid} ({name}): {len(chunks)} total sections ({len(sub)} substantive)")
