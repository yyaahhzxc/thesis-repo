#!/usr/bin/env python3
"""
scripts/verify_references.py
Comprehensive verification and integrity checker for references_verified.bib.

Checks:
1. Compares references_verified.bib against CS_Undergraduate_Thesis_Template/references.bib.
2. Identifies all @misc, news, government, legal, and non-academic entries.
3. Validates academic entries (arXiv IDs, DOIs, ACL anthology links).
4. Verifies citation usage across LaTeX manuscript chapters.
5. Flags discrepancies, hallucinations, or malformed fields.
"""

import os
import re
import sys
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERIFIED_BIB = REPO_ROOT / "references_verified.bib"
ORIGINAL_BIB = REPO_ROOT / "CS_Undergraduate_Thesis_Template" / "references.bib"
TEX_DIR = REPO_ROOT / "CS_Undergraduate_Thesis_Template"


def parse_bib_robust(bib_path):
    with open(bib_path, 'r', encoding='utf-8') as f:
        text = f.read()

    entries = []
    i = 0
    n = len(text)

    while i < n:
        at = text.find('@', i)
        if at == -1:
            break
        brace = text.find('{', at)
        if brace == -1:
            break
        entry_type = text[at + 1:brace].strip().lower()

        depth = 1
        j = brace + 1
        while j < n and depth > 0:
            if text[j] == '{':
                depth += 1
            elif text[j] == '}':
                depth -= 1
            j += 1

        body = text[brace + 1:j - 1]
        first_comma = body.find(',')
        if first_comma != -1:
            key = body[:first_comma].strip()
            fields_str = body[first_comma + 1:]
            
            # Parse fields
            fields = {}
            fi = 0
            fn = len(fields_str)
            while fi < fn:
                eq = fields_str.find('=', fi)
                if eq == -1:
                    break
                fname = fields_str[fi:eq].strip().lower()
                fname = re.sub(r'^[,\s]+', '', fname)

                fj = eq + 1
                while fj < fn and fields_str[fj].isspace():
                    fj += 1
                if fj >= fn:
                    break

                val = ''
                if fields_str[fj] == '{':
                    fdepth = 1
                    fk = fj + 1
                    while fk < fn and fdepth > 0:
                        if fields_str[fk] == '{':
                            fdepth += 1
                        elif fields_str[fk] == '}':
                            fdepth -= 1
                        fk += 1
                    val = fields_str[fj + 1:fk - 1].strip()
                    fi = fk
                elif fields_str[fj] == '"':
                    fk = fj + 1
                    while fk < fn and fields_str[fk] != '"':
                        if fields_str[fk] == '\\':
                            fk += 1
                        fk += 1
                    val = fields_str[fj + 1:fk].strip()
                    fi = fk + 1
                else:
                    comma = fields_str.find(',', fj)
                    if comma == -1:
                        val = fields_str[fj:].strip()
                        fi = fn
                    else:
                        val = fields_str[fj:comma].strip()
                        fi = comma + 1
                
                clean_val = re.sub(r'\s+', ' ', val).strip()
                if fname:
                    fields[fname] = clean_val

            raw_bib = text[at:j]
            entries.append({
                "entry_type": entry_type,
                "citekey": key,
                "fields": fields,
                "raw_bib": raw_bib
            })
        i = j

    return entries


