from pathlib import Path

base_dir = Path("corpus/cleaned/local/cleaned_transcriptions")

for p in base_dir.rglob("*0309*"):
    print("Found 0309:", p, f"({p.stat().st_size:,} bytes)")

for p in base_dir.rglob("*0310*"):
    print("Found 0310:", p, f"({p.stat().st_size:,} bytes)")

for p in base_dir.rglob("*aerial*"):
    print("Found aerial:", p, f"({p.stat().st_size:,} bytes)")

for p in base_dir.rglob("*mining*"):
    print("Found mining:", p, f"({p.stat().st_size:,} bytes)")

