import os
from pathlib import Path

dirs_to_check = [
    Path("corpus/cleaned/local/cleaned_transcriptions"),
    Path("ground_truth"),
    Path("src/demo"),
    Path("data")
]

print("Scanning specific directories for 0310-07...")
for d in dirs_to_check:
    for fp in d.rglob("*"):
        if fp.is_file() and fp.suffix in [".txt", ".json"]:
            if "0310" in fp.name or "watershed" in fp.name.lower():
                print(f"  {fp} ({fp.stat().st_size:,} bytes)")