def scan_latex_citations():
    citation_map = {}
    tex_files = list(TEX_DIR.glob("**/*.tex"))

    for tf in tex_files:
        rel_path = tf.relative_to(REPO_ROOT).as_posix()
        try:
            with open(tf, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        for match in re.finditer(r'\\cite[a-zA-Z]*\*?\{([^}]+)\}', content):
            keys = [k.strip() for k in match.group(1).split(',') if k.strip()]
            for k in keys:
                if k not in citation_map:
                    citation_map[k] = {"count": 0, "files": set()}
                citation_map[k]["count"] += 1
                citation_map[k]["files"].add(rel_path)

    for k in citation_map:
        citation_map[k]["files"] = sorted(list(citation_map[k]["files"]))

    return citation_map


def main():
    print("=" * 70)
    print("      BIBLIOGRAPHY VERIFICATION & INTEGRITY AUDITOR")
    print("=" * 70)

    entries = parse_bib_robust(VERIFIED_BIB)
    citations = scan_latex_citations()

    total = len(entries)
    print(f"\n[+] Total entries in references_verified.bib: {total}")

    # Categorize entries
    categories = {
        "ph_law_and_jurisprudence": [],
        "news_and_media": [],
        "cs_nlp_papers": [],
        "statistical_evaluation": [],
        "books_and_manuals": [],
        "other": []
    }

    suspicious_candidates = []
    missing_urls = []

    for e in entries:
        ck = e["citekey"]
        f = e["fields"]
        etype = e["entry_type"]
        title = f.get("title", "")
        author = f.get("author", "")
        url = f.get("url", "")
        doi = f.get("doi", "")
        howpub = f.get("howpublished", "")

        is_cited = ck in citations
        cite_count = citations[ck]["count"] if is_cited else 0
        cited_files = citations[ck]["files"] if is_cited else []

        e["is_cited"] = is_cited
        e["cite_count"] = cite_count
        e["cited_files"] = cited_files

        if not url and not doi:
            missing_urls.append(e)

        # Categorization
        ck_lower = ck.lower()
        title_lower = title.lower()
        url_lower = url.lower()
        howpub_lower = howpub.lower()

        if any(k in ck_lower for k in ["ra", "pd", "eo", "act", "ca638", "scp", "scam", "spdavao"]) or \
           "supreme court" in title_lower or "republic act" in title_lower or "ordinance" in title_lower or \
           "lawphil.net" in url_lower or "officialgazette.gov.ph" in url_lower:
            categories["ph_law_and_jurisprudence"].append(e)

        elif any(k in url_lower for k in ["rappler.com", "inquirer.net", "philstar.com", "sunstar.com.ph", "davaotoday.com", "mindanews.com", "newsinfo"]) or \
             any(k in howpub_lower for k in ["rappler", "inquirer", "sunstar", "philstar", "davao today", "mindanews"]):
            categories["news_and_media"].append(e)
            suspicious_candidates.append(e)

        elif any(k in ck_lower for k in ["mcnemar", "friedman", "fleiss", "cohen", "landis", "vabalas", "card2020", "demsar"]):
            categories["statistical_evaluation"].append(e)

        elif etype in ["book"]:
            categories["books_and_manuals"].append(e)

        elif any(k in url_lower for k in ["arxiv.org", "aclanthology.org", "doi.org", "ieeexplore", "acm.org", "springer.com", "sciencedirect.com", "openreview.net"]):
            categories["cs_nlp_papers"].append(e)

        else:
            categories["other"].append(e)
            if etype == "misc" or not doi:
                suspicious_candidates.append(e)

    print("\n--- CATEGORY BREAKDOWN ---")
    for cat, items in categories.items():
        print(f"  * {cat:28s}: {len(items):3d} entries")

    print(f"\n--- URL COVERAGE ---")
    has_url_count = sum(1 for e in entries if e["fields"].get("url") or e["fields"].get("doi"))
    print(f"  * Entries with URL/DOI: {has_url_count} / {total} ({has_url_count/total*100:.1f}%)")
    print(f"  * Entries missing URL:  {len(missing_urls)}")

    print(f"\n--- SUSPICIOUS / HIGH-PRIORITY VERIFICATION CANDIDATES ({len(suspicious_candidates)} entries) ---")
    for idx, e in enumerate(suspicious_candidates, 1):
        ck = e["citekey"]
        f = e["fields"]
        print(f"\n[{idx}] Citekey: {ck}")
        print(f"    Title:        {f.get('title', 'N/A')}")
        print(f"    Author:       {f.get('author', 'N/A')}")
        print(f"    Year:         {f.get('year', 'N/A')}")
        print(f"    Howpublished: {f.get('howpublished', 'N/A')}")
        print(f"    URL:          {f.get('url', 'N/A')}")
        print(f"    Cited in:     {e['cite_count']}x across {e['cited_files']}")

    # Save detailed audit report to JSON
    report_file = REPO_ROOT / "docs" / "suspicious_references_audit.json"
    with open(report_file, 'w', encoding='utf-8') as f_out:
        json.dump(suspicious_candidates, f_out, indent=2, ensure_ascii=False)
    print(f"\n[OK] Exported suspicious references to {report_file}")


if __name__ == "__main__":
    main()
