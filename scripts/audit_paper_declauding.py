#!/usr/bin/env python3
"""
Audit Paper Declauding (Anti-AI Writing Tics Auditor)
Scans LaTeX manuscript chapters against the universal declauding register rules
to catch sentence-ending participle tails, forced triads, copula avoidance,
slop buzzwords, and staged reveals.

Usage:
    python scripts/audit_paper_declauding.py
    python scripts/audit_paper_declauding.py --chapter results_and_discussion
    python scripts/audit_paper_declauding.py --file CS_Undergraduate_Thesis_Template/chapters/introduction.tex
"""

import argparse
import os
import sys
from pathlib import Path

# Add declauding script path to import declaude_lint RULES
SKILL_DIR = Path(".agents/skills/declauding")
LINT_SCRIPT = SKILL_DIR / "scripts" / "declaude_lint.py"

if not LINT_SCRIPT.exists():
    print(f"Error: Could not find linter at {LINT_SCRIPT}")
    sys.exit(1)

# Import the lint module dynamically
import importlib.util
spec = importlib.util.spec_from_file_location("declaude_lint", str(LINT_SCRIPT))
declaude_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(declaude_lint)

def scan_file(file_path: Path):
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    
    # Run the rules
    hits_by_category = {}
    detailed_hits = []
    
    for cat, pat, note in declaude_lint.RULES:
        # Regex search per line or paragraph
        flags = declaude_lint.re.IGNORECASE
        # Check multiline or line by line
        for line_num, line in enumerate(lines, 1):
            # Skip LaTeX comments or macro definitions
            clean_line = line.strip()
            if clean_line.startswith("%") or clean_line.startswith("\\newcommand") or clean_line.startswith("\\usepackage"):
                continue
            
            for m in declaude_lint.re.finditer(pat, line, flags):
                matched_text = m.group(0).strip()
                hits_by_category[cat] = hits_by_category.get(cat, 0) + 1
                detailed_hits.append({
                    "line": line_num,
                    "category": cat,
                    "matched": matched_text,
                    "note": note,
                    "full_line": line
                })
    
    return hits_by_category, detailed_hits

def main():
    parser = argparse.ArgumentParser(description="Audit thesis chapters for LLM writing tics.")
    parser.add_argument("--chapter", help="Specific chapter filename (without .tex)")
    parser.add_argument("--file", help="Specific file path to check")
    parser.add_argument("--include-appendices", action="store_true", help="Also audit appendices")
    args = parser.parse_args()

    repo_root = Path(".")
    chapters_dir = repo_root / "CS_Undergraduate_Thesis_Template" / "chapters"
    
    if args.file:
        files_to_check = [Path(args.file)]
    elif args.chapter:
        target = chapters_dir / f"{args.chapter}.tex"
        if not target.exists():
            target = repo_root / args.chapter
        files_to_check = [target]
    else:
        files_to_check = sorted(list(chapters_dir.glob("*.tex")))
        if args.include_appendices:
            appendices_dir = repo_root / "CS_Undergraduate_Thesis_Template" / "appendices"
            if appendices_dir.exists():
                files_to_check.extend(sorted(list(appendices_dir.glob("*.tex"))))

    print("=" * 80)
    print("THESIS MANUSCRIPT DECLAUDING & ANTI-AI TIC AUDIT")
    print("=" * 80)
    
    summary_rows = []
    total_candidates = 0
    
    categories = ["participle", "triad", "copula", "slop", "staging", "flat-certainty", "agency"]
    
    for f in files_to_check:
        if not f.exists():
            print(f"Skipping missing file: {f}")
            continue
            
        hits_by_cat, detailed = scan_file(f)
        file_total = sum(hits_by_cat.values())
        total_candidates += file_total
        
        row = {
            "file": f.name,
            "total": file_total
        }
        for c in categories:
            row[c] = hits_by_cat.get(c, 0)
        summary_rows.append((row, detailed))

    # Print summary table
    header = f"{'Chapter / File':<30} | {'Total':<6} | {'Participle':<10} | {'Triad':<6} | {'Copula':<7} | {'Slop':<5} | {'Staging':<7} | {'Certainty':<9}"
    print(header)
    print("-" * len(header))
    
    for row, _ in summary_rows:
        print(f"{row['file']:<30} | {row['total']:<6} | {row['participle']:<10} | {row['triad']:<6} | {row['copula']:<7} | {row['slop']:<5} | {row['staging']:<7} | {row['flat-certainty']:<9}")
    
    print("-" * len(header))
    print(f"{'OVERALL TOTAL':<30} | {total_candidates:<6}")
    print("=" * 80)
    
    # If single file checked or user requested details, print itemized lines
    if len(files_to_check) == 1:
        _, detailed = summary_rows[0]
        print(f"\nItemized Candidates for {files_to_check[0].name}:")
        for hit in detailed:
            print(f"  L{hit['line']:<4} [{hit['category']}] {hit['matched']} ({hit['note']})")
            print(f"        \"{hit['full_line'].strip()[:90]}...\"")
    else:
        print("\nTip: To see line-by-line candidates for a specific chapter, run:")
        print("     python scripts/audit_paper_declauding.py --chapter <name>")

if __name__ == "__main__":
    main()

