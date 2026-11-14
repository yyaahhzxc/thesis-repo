"""
scripts/run_tier3_clean_sync.py
=================================
Executes 100% genuine, full-PDF in-process audits across all Tier 3 PDFs in
src/demo/sample_cases/pdf/ using execute_full_ordinance_audit() from src/demo/app.py
(no HTTP timeouts, no TIER3_TXT_MAP snippet overrides).

Writes synchronized outputs matching exact Demo UI pair-counting logic to:
  - output/tier3_live_demo_full_audit_all10.json
  - output/tier3_live_demo_audit_report.txt

Usage:
  .\venv\Scripts\python.exe scripts/run_tier3_clean_sync.py --suite standard8
  .\venv\Scripts\python.exe scripts/run_tier3_clean_sync.py --suite revcode
  .\venv\Scripts\python.exe scripts/run_tier3_clean_sync.py --suite all
"""
import argparse
import hashlib
import html
import json
import re
import sys
import time
from pathlib import Path

import pypdf

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src" / "demo"))
import app as demo_app  # noqa: E402

PDF_DIR = REPO_ROOT / "src" / "demo" / "sample_cases" / "pdf"
OUT_JSON = REPO_ROOT / "output" / "tier3_live_demo_full_audit_all10.json"
OUT_REPORT = REPO_ROOT / "output" / "tier3_live_demo_audit_report.txt"

CASES = [
    ("DAVAO-TIER3-01", "01_mosqueda_aerial_spraying_ban.pdf"),
    ("DAVAO-TIER3-02", "02_evasco_billboard_regulation.pdf"),
    ("DAVAO-TIER3-03", "03_arc_investors_holding_tax.pdf"),
    ("DAVAO-TIER3-04", "04_first_meridian_payment_under_protest.pdf"),
    ("DAVAO-TIER3-05", "05_davao_gsis_property_tax.pdf"),
    ("DAVAO-TIER3-06", "06_mining_ban_watershed.pdf"),
    ("DAVAO-TIER3-07", "07_davao_anti_smoking_stricter_standard.pdf"),
    ("DAVAO-TIER3-08", "08_davao_speed_limits_traffic_code.pdf"),
    ("SC-PHIL-09", "09_magtajas_casino_preemption.pdf"),
    ("SC-PHIL-10", "10_city_of_manila_laguio_due_process.pdf"),
]

XAI_SPAN_RE = re.compile(
    r'<span[^>]*class="xai-token"[^>]*data-weight="([^"]+)"[^>]*>(.*?)</span>',
    re.DOTALL,
)


def extract_top_xai_tokens(xai_html: str, top_k: int = 15):
    if not xai_html:
        return []
    tokens = []
    for weight_str, raw_tok in XAI_SPAN_RE.findall(xai_html):
        tok = html.unescape(raw_tok).strip()
        if not tok:
            continue
        try:
            w = float(weight_str)
        except ValueError:
            continue
        tokens.append((tok, round(w, 4)))
    tokens.sort(key=lambda x: x[1], reverse=True)
    seen = set()
    unique_top = []
    for tok, w in tokens:
        k = tok.lower()
        if k not in seen:
            seen.add(k)
            unique_top.append({"token": tok, "weight": w})
        if len(unique_top) >= top_k:
            break
    return unique_top


