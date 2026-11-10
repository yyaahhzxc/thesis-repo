from pathlib import Path

p = Path("corpus/cleaned/local/cleaned_transcriptions/landmark_ordinances/Ordinance No. 0158-05.txt")
text = p.read_text(encoding="utf-8")

lines = text.splitlines()
for i, line in enumerate(lines):
    if "SECTION 69" in line.upper() or "SEC. 69" in line.upper():
        print(f"Line {i+1}: {line}")
        for k in range(i, min(len(lines), i + 25)):
            print("  ", lines[k])
        print("=" * 60)
        break

for i, line in enumerate(lines):
    if "SECTION 423" in line.upper() or "SEC. 423" in line.upper():
        print(f"Line {i+1}: {line}")
        for k in range(i, min(len(lines), i + 20)):
            print("  ", lines[k])
        print("=" * 60)
        break

