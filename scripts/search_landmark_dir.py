from pathlib import Path

landmark_dir = Path("corpus/cleaned/local/cleaned_transcriptions/landmark_ordinances")
targets = ["0158", "158", "0310", "310", "0309", "309", "092", "0367", "0270"]

print("Matches in landmark_ordinances:")
for f in landmark_dir.glob("*.txt"):
    for t in targets:
        if t in f.name:
            print(f"  {f.name} (size: {f.stat().st_size:,} bytes)")

