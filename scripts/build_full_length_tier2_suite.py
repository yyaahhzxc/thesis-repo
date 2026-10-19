"""
scripts/build_full_length_tier2_suite.py
========================================
Compiles the complete 10-draft Tier 2 Injected-Fault benchmark suite with
realistic corpus length (1,200 to 2,200 words per draft) and multi-paragraph
legislative text matching the empirical drafting patterns of the Sangguniang
Panlungsod of Davao City.

Writes:
- data/tier2_draft_ordinances/DRAFT-ORD-2026-01.json ... DRAFT-ORD-2026-10.json
- data/tier2_draft_ordinances_benchmark.jsonl
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "data" / "tier2_draft_ordinances"
BENCHMARK_PATH = REPO_ROOT / "data" / "tier2_draft_ordinances_benchmark.jsonl"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

import sys
sys.path.insert(0, str(REPO_ROOT))

# Import draft builders
from scripts.tier2_drafts_data import get_draft_01, get_draft_02, get_draft_03
from scripts.tier2_drafts_data_part2 import get_draft_04, get_draft_05, get_draft_06, get_draft_07
from scripts.tier2_drafts_data_part3 import get_draft_08, get_draft_09, get_draft_10


def build_suite():
    drafts = [
        get_draft_01(),
        get_draft_02(),
        get_draft_03(),
        get_draft_04(),
        get_draft_05(),
        get_draft_06(),
        get_draft_07(),
        get_draft_08(),
        get_draft_09(),
        get_draft_10(),
    ]

    print("=" * 80)
    print("COMPILING FULL-LENGTH TIER 2 DRAFT ORDINANCES SUITE")
    print("=" * 80)

    summary_rows = []
    total_sections = 0
    total_words = 0

    # Write individual JSON files
    for d in drafts:
        doc_id = d["doc_id"]
        sec_count = len(d["sections"])
        word_count = sum(len(s["text"].split()) for s in d["sections"])
        total_sections += sec_count
        total_words += word_count

        # Identify planted defect(s)
        defects = [s for s in d["sections"] if s.get("label") == "Contradiction"]
        defect_str = ", ".join([f"Sec {s['sec_num']} ({s.get('target_statute')})" for s in defects])

        # Write out formatted JSON file
        json_file = OUTPUT_DIR / f"{doc_id}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)

        summary_rows.append({
            "doc_id": doc_id,
            "title": d["title"][:50] + "...",
            "sections": sec_count,
            "words": word_count,
            "defect": defect_str
        })

    # Write out unified benchmark JSONL file
    with open(BENCHMARK_PATH, "w", encoding="utf-8") as f:
        for d in drafts:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    print(f"{'Doc ID':<18} | {'Sections':<8} | {'Words':<8} | {'Planted Defect'}")
    print("-" * 80)
    for r in summary_rows:
        print(f"{r['doc_id']:<18} | {r['sections']:<8} | {r['words']:<8} | {r['defect']}")
    print("-" * 80)
    print(f"Total Enactments: {len(drafts)}")
    print(f"Total Sections:   {total_sections} (Mean: {total_sections / len(drafts):.1f} per draft)")
    print(f"Total Words:      {total_words:,} (Mean: {total_words / len(drafts):.1f} per draft)")
    print(f"Saved JSON files to: {OUTPUT_DIR}")
    print(f"Saved benchmark to:  {BENCHMARK_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    build_suite()
