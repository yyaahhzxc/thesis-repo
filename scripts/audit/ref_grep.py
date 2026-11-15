#!/usr/bin/env python3
"""Search a locally stored reference PDF (docs/references/<key>.pdf) for phrases or numbers.

Used during manuscript sweeps to verify that a claim, formula, or numeric
threshold attributed to \\cite{key} literally appears in the cited source
(paper-rigor-and-citations.md: zero phantom attribution).

    python scripts/audit/ref_grep.py KEY "term one" "0.61" [--context 160] [--max 6]
    python scripts/audit/ref_grep.py KEY --pages          # page count / text-extractable?

Exit code 0 = at least one term found; 1 = none found; 2 = PDF missing/unreadable.
Matching is case-insensitive on whitespace-normalised text (hyphenation at line ends is repaired).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REFS = ROOT / "docs" / "references"
CACHE = ROOT / "output" / "ref_text_cache"


def page_texts(pdf: Path) -> list[str]:
    cache = CACHE / (pdf.stem + ".txt")
    if cache.exists() and cache.stat().st_mtime >= pdf.stat().st_mtime:
        return cache.read_text(encoding="utf-8", errors="replace").split("\f")
    import fitz  # PyMuPDF
    doc = fitz.open(pdf)
    pages = [p.get_text() for p in doc]
    CACHE.mkdir(parents=True, exist_ok=True)
    cache.write_text("\f".join(pages), encoding="utf-8")
    return pages


def norm(t: str) -> str:
    t = re.sub(r"-\s*\n\s*", "", t)
    return re.sub(r"\s+", " ", t).lower()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("key")
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--context", type=int, default=140)
    ap.add_argument("--max", type=int, default=5, help="max hits printed per term")
    ap.add_argument("--pages", action="store_true")
    args = ap.parse_args()
    pdf = next((p for p in REFS.glob("*.pdf") if p.stem.lower() == args.key.lower()), None)
    if pdf is None:
        print(f"NO LOCAL PDF for key '{args.key}' in docs/references/ (cannot verify; flag for human review)")
        return 2
    try:
        pages = page_texts(pdf)
    except Exception as exc:
        print(f"cannot read {pdf.name}: {exc}")
        return 2
    chars = sum(len(p.strip()) for p in pages)
    if args.pages or not args.terms:
        print(f"{pdf.name}: {len(pages)} pages, {chars} extractable characters"
              + ("  (SCANNED / no text layer: verify manually)" if chars < 500 else ""))
        return 0 if chars >= 500 else 2
    if chars < 500:
        print(f"{pdf.name}: no extractable text (scanned). Verify manually; do not assume support.")
        return 2
    found_any = False
    normed = [norm(p) for p in pages]
    for term in args.terms:
        needle = norm(term)
        shown = 0
        for i, pt in enumerate(normed, 1):
            for m in re.finditer(re.escape(needle), pt):
                if shown == 0:
                    print(f"== '{term}'")
                s, e = max(0, m.start() - args.context), min(len(pt), m.end() + args.context)
                print(f"  p.{i}: ...{pt[s:e]}...")
                shown += 1
                found_any = True
                if shown >= args.max:
                    break
            if shown >= args.max:
                break
        if shown == 0:
            print(f"== '{term}': NOT FOUND in {pdf.name}")
    return 0 if found_any else 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