def extract_conflict_pairs(data: dict):
    conflict_pairs = []
    for sec in data.get("sections", []):
        if sec.get("is_boilerplate"):
            continue
        cands = sec.get("candidate_shortlist") or []
        sec_conflicts = []
        for c in cands:
            if not c.get("stage2_evaluated"):
                continue
            tau_c = c.get("dynamic_threshold", 0.45)
            tau_pct = c.get("dynamic_threshold_pct", 45.0)
            is_c = bool(
                c.get("is_conflict")
                or (c.get("p_contradiction") is not None and c["p_contradiction"] >= tau_c)
                or (c.get("stage2_confidence") is not None and float(c["stage2_confidence"]) >= tau_pct)
            )
            if is_c:
                sec_conflicts.append(c)

        if sec_conflicts:
            sec_conflicts.sort(key=lambda x: x.get("stage2_confidence") or 0, reverse=True)
            for c in sec_conflicts:
                ord_html = c.get("ordinance_html") or sec.get("ordinance_html") or ""
                stat_html = c.get("statute_html") or sec.get("statute_html") or ""
                conflict_pairs.append({
                    "sec_num": sec.get("sec_num"),
                    "sec_title": sec.get("sec_title"),
                    "target_statute": c.get("citation") or sec.get("target_statute"),
                    "statute_title": c.get("title") or sec.get("statute_title") or "",
                    "confidence_pct": c.get("stage2_confidence") if c.get("stage2_confidence") is not None else round((c.get("p_contradiction") or 0.95) * 100, 2),
                    "p_contradiction": c.get("p_contradiction"),
                    "dynamic_threshold_pct": c.get("dynamic_threshold_pct", 45.0),
                    "graph_distance_d_g": c.get("graph_distance_d_g", sec.get("graph_distance_d_g", 999)),
                    "relation_type": c.get("relation_type", sec.get("relation_type", "")),
                    "ordinance_text": (sec.get("ordinance_text") or sec.get("text") or "").strip(),
                    "statute_text": (c.get("raw_text") or c.get("prepended_text") or sec.get("statute_text") or "").strip(),
                    "top_ordinance_xai": extract_top_xai_tokens(ord_html, top_k=15),
                    "top_statute_xai": extract_top_xai_tokens(stat_html, top_k=15),
                    "legal_rationale": c.get("summary") or sec.get("legal_rationale"),
                })
        elif sec.get("verdict") == "CONTRADICTION":
            ord_html = sec.get("ordinance_html") or ""
            stat_html = sec.get("statute_html") or ""
            conflict_pairs.append({
                "sec_num": sec.get("sec_num"),
                "sec_title": sec.get("sec_title"),
                "target_statute": sec.get("target_statute"),
                "statute_title": sec.get("statute_title") or "",
                "confidence_pct": sec.get("confidence_percentage", 95.0),
                "p_contradiction": sec.get("conflict_probability"),
                "dynamic_threshold_pct": sec.get("dynamic_threshold_pct", 45.0),
                "graph_distance_d_g": sec.get("graph_distance_d_g", 999),
                "relation_type": sec.get("relation_type", ""),
                "ordinance_text": (sec.get("ordinance_text") or sec.get("text") or "").strip(),
                "statute_text": (sec.get("statute_text") or "").strip(),
                "top_ordinance_xai": extract_top_xai_tokens(ord_html, top_k=15),
                "top_statute_xai": extract_top_xai_tokens(stat_html, top_k=15),
                "legal_rationale": sec.get("legal_rationale"),
            })
    return conflict_pairs


def run_case(case_id: str, pdf_name: str):
    pdf_path = PDF_DIR / pdf_name
    pdf_sha = hashlib.sha256(pdf_path.read_bytes()).hexdigest()[:16]
    reader = pypdf.PdfReader(str(pdf_path))
    raw_text = "\n\n".join(p.extract_text() or "" for p in reader.pages).strip()
    if not raw_text:
        raise RuntimeError(f"PDF {pdf_name} yielded empty text!")

    print(f"\n{'='*80}\n[*] Auditing {case_id} ({pdf_name} | pages={len(reader.pages)} | chars={len(raw_text)} | sha={pdf_sha})...", flush=True)
    last_print = [0.0]

    def cb(stage, progress, badge, msg):
        now = time.perf_counter()
        if now - last_print[0] >= 15.0 or progress in (20, 100):
            print(f"    [{progress:3d}%] {stage}: {badge} - {msg}", flush=True)
            last_print[0] = now

    t0 = time.perf_counter()
    data = demo_app.execute_full_ordinance_audit(raw_text, pdf_name, doc_id=None, progress_callback=cb)
    elapsed = time.perf_counter() - t0
    conflict_pairs = extract_conflict_pairs(data)
    distinct_secs = sorted(list(set(p["sec_num"] for p in conflict_pairs)))
    substantive = sum(1 for s in data.get("sections", []) if not s.get("is_boilerplate"))

    print(f"[+] Finished {case_id} in {elapsed:.2f}s | Sections: {data.get('total_sections')} ({substantive} substantive)", flush=True)
    print(f"    --> UI Headline: {len(conflict_pairs)} Conflicts Detected! ({len(distinct_secs)} Problematic Sections: {distinct_secs})", flush=True)

    return {
        "case_id": case_id,
        "pdf_name": pdf_name,
        "pdf_pages": len(reader.pages),
        "pdf_sha256_prefix": pdf_sha,
        "audit_latency_s": round(elapsed, 2),
        "latency_metrics": data.get("latency_metrics", {}),
        "total_sections": data.get("total_sections", 0),
        "substantive_sections": substantive,
        "total_conflicts_found": len(conflict_pairs),
        "problematic_sections": distinct_secs,
        "conflict_pairs": conflict_pairs,
    }


