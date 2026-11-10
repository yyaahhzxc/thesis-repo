import os
from pathlib import Path

repo_root = Path(".")

print("Searching for files mentioning 0310-07...")
for root, dirs, files in os.walk("."):
    if ".git" in root or "venv" in root or "__pycache__" in root:
        continue
    for f in files:
        if f.endswith((".txt", ".json", ".md", ".jsonl")):
            fp = Path(root) / f
            try:
                content = fp.read_text(encoding="utf-8", errors="ignore")
                if "0310-07" in content or "0310_07" in content:
                    print(f"  Found in {fp} (size: {fp.stat().st_size:,} bytes)")
            except Exception:
                pass

