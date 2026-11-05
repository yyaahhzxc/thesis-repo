import os
import sys
import time
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "corpus" / "city_ordinances" / "City Ordinances (2020-2017)"
OUTPUT_DIR = BASE_DIR / "kaggle"
OUTPUT_ZIP = OUTPUT_DIR / "city_ordinances_2020_2017.zip"

def main():
    if not INPUT_DIR.exists():
        print(f"[-] Error: Input directory not found: {INPUT_DIR}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(INPUT_DIR.rglob("*.pdf"))
    if not pdf_files:
        print(f"[-] Error: No PDF files found in: {INPUT_DIR}")
        sys.exit(1)

    total_bytes = sum(f.stat().st_size for f in pdf_files)
    print("=" * 65)
    print("  Kaggle Dataset Packager - Davao City Ordinances (2020-2017)")
    print("=" * 65)
    print(f"[*] Found:       {len(pdf_files)} PDF files")
    print(f"[*] Total Size:  {total_bytes / (1024 * 1024):.1f} MB ({total_bytes / (1024 * 1024 * 1024):.2f} GB)")
    print(f"[*] Target Zip:  {OUTPUT_ZIP}")
    print("=" * 65)
    print("[*] Packing files into zip archive (preserving year folders)...")

    start_time = time.time()
    # Using compresslevel=1 for speed; PDFs contain compressed streams already
    with zipfile.ZipFile(OUTPUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as zf:
        for idx, pdf_path in enumerate(pdf_files, 1):
            rel_path = pdf_path.relative_to(INPUT_DIR)
            zf.write(pdf_path, arcname=str(rel_path))
            if idx % 25 == 0 or idx == len(pdf_files):
                print(f"    -> [{idx}/{len(pdf_files)}] Packed: {rel_path}")

    elapsed = time.time() - start_time
    zip_size = OUTPUT_ZIP.stat().st_size
    print("\n" + "=" * 65)
    print(f"[OK] Successfully created Kaggle dataset archive!")
    print(f"[OK] Location:   {OUTPUT_ZIP}")
    print(f"[OK] Zip Size:   {zip_size / (1024 * 1024):.1f} MB")
    print(f"[OK] Time Taken: {elapsed:.1f} seconds")
    print("=" * 65)
    print("\nNext Steps:")
    print("1. Go to https://www.kaggle.com/datasets -> Click 'New Dataset'")
    print("2. Drag & drop the generated zip file: city_ordinances_2020_2017.zip")
    print("3. Title: davao-ordinances-2020-2017")
    print("4. Set Visibility to 'Private' and click 'Create'.")

if __name__ == "__main__":
    main()
