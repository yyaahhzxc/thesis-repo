import csv
import re
import argparse
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_TRANSCRIPT_DIR = BASE_DIR / "vlm_transcriptions"
CLEANED_TRANSCRIPT_DIR = BASE_DIR / "cleaned_transcriptions"
DEFAULT_REPORT_PATH = BASE_DIR / "transcript_quality_report.csv"

# Regex patterns for quality and anomaly detection
PATTERNS = {
    "foreign_script_hallucination": r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af\u0600-\u06ff\u0400-\u04ff]",
    "replacement_character": r"\ufffd",
    "undefined": r"\bundefined\b",
    "placeholder": r"\b(?:TODO|TBD|LOREM IPSUM)\b",
    "vlm_repetition_loop": r"(?:\b\d+\s+){8,}\b",
    "repeated_word": r"\b(?!x+\b|no\b|page\b|section\b|ord\b)(\w{2,})(?:\s+\1){3,}\b",
    # Protects markdown table frames (|---|, |:---:|), box drawing (+, =), headers (#), and common punctuation
    "repeated_character": r"(?:([A-Za-z0-9])\1{7,}|([^A-Za-z0-9\s|_\-=.+:*#])\2{5,})",
    "broken_number": r"\b\d+[A-Za-z]{4,}\d+\b",
    # Characters outside valid English/Latin, Filipino/Spanish accents, common punctuation, legal signs (₱, §, ¶, °, etc.), and box tables
    "ocr_garbage": r"[^\x09\x0a\x0d\x20-\x7e\u00a0-\u024f\u2000-\u206f\u20a0-\u20cf\u2100-\u214f\u2150-\u218f\u2190-\u21ff\u2200-\u22ff\u2500-\u259f\u25a0-\u25ff\u2700-\u27bf]",
}

def get_line_number(text, position):
    return text.count("\n", 0, position) + 1

def scan_file(path):
    issues = []
    text = path.read_text(encoding="utf-8", errors="replace")

    if not text.strip():
        issues.append(("empty_file", 1, "File is empty"))
        return issues

    if len(text.strip()) < 150:
        issues.append(("very_short_file", 1, text.strip()[:100]))

    # Check page markers on the complete document
    page_markers = [
        int(number)
        for number in re.findall(r"--- \[Page (\d+)\] ---", text)
    ]

    if not page_markers:
        issues.append(("missing_page_markers", 1, "No page markers found in file"))
    else:
        # Check if sequence is strictly increasing and contiguous
        # Permits documents starting at Page 2 when front-matter/cover roster was skipped
        is_contiguous = all(b - a == 1 for a, b in zip(page_markers, page_markers[1:]))
        starts_valid = len(page_markers) > 0 and page_markers[0] in [1, 2]
        if not (is_contiguous and starts_valid):
            issues.append(
                (
                    "page_sequence_problem",
                    1,
                    f"Found {page_markers}; expected contiguous sequence starting at 1 or 2",
                )
            )


    # Check for anomalies and quality flags
    for issue_type, pattern in PATTERNS.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            line_number = get_line_number(text, match.start())
            start_pos = max(0, match.start() - 50)
            end_pos = min(len(text), match.end() + 50)
            excerpt = " ".join(text[start_pos:end_pos].split())
            issues.append((issue_type, line_number, excerpt))

    return issues

def main():
    parser = argparse.ArgumentParser(description="Audit quality of ordinance transcriptions.")
    parser.add_argument(
        "--cleaned",
        action="store_true",
        help="Audit the cleaned_transcriptions directory instead of raw vlm_transcriptions",
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=None,
        help="Custom directory of transcriptions to audit",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Custom output CSV report path",
    )
    args = parser.parse_args()

    if args.dir:
        transcript_dir = Path(args.dir).resolve()
    elif args.cleaned:
        transcript_dir = CLEANED_TRANSCRIPT_DIR
    else:
        transcript_dir = DEFAULT_TRANSCRIPT_DIR

    report_path = Path(args.output).resolve() if args.output else DEFAULT_REPORT_PATH

    txt_files = sorted(transcript_dir.rglob("*.txt"))

    if not txt_files:
        raise SystemExit(f"No TXT files found in {transcript_dir}")

    rows = []
    issue_counts = Counter()
    files_with_issues = set()

    for path in txt_files:
        issues = scan_file(path)
        if issues:
            files_with_issues.add(path)
            for issue_type, line_number, excerpt in issues:
                issue_counts[issue_type] += 1
                rows.append(
                    {
                        "file": str(path.relative_to(BASE_DIR)),
                        "issue": issue_type,
                        "line": line_number,
                        "excerpt": excerpt,
                    }
                )

    with report_path.open("w", newline="", encoding="utf-8") as report:
        writer = csv.DictWriter(
            report,
            fieldnames=["file", "issue", "line", "excerpt"],
        )
        writer.writeheader()
        writer.writerows(rows)

    clean_files = len(txt_files) - len(files_with_issues)
    pass_rate = (clean_files / len(txt_files)) * 100

    print("=" * 60)
    print("           TRANSCRIPT QUALITY AUDIT REPORT")
    print("=" * 60)
    print(f"Target Directory:        {transcript_dir.name}")
    print(f"Total Scanned Files:     {len(txt_files)}")
    print(f"Clean (Passed) Files:    {clean_files} ({pass_rate:.1f}%)")
    print(f"Flagged Files:           {len(files_with_issues)} ({100 - pass_rate:.1f}%)")
    print(f"Total Issues Flagged:    {len(rows)}")
    print("-" * 60)
    if issue_counts:
        print("Issue Breakdown:")
        for issue, count in issue_counts.most_common():
            print(f"  - {issue:<30}: {count:>5}")
    else:
        print("  All files passed with 0 issues!")
    print("=" * 60)
    print(f"Full Report Saved To: {report_path}\n")

if __name__ == "__main__":
    main()