"""Synchronizes all 10 cases in ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl
with 100% verbatim PDF ordinance sections and 100% verbatim positive-law statute text
from data/unified_dual_statutory_provisions.jsonl.
"""

import ast
import json
import os
import re
from pathlib import Path

import pypdf

REPO_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = REPO_ROOT / "src" / "demo" / "app.py"
UNIFIED_PATH = REPO_ROOT / "data" / "unified_dual_statutory_provisions.jsonl"
TIER3_JSONL_PATH = REPO_ROOT / "ground_truth" / "tier3_sc_cases" / "tier3_jurisprudential_cases.jsonl"
TIER3_PDF_DIR = REPO_ROOT / "src" / "demo" / "sample_cases" / "pdf"

CONST_ART3_SEC1_VERBATIM = (
    "Section 1. No person shall be deprived of life, liberty, or property without due process "
    "of law, nor shall any person be denied the equal protection of the laws."
)

CASE_ALIGNMENT_SPEC = {
    "DAVAO-TIER3-01": {
        "pdf_name": "01_mosqueda_aerial_spraying_ban.pdf",
        "sec_num": 5,
        "target_pids": ["nat_pd_1144_1977_sec_6"],
        "extra_premises": [],
    },
    "DAVAO-TIER3-02": {
        "pdf_name": "02_evasco_billboard_regulation.pdf",
        "sec_num": 7,
        "target_pids": ["nat_ra_7160_1991_sec_458"],
        "extra_premises": [],
    },
    "DAVAO-TIER3-03": {
        "pdf_name": "03_arc_investors_holding_tax.pdf",
        "sec_num": 69,
        "target_pids": ["nat_ra_7160_1991_sec_143"],
        "extra_premises": [],
    },
    "DAVAO-TIER3-04": {
        "pdf_name": "04_first_meridian_payment_under_protest.pdf",
        "sec_num": 423,
        "target_pids": ["nat_ra_7160_1991_sec_195"],
        "extra_premises": [],
    },
    "DAVAO-TIER3-05": {
        "pdf_name": "05_davao_gsis_property_tax.pdf",
        "sec_num": 8,
        "target_pids": ["nat_ra_7160_1991_sec_193", "nat_ra_7160_1991_sec_234"],
        "extra_premises": [],
    },
    "DAVAO-TIER3-06": {
        "pdf_name": "06_mining_ban_watershed.pdf",
        "sec_num": 5,
        "target_pids": ["nat_ra_7942_1995_sec_4", "nat_ra_7942_1995_sec_27"],
        "extra_premises": [],
    },
    "DAVAO-TIER3-07": {
        "pdf_name": "07_davao_anti_smoking_stricter_standard.pdf",
        "sec_num": 4,
        "target_pids": ["nat_ra_7160_1991_sec_16", "nat_ra_9211_2003_sec_5"],
        "extra_premises": [],
    },
    "DAVAO-TIER3-08": {
        "pdf_name": "08_davao_speed_limits_traffic_code.pdf",
        "sec_num": 7,
        "target_pids": ["nat_ra_4136_1964_sec_35", "nat_ra_4136_1964_sec_38"],
        "extra_premises": [],
    },
    "SC-PHIL-09": {
        "pdf_name": "09_magtajas_casino_preemption.pdf",
        "sec_num": 1,
        "target_pids": ["nat_pd_1869_1983_sec_1", "nat_pd_1869_1983_sec_10", "nat_ra_7160_1991_sec_5"],
        "extra_premises": [],
    },
    "SC-PHIL-10": {
        "pdf_name": "10_city_of_manila_laguio_due_process.pdf",
        "sec_num": 1,
        "target_pids": ["nat_ra_7160_1991_sec_458"],
        "extra_premises": [
            {
                "citation": "1987 Constitution, Article III, Section 1",
                "raw_text": CONST_ART3_SEC1_VERBATIM,
            }
        ],
    },
}


