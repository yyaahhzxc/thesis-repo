"""
scripts/audit_tier3_via_demo.py
===============================
Audit all 10 Tier 3 landmark Supreme Court cases directly through the active,
fully populated demo backend (Stage 1 MiniLM + Stage 2 DeBERTa Cross-Encoder)
running at http://127.0.0.1:5000/api/audit-document.

Extracts for every single detected conflict:
1. Exact proposed draft Section & Title
2. Target Statute Citation & Title
3. Confidence Percentage & Contradiction Probability
4. Full text of the conflicting ordinance clause & statutory passage
5. Cross-attention XAI token saliency weights
"""
import glob
import html
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path
import pypdf

REPO_ROOT = Path(__file__).resolve().parents[1]
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

XAI_SPAN_RE = re.compile(r'<span[^>]*class="xai-token"[^>]*data-weight="([^"]+)"[^>]*>(.*?)</span>', re.DOTALL)

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

def run_case_audit(case_id, pdf_name):
    pdf_path = PDF_DIR / pdf_name
    print(f"\n================================================================================")
    print(f"[*] Auditing {case_id} ({pdf_name})...")
    reader = pypdf.PdfReader(str(pdf_path))
    raw_text = "\n\n".join(p.extract_text() or "" for p in reader.pages).strip()
    
    payload = json.dumps({
        "document_text": raw_text,
        "filename": pdf_name,
        "doc_id": case_id
    }).encode("utf-8")
    
    t0 = time.perf_counter()
    req = urllib.request.Request(
        "http://127.0.0.1:5000/api/audit-document",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode("utf-8"))
    elapsed = time.perf_counter() - t0
    print(f"[+] Finished {case_id} in {elapsed:.2f}s | Total Sections: {data.get('total_sections')}")
    
    # Extract conflict pairs exactly as UI does
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
                    "ordinance_text": (sec.get("ordinance_text") or sec.get("text") or "").strip(),
                    "statute_text": (c.get("raw_text") or c.get("prepended_text") or sec.get("statute_text") or "").strip(),
                    "top_ordinance_xai": extract_top_xai_tokens(ord_html, top_k=15),
                    "top_statute_xai": extract_top_xai_tokens(stat_html, top_k=15),
                    "legal_rationale": c.get("summary") or sec.get("legal_rationale")
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
                "ordinance_text": (sec.get("ordinance_text") or sec.get("text") or "").strip(),
                "statute_text": (sec.get("statute_text") or "").strip(),
                "top_ordinance_xai": extract_top_xai_tokens(ord_html, top_k=15),
                "top_statute_xai": extract_top_xai_tokens(stat_html, top_k=15),
                "legal_rationale": sec.get("legal_rationale")
            })
            
    distinct_secs = sorted(list(set(p["sec_num"] for p in conflict_pairs)))
    print(f"    --> Total Conflicts Found: {len(conflict_pairs)}")
    print(f"    --> Affected Sections ({len(distinct_secs)}): {distinct_secs}")
    
    return {
        "case_id": case_id,
        "pdf_name": pdf_name,
        "audit_latency_s": round(elapsed, 2),
        "total_sections": data.get("total_sections"),
        "total_conflicts_found": len(conflict_pairs),
        "problematic_sections": distinct_secs,
        "conflict_pairs": conflict_pairs
    }

def main():
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    results = {}
    
    for case_id, pdf_name in CASES:
        try:
            res = run_case_audit(case_id, pdf_name)
            results[case_id] = res
        except Exception as e:
            print(f"[!] Error processing {case_id}: {e}")
            
    # Save full JSON
    OUT_JSON.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[+] Saved full audit output to: {OUT_JSON}")
    
    # Generate human-readable text report
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write("================================================================================\n")
        f.write("TIER 3 SUPREME COURT PREEMPTION AUDIT: FULL SYSTEM-FOUND CONFLICTS & XAI REPORT\n")
        f.write("Platform: Live Demo Neural Engine (MiniLM-L6-v2 + Tuned DeBERTa-v3 Cross-Encoder)\n")
        f.write("================================================================================\n\n")
        
        for case_id, _ in CASES:
            if case_id not in results:
                continue
            r = results[case_id]
            f.write(f"################################################################################\n")
            f.write(f"CASE: {case_id} | Document: {r['pdf_name']}\n")
            f.write(f"Total Sections: {r['total_sections']} | Latency: {r['audit_latency_s']}s\n")
            f.write(f"Total Conflicts Detected: {r['total_conflicts_found']}\n")
            f.write(f"Problematic Sections: {r['problematic_sections']}\n")
            f.write(f"################################################################################\n\n")
            
            for i, p in enumerate(r["conflict_pairs"], 1):
                f.write(f"--- Conflict #{i} --------------------------------------------------------\n")
                f.write(f"Draft Provision : Section {p['sec_num']} ({p['sec_title']})\n")
                f.write(f"Target Statute  : {p['target_statute']}\n")
                f.write(f"Statute Title   : {p['statute_title']}\n")
                f.write(f"Confidence      : {p['confidence_pct']}%\n")
                f.write(f"Draft Text Snippet   : {p['ordinance_text'][:250]}...\n")
                f.write(f"Statute Text Snippet : {p['statute_text'][:250]}...\n")
                f.write(f"Top Draft Saliency   : {[(t['token'], t['weight']) for t in p['top_ordinance_xai'][:8]]}\n")
                f.write(f"Top Statute Saliency : {[(t['token'], t['weight']) for t in p['top_statute_xai'][:8]]}\n")
                if p.get("legal_rationale"):
                    f.write(f"Legal Rationale : {p['legal_rationale']}\n")
                f.write("\n")
            f.write("\n")
            
    print(f"[+] Saved human-readable report to: {OUT_REPORT}")

if __name__ == "__main__":
    main()

