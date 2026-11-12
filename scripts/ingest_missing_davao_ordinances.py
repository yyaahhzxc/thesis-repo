"""
ingest_missing_davao_ordinances.py
==================================
Safely adds missing authentic Davao City Tier 3 Ordinances:
- Ordinance No. 0309-07 (Aerial Spraying Ban, 2007)
- Ordinance No. 092-2000 (Billboard Regulation, 2000)
- Ordinance No. 0158-05 (Revenue Code of 2005)
- Ordinance No. 0325-15 (Mining Closure, 2015)
into:
1. corpus/city_ordinances/categorized_davao_ordinances.jsonl
2. data/unified_dual_statutory_provisions.jsonl
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = REPO_ROOT / "corpus/city_ordinances/categorized_davao_ordinances.jsonl"
UNIFIED_PATH = REPO_ROOT / "data/unified_dual_statutory_provisions.jsonl"
CASES_DIR = REPO_ROOT / "src/demo/sample_cases"

BOILERPLATE_KEYWORDS = ["title", "short title", "effectivity", "repealing", "separability", "scope", "coverage"]

def is_bp(sec_title, sec_text):
    t = (sec_title + " " + sec_text[:80]).lower()
    return any(k in t for k in BOILERPLATE_KEYWORDS)

def run_ingest():
    # 1. Check existing numbers in corpus
    existing_corpus_nums = set()
    if CORPUS_PATH.exists():
        with open(CORPUS_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    d = json.loads(line)
                    existing_corpus_nums.add(d.get("ordinance_number"))

    # 2. Check existing provision_ids in unified
    existing_prov_ids = set()
    if UNIFIED_PATH.exists():
        with open(UNIFIED_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    d = json.loads(line)
                    existing_prov_ids.add(d.get("provision_id"))

    print(f"[*] Initial Corpus records: {len(existing_corpus_nums)}")
    print(f"[*] Initial Unified provisions: {len(existing_prov_ids)}")

    # Ordinances to add
    specs = [
        {
            "json_file": "01_mosqueda_aerial_spraying_ban.json",
            "ord_num": "0309-07",
            "ord_id": "davao_ordinance_no_0309_07",
            "year": 2007,
            "era": "Post-LGC Historical Era (1992–2015)",
            "typology_id": 1,
            "typology": "Substantive Regulatory, Health & Penal Ordinances",
            "domain_id": 4,
            "domain": "Agriculture & Agrarian Reform"
        },
        {
            "json_file": "02_evasco_billboard_regulation.json",
            "ord_num": "092-2000",
            "ord_id": "davao_ordinance_no_092_2000",
            "year": 2000,
            "era": "Post-LGC Historical Era (1992–2015)",
            "typology_id": 1,
            "typology": "Substantive Regulatory, Health & Penal Ordinances",
            "domain_id": 5,
            "domain": "Local Taxation, Revenue & Fiscal Administration"
        },
        {
            "json_file": "03_arc_investors_holding_tax.json",
            "ord_num": "0158-05",
            "ord_id": "davao_ordinance_no_0158_05",
            "year": 2005,
            "era": "Post-LGC Historical Era (1992–2015)",
            "typology_id": 1,
            "typology": "Substantive Regulatory, Health & Penal Ordinances",
            "domain_id": 5,
            "domain": "Local Taxation, Revenue & Fiscal Administration"
        },
        {
            "json_file": "06_mining_ban_watershed.json",
            "ord_num": "0325-15",
            "ord_id": "davao_ordinance_no_0325_15",
            "year": 2015,
            "era": "Post-LGC Historical Era (1992–2015)",
            "typology_id": 1,
            "typology": "Substantive Regulatory, Health & Penal Ordinances",
            "domain_id": 3,
            "domain": "Environmental Protection, Forestry & Sanitation"
        }
    ]

    new_corpus_records = []
    new_provisions = []

    for spec in specs:
        ord_num = spec["ord_num"]
        json_path = CASES_DIR / spec["json_file"]
        if not json_path.exists():
            print(f"[!] Warning: {json_path} does not exist, skipping.")
            continue
        
        data = json.loads(json_path.read_text(encoding="utf-8"))
        sections = data.get("sections", [])
        title = data.get("title", "")
        
        full_text_chunks = [title]
        processed_sections = []
        op_count = 0
        bp_count = 0

        for sec in sections:
            s_num = sec.get("number")
            s_head = sec.get("heading", "")
            s_text = sec.get("text", "")
            marker = f"SECTION {s_num}"
            full_clause = f"{marker}. {s_head}. {s_text}".strip()
            full_text_chunks.append(full_clause)
            
            bp = is_bp(s_head, s_text)
            if bp:
                bp_count += 1
            else:
                op_count += 1

            words = len(s_text.split())
            est_tokens = int(words * 1.33)
            
            processed_sections.append({
                "section_index": s_num,
                "section_marker": marker,
                "section_title": s_head,
                "raw_text": s_text,
                "is_boilerplate": bp,
                "word_count": words,
                "est_tokens": est_tokens,
                "fits_512": (est_tokens <= 512)
            })

            # Provision for unified dataset
            clean_ord_id = spec["ord_id"].replace("davao_ordinance_no_", "ord_")
            prov_id = f"loc_{clean_ord_id}_sec_{s_num}"
            if prov_id not in existing_prov_ids:
                prov_record = {
                    "provision_id": prov_id,
                    "jurisdiction": "local",
                    "enactment_id": spec["ord_id"],
                    "enactment_number": f"Ordinance No. {ord_num}",
                    "enactment_title": title,
                    "year": spec["year"],
                    "era": spec["era"],
                    "section_number": str(s_num),
                    "section_title": s_head,
                    "raw_text": s_text,
                    "prepended_text": f"[Ordinance No. {ord_num} | Section {s_num}: {s_head}] {s_text}",
                    "word_count": words,
                    "est_tokens": est_tokens,
                    "fits_512": (est_tokens <= 512),
                    "is_boilerplate": bp,
                    "is_operative": not bp,
                    "macro_domain_id": spec["domain_id"],
                    "macro_domain": spec["domain"]
                }
                new_provisions.append(prov_record)
                existing_prov_ids.add(prov_id)

        full_text = "\n\n".join(full_text_chunks)
        total_words = len(full_text.split())
        total_chars = len(full_text)

        if ord_num not in existing_corpus_nums:
            corpus_record = {
                "ordinance_id": spec["ord_id"],
                "ordinance_number": ord_num,
                "filename": f"{spec['year']}/Ordinance No. {ord_num}.txt",
                "year": spec["year"],
                "era": spec["era"],
                "title": title,
                "functional_typology_id": spec["typology_id"],
                "functional_typology": spec["typology"],
                "word_count": total_words,
                "char_count": total_chars,
                "vlm_raw_word_count": total_words,
                "vlm_raw_char_count": total_chars,
                "chars_pruned": 0,
                "words_pruned": 0,
                "total_sections": len(sections),
                "operative_sections": op_count,
                "boilerplate_sections": bp_count,
                "sections": processed_sections,
                "full_text": full_text
            }
            new_corpus_records.append(corpus_record)
            existing_corpus_nums.add(ord_num)
            print(f"[+] Prepared Corpus Record: Ordinance No. {ord_num} ({len(sections)} sections, {total_words} words)")

    # Append to corpus
    if new_corpus_records:
        with open(CORPUS_PATH, "a", encoding="utf-8") as f:
            for rec in new_corpus_records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"[SUCCESS] Appended {len(new_corpus_records)} records to {CORPUS_PATH.name}")

    # Append to unified provisions
    if new_provisions:
        with open(UNIFIED_PATH, "a", encoding="utf-8") as f:
            for prov in new_provisions:
                f.write(json.dumps(prov, ensure_ascii=False) + "\n")
        print(f"[SUCCESS] Appended {len(new_provisions)} provisions to {UNIFIED_PATH.name}")

if __name__ == "__main__":
    run_ingest()