def load_chunker_from_app():
    src = APP_PATH.read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {"re": re}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ("is_boilerplate_section", "chunk_ordinance_sections"):
            exec(compile(ast.Module(body=[node], type_ignores=[]), "<ast>", "exec"), ns)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in ("BOILERPLATE_TITLES", "BOILERPLATE_KEYWORDS", "SECTION_HEADER_RE"):
                    exec(compile(ast.Module(body=[node], type_ignores=[]), "<ast>", "exec"), ns)
    return ns["chunk_ordinance_sections"]


def main():
    chunk_ordinance_sections = load_chunker_from_app()
    needed_pids = {pid for spec in CASE_ALIGNMENT_SPEC.values() for pid in spec["target_pids"]}
    corpus_recs = {}
    with open(UNIFIED_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            pid = obj.get("provision_id")
            if pid in needed_pids:
                corpus_recs[pid] = obj

    missing = needed_pids - set(corpus_recs.keys())
    if missing:
        raise RuntimeError(f"Missing target provision IDs in {UNIFIED_PATH}: {sorted(missing)}")

    # Extract exact PDF sections (cache shared RevCode PDF)
    pdf_cache = {}
    cases = [json.loads(ln) for ln in TIER3_JSONL_PATH.read_text(encoding="utf-8").splitlines() if ln.strip()]
    updated = []

    print("=" * 96)
    print("TIER 3 VERBATIM ALIGNMENT VERIFICATION (PDF SECTION + CORPUS STATUTE)")
    print("=" * 96)

    for c in cases:
        cid = c["case_id"]
        spec = CASE_ALIGNMENT_SPEC[cid]
        pdf_path = TIER3_PDF_DIR / spec["pdf_name"]
        if not pdf_path.exists():
            raise FileNotFoundError(f"Missing Tier 3 PDF: {pdf_path}")

        if spec["pdf_name"] not in pdf_cache:
            raw_pdf = "\n\n".join(pg.extract_text() or "" for pg in pypdf.PdfReader(str(pdf_path)).pages).strip()
            _, chunks = chunk_ordinance_sections(raw_pdf, default_title=spec["pdf_name"])
            pdf_cache[spec["pdf_name"]] = {ch["sec_num"]: ch for ch in chunks}

        chunk_map = pdf_cache[spec["pdf_name"]]
        if spec["sec_num"] not in chunk_map:
            raise KeyError(f"Section {spec['sec_num']} not found in {spec['pdf_name']}")
        ch = chunk_map[spec["sec_num"]]
        pdf_sec_text = ch["text"].strip()

        if spec["extra_premises"]:
            primary_source = spec["extra_premises"][0]["citation"]
            primary_premise = spec["extra_premises"][0]["raw_text"].strip()
        else:
            primary_pid = spec["target_pids"][0]
            rec = corpus_recs[primary_pid]
            primary_source = primary_pid
            primary_premise = (rec.get("raw_text") or "").lstrip("- \r\n").strip()

        c["challenged_pdf_name"] = spec["pdf_name"]
        c["challenged_sec_num"] = spec["sec_num"]
        c["challenged_sec_title"] = ch.get("sec_title") or ""
        c["challenged_text"] = pdf_sec_text
        c["target_provision_ids"] = list(spec["target_pids"])
        c["extra_premises"] = spec["extra_premises"]
        c["premise_source"] = primary_source
        c["premise_text"] = primary_premise
        updated.append(c)

        print(
            f"{cid:15s} | PDF={spec['pdf_name']} Sec.{spec['sec_num']:<3d} ({len(pdf_sec_text):4d} chars) "
            f"| Premise={primary_source} ({len(primary_premise):5d} chars) | targets={spec['target_pids']}"
        )

    tmp_path = TIER3_JSONL_PATH.with_suffix(".jsonl.tmp")
    with open(tmp_path, "w", encoding="utf-8") as fout:
        for c in updated:
            fout.write(json.dumps(c, ensure_ascii=False) + "\n")
    os.replace(tmp_path, TIER3_JSONL_PATH)
    print(f"\n[OK] Synchronized all {len(updated)} cases verbatim in {TIER3_JSONL_PATH}")


if __name__ == "__main__":
    main()
