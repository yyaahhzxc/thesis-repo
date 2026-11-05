import os
import sys
import shutil
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET_TXT_DIR = BASE_DIR / "vlm_transcriptions"
KAGGLE_DIR = BASE_DIR / "kaggle"

def find_zip_file():
    # Check in kaggle folder first
    candidates = list(KAGGLE_DIR.glob("*.zip"))
    
    # Also check user's Windows Downloads directory
    user_home = Path.home()
    downloads_dir = user_home / "Downloads"
    if downloads_dir.exists():
        candidates += list(downloads_dir.glob("*transcription*.zip"))
        candidates += list(downloads_dir.glob("*vlm*.zip"))
    
    for c in candidates:
        if "transcription" in c.name.lower() or "vlm" in c.name.lower() or "2020" in c.name:
            return c
    return None

def main():
    print("=" * 65)
    print("  Kaggle Results Integrator - Davao City Ordinances")
    print("=" * 65)

    zip_path = None
    if len(sys.argv) > 1:
        zip_path = Path(sys.argv[1])
    else:
        zip_path = find_zip_file()

    if not zip_path or not zip_path.exists():
        print("[-] Could not automatically find the Kaggle transcript zip file.")
        print("[-] Please provide the path to your downloaded zip:")
        print("    python kaggle/integrate_results.py \"path/to/vlm_transcriptions_2020_2017.zip\"")
        sys.exit(1)

    print(f"[*] Found transcript archive: {zip_path}")
    print(f"[*] Target Directory:        {TARGET_TXT_DIR}")

    TARGET_TXT_DIR.mkdir(parents=True, exist_ok=True)

    extracted_count = 0
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.infolist():
            if member.is_dir() or not member.filename.lower().endswith(".txt"):
                continue
            
            # Normalize path: strip leading 'vlm_transcriptions/' or 'working/' if present
            parts = Path(member.filename).parts
            if "vlm_transcriptions" in parts:
                idx = parts.index("vlm_transcriptions")
                rel_parts = parts[idx + 1:]
            else:
                rel_parts = parts

            dest_path = TARGET_TXT_DIR.joinpath(*rel_parts)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            with zf.open(member) as source, open(dest_path, "wb") as target:
                shutil.copyfileobj(source, target)
            extracted_count += 1

    print(f"\n[OK] Successfully extracted {extracted_count} transcript files into {TARGET_TXT_DIR}!")

    # Check updated inventory
    all_txt = list(TARGET_TXT_DIR.rglob("*.txt"))
    years_found = sorted({p.parent.name for p in all_txt if p.parent.name.isdigit()})
    print("\n" + "=" * 65)
    print("           CURRENT INVENTORY OF TRANSCRIPTIONS")
    print("=" * 65)
    print(f"Total Transcripts Available: {len(all_txt)}")
    print(f"Years Included:              {', '.join(years_found)}")
    print("=" * 65)
    print("\nNext steps:")
    print("1. Run cleaning pipeline:  python clean_transcripts.py")
    print("2. Run audit pipeline:     python audit_transcripts.py")

if __name__ == "__main__":
    main()
