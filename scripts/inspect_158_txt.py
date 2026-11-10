from pathlib import Path

p = Path("corpus/cleaned/local/cleaned_transcriptions/landmark_ordinances/Ordinance No. 0158-05.txt")
lines = p.read_text(encoding="utf-8").splitlines()
print(f"Total lines in Ordinance No. 0158-05.txt: {len(lines):,}")
print("\nFirst 40 lines:")
for l in lines[:40]:
    print(l)