def write_report(results: dict):
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write("================================================================================\n")
        f.write("OFFICIAL TIER 3 SUPREME COURT PREEMPTION AUDIT: FULL-PDF SYNCHRONIZED LOG\n")
        f.write("Platform: Prototype Demo Backend Engine (MiniLM-L6-v2 + Tuned DeBERTa-v3 Cross-Encoder)\n")
        f.write("Mode: Direct Full-PDF Execution (Zero Snippet Fallbacks, Zero HTTP Timeouts)\n")
        f.write("================================================================================\n\n")

        for cid, _ in CASES:
            if cid not in results:
                continue
            r = results[cid]
            f.write("#" * 80 + "\n")
            f.write(f"CASE: {cid} | Document: {r['pdf_name']} | Pages: {r.get('pdf_pages', '?')}\n")
            f.write(f"Total Sections: {r['total_sections']} ({r.get('substantive_sections', '?')} substantive) | Latency: {r['audit_latency_s']}s\n")
            f.write(f"UI Headline: {r['total_conflicts_found']} Conflicts Detected!\n")
            f.write(f"UI Subheadline: {len(r['problematic_sections'])} Problematic Sections: {r['problematic_sections']}\n")
            f.write("#" * 80 + "\n\n")

            if not r["conflict_pairs"]:
                f.write("   [VERDICT] All substantive provisions passed calibrated threshold tau* (0 Conflicts Detected).\n\n")
            else:
                for idx, p in enumerate(r["conflict_pairs"], 1):
                    f.write(f"--- Conflict #{idx} --------------------------------------------------------\n")
                    f.write(f"Draft Provision : Section {p['sec_num']} ({p['sec_title']})\n")
                    f.write(f"Target Statute  : {p['target_statute']}\n")
                    f.write(f"Statute Title   : {p['statute_title']}\n")
                    f.write(f"Confidence      : {p['confidence_pct']}%\n")
                    f.write(f"Decision Cutoff : tau* = {p['dynamic_threshold_pct']}% (d_G = {p.get('graph_distance_d_g', '?')})\n")
                    f.write(f"Draft Text Snippet   : {p['ordinance_text'][:220].replace(chr(10), ' ')}...\n")
                    f.write(f"Statute Text Snippet : {p['statute_text'][:220].replace(chr(10), ' ')}...\n")
                    f.write(f"Top Draft Saliency   : {[(t['token'], t['weight']) for t in p['top_ordinance_xai'][:8]]}\n")
                    f.write(f"Top Statute Saliency : {[(t['token'], t['weight']) for t in p['top_statute_xai'][:8]]}\n")
                    f.write(f"Legal Rationale : {p['legal_rationale']}\n\n")
            f.write("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=["standard8", "revcode", "all", "manila"], default="standard8")
    args = parser.parse_args()

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    results = {}
    if OUT_JSON.exists():
        try:
            results = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        except Exception:
            results = {}

    if args.suite == "manila":
        target_cases = [c for c in CASES if c[0] == "SC-PHIL-10"]
    elif args.suite == "standard8":
        target_cases = [c for c in CASES if c[0] not in ("DAVAO-TIER3-03", "DAVAO-TIER3-04")]
    elif args.suite == "revcode":
        target_cases = [c for c in CASES if c[0] in ("DAVAO-TIER3-03", "DAVAO-TIER3-04")]
    else:
        target_cases = CASES

    sha_cache = {}
    for cid, pdf_name in target_cases:
        pdf_sha = hashlib.sha256((PDF_DIR / pdf_name).read_bytes()).hexdigest()[:16]
        if pdf_sha in sha_cache:
            base = dict(sha_cache[pdf_sha])
            base["case_id"] = cid
            base["pdf_name"] = pdf_name
            results[cid] = base
            print(f"[*] {cid} shares identical PDF SHA ({pdf_sha}); mirrored clean result from {sha_cache[pdf_sha]['case_id']}.", flush=True)
        else:
            res = run_case(cid, pdf_name)
            results[cid] = res
            sha_cache[pdf_sha] = res
        OUT_JSON.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        write_report(results)

    print(f"\n[OK] Synchronized audit saved to {OUT_JSON} and {OUT_REPORT}")


if __name__ == "__main__":
    main()
