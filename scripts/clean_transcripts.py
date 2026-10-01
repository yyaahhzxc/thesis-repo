import os
import re
import csv
import shutil
import unicodedata
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "vlm_transcriptions"
OUTPUT_DIR = BASE_DIR / "cleaned_transcriptions"
REVIEW_QUEUE_DIR = BASE_DIR / "review_queue"
CLEANING_REPORT = BASE_DIR / "cleaning_summary_report.csv"

# Regex patterns for cleaning
# 1. Foreign script hallucinations (CJK, Cyrillic, Arabic, etc.)
RE_FOREIGN_SCRIPTS = re.compile(
    r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af\u0600-\u06ff\u0400-\u04ff]"
)

# 2. VLM prompt artifacts like "**正文:**" or "正文:"
RE_VLM_PROMPT_ARTIFACTS = re.compile(
    r"\*{0,2}正文\*{0,2}:?\s*", re.IGNORECASE
)

# 3. Collapsing runaway single-character repetition loops (e.g., "0000000000000000" -> "000")
# Threshold set to 7 to prevent altering valid padded numbers, serials, or survey coordinates
RE_REPEATED_ALPHANUM = re.compile(r"([A-Za-z0-9])\1{7,}")

# 4. Collapsing runaway word/token repetitions (e.g., "1 1 1 1 1 1 1..." or "Councillor Councillor Councillor...")
# Excludes legal ellipsis notation 'xxx' and structural keywords ('no', 'page', 'section', 'ord')
RE_REPEATED_WORDS = re.compile(
    r"\b(?!x+\b|no\b|page\b|section\b|ord\b)(\w+)(?:\s+\1){3,}\b", re.IGNORECASE
)


# 5. Invisible / Zero-width characters & non-breaking spaces
RE_ZERO_WIDTH = re.compile(r"[\u200b\u200c\u200d\u200e\u200f\ufeff]")

# 6. Excess blank lines (3 or more -> 2)
RE_EXCESS_NEWLINES = re.compile(r"\n{3,}")

def clean_text(raw_text: str):
    stats = Counter()
    cleaned = raw_text

    # Step 1: Normalize Unicode (NFKC) & non-breaking spaces
    cleaned = unicodedata.normalize("NFKC", cleaned)
    cleaned = cleaned.replace("\u00a0", " ")

    # Step 2: Remove zero-width characters
    if RE_ZERO_WIDTH.search(cleaned):
        stats["removed_zero_width_chars"] += 1
        cleaned = RE_ZERO_WIDTH.sub("", cleaned)

    # Step 3: Remove VLM Prompt Artifacts
    if RE_VLM_PROMPT_ARTIFACTS.search(cleaned):
        stats["removed_prompt_artifacts"] += 1
        cleaned = RE_VLM_PROMPT_ARTIFACTS.sub("", cleaned)

    # Step 4: Remove stray foreign script hallucinations
    foreign_matches = RE_FOREIGN_SCRIPTS.findall(cleaned)
    if foreign_matches:
        stats["removed_foreign_scripts"] += len(foreign_matches)
        cleaned = RE_FOREIGN_SCRIPTS.sub("", cleaned)

    # Step 5: Collapse runaway character loops (e.g. 10000000000000000 -> 1000)
    def collapse_char_match(match):
        stats["collapsed_char_loops"] += 1
        char = match.group(1)
        return char * 3

    cleaned = RE_REPEATED_ALPHANUM.sub(collapse_char_match, cleaned)

    # Step 6: Collapse repeated word/token loops (e.g. "1 1 1 1 1 1 1..." or "Councillor Councillor...")
    def collapse_word_loop(match):
        stats["collapsed_word_loops"] += 1
        word = match.group(1)
        return word

    cleaned = RE_REPEATED_WORDS.sub(collapse_word_loop, cleaned)

    # Step 7: Line-by-line whitespace trim and excessive newline collapse
    lines = [line.rstrip() for line in cleaned.split("\n")]
    cleaned = "\n".join(lines)
    cleaned = RE_EXCESS_NEWLINES.sub("\n\n", cleaned).strip() + "\n"

    return cleaned, stats

def main():
    txt_files = sorted(INPUT_DIR.rglob("*.txt"))
    if not txt_files:
        raise SystemExit(f"No text files found in {INPUT_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_QUEUE_DIR.mkdir(parents=True, exist_ok=True)

    summary_rows = []
    total_modifications = 0
    flagged_for_review = 0

    print(f"[*] Starting Automated Cleanup for {len(txt_files)} transcript files...")

    for path in txt_files:
        relative_path = path.relative_to(INPUT_DIR)
        out_path = OUTPUT_DIR / relative_path
        out_path.parent.mkdir(parents=True, exist_ok=True)

        raw_text = path.read_text(encoding="utf-8", errors="replace")
        cleaned_text, stats = clean_text(raw_text)

        out_path.write_text(cleaned_text, encoding="utf-8")

        # Track meaningful fixes
        meaningful_fixes = (
            stats.get("collapsed_char_loops", 0)
            + stats.get("collapsed_word_loops", 0)
            + stats.get("removed_foreign_scripts", 0)
            + stats.get("removed_prompt_artifacts", 0)
            + stats.get("removed_zero_width_chars", 0)
        )

        if meaningful_fixes > 0:
            total_modifications += 1

        # Check if file has severe issues warranting spot review
        needs_review = (
            stats.get("removed_prompt_artifacts", 0) > 0
            or stats.get("removed_foreign_scripts", 0) > 2
            or stats.get("collapsed_word_loops", 0) > 2
            or len(cleaned_text.strip()) < 150
        )

        if needs_review:
            flagged_for_review += 1
            review_raw = REVIEW_QUEUE_DIR / f"RAW_{relative_path.name}"
            review_cleaned = REVIEW_QUEUE_DIR / f"CLEANED_{relative_path.name}"
            shutil.copy2(path, review_raw)
            shutil.copy2(out_path, review_cleaned)

        summary_rows.append(
            {
                "file": str(relative_path),
                "fixed": "YES" if meaningful_fixes > 0 else "NO",
                "total_fixes": meaningful_fixes,
                "needs_review": "YES" if needs_review else "NO",
                "details": "; ".join(f"{k}={v}" for k, v in stats.items()) if stats else "clean",
            }
        )

    # Write summary CSV
    with CLEANING_REPORT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["file", "fixed", "total_fixes", "needs_review", "details"],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    print("=" * 60)
    print("           DATA CLEANUP EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Total Files Processed:       {len(txt_files)}")
    print(f"Files Modified with Fixes:   {total_modifications}")
    print(f"Files Already Clean:         {len(txt_files) - total_modifications}")
    print(f"Files in Review Queue:       {flagged_for_review} (Saved to review_queue/)")
    print(f"Clean Output Directory:      {OUTPUT_DIR}")
    print(f"Summary Report Saved To:     {CLEANING_REPORT}")
    print("=" * 60)

if __name__ == "__main__":
    main()
