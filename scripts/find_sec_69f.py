from pathlib import Path

p = Path("corpus/cleaned/local/cleaned_transcriptions/landmark_ordinances/Ordinance No. 0158-05.txt")
lines = p.read_text(encoding="utf-8").splitlines()

for i in range(1637, min(len(lines), 2000)):
    if "(f)" in lines[i] or "Banks" in lines[i] or "financial" in lines[i].lower():
        print(f"Line {i+1}: {lines[i]}")
        for k in range(max(0, i-2), min(len(lines), i+10)):
            print("  ", lines[k])
        print("-" * 50)
        break

