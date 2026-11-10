import re
import json
from pathlib import Path

txt_path = Path("corpus/cleaned/local/cleaned_transcriptions/landmark_ordinances/Ordinance No. 0158-05.txt")
raw_text = txt_path.read_text(encoding="utf-8")

# Pattern for sections in Ordinance No. 0158-05
# Example: "Section 69. Imposition of Tax. - There is hereby imposed..."
# or "Section 423. Payment Under Protest. - No protest shall be..."
sec_pattern = re.compile(r'(?:^|\n)(?:SECTION|Section|SEC\.)\s+(\d+[A-Za-z]?)\.?\s*([^\n\-\–\—]+)?\s*[\-\–\—\.]?\s*', re.MULTILINE)

matches = list(sec_pattern.finditer(raw_text))
print(f"Total section matches found in text: {len(matches)}")

sections = []
for idx, m in enumerate(matches):
    sec_num_str = m.group(1)
    sec_title = (m.group(2) or "").strip().rstrip(".-–— ")
    start_pos = m.end()
    end_pos = matches[idx + 1].start() if idx + 1 < len(matches) else len(raw_text)
    body_text = raw_text[start_pos:end_pos].strip()
    
    # Clean page headers / footers from OCR
    body_text = re.sub(r'---\s*\[Page\s*\d+\]\s*---', '', body_text)
    body_text = re.sub(r'The 2005 Revenue Code of the City of Davao', '', body_text)
    body_text = re.sub(r'Page\s*\d+', '', body_text)
    body_text = body_text.strip()
    
    sections.append({
        "sec_num": sec_num_str,
        "sec_title": sec_title if sec_title else "Operative Provision",
        "text": body_text[:200]  # snippet
    })

print(f"Extracted {len(sections)} sections.")
print("Sample extracted sections:")
for s in sections[:5]:
    print(f"  Sec {s['sec_num']}: {s['sec_title']} -> {s['text'][:60]}...")

print("\nKey target sections:")
for s in sections:
    if s['sec_num'] in ['69', '135', '423', '424']:
        print(f"  Sec {s['sec_num']}: {s['sec_title']} -> {s['text'][:80]}...")

