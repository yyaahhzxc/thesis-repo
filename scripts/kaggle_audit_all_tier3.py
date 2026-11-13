"""
kaggle_audit_all_tier3.py
=========================
Full GPU-accelerated demo-site audit across all 10 Tier 3 Supreme Court PDFs
using the true fine-tuned Stage 2 Cross-Encoder (`models/nli-deberta-v3-finetuned`)
with XAI cross-attention token saliency preserved.

Usage on Kaggle:
    python scripts/kaggle_audit_all_tier3.py
"""
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src" / "demo"))
os.chdir(str(REPO_ROOT))

# 1. Ensure fine-tuned Stage 2 checkpoint exists before importing src.demo.app
FINETUNED_DIR = REPO_ROOT / "models" / "nli-deberta-v3-finetuned"
if not FINETUNED_DIR.exists():
    print("[Setup] models/nli-deberta-v3-finetuned not found. Training Stage 2 Cross-Encoder first...", flush=True)
    subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "train_stage2_cross_encoder.py")], check=True)

# 2. Enable GPU in src.demo.app
os.environ["ALLOW_GPU"] = "1"

import pypdf
import src.demo.app as demo_app

PDF_DIR = REPO_ROOT / "src" / "demo" / "sample_cases" / "pdf"
OUT_JSON = REPO_ROOT / "output" / "tier3_kaggle_full_audit_all10.json"
OUT_TXT = REPO_ROOT / "output" / "tier3_kaggle_conflicts_with_xai.txt"

FILES = [
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


def extract_top_xai_tokens(xai_html: str, top_k: int = 12):
    """Extracts top-k highest-weighted tokens from rendered XAI HTML spans."""
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
    # Sort descending by weight, deduplicate keeping max weight per lowercased token
    tokens.sort(key=lambda x: x[1], reverse=True)
    seen = set()
    unique_top = []
    for tok, w in tokens:
        key = tok.lower()
        if key not in seen:
            seen.add(key)
            unique_top.append({"token": tok, "weight": w})
        if len(unique_top) >= top_k:
            break
    return unique_top


def extract_ui_conflict_pairs(audit: dict):
    """Exact mirror of src/demo/static/index.html Option B (Preemption-Pair View) with XAI tokens."""
    pairs = []
    for sec in audit.get("sections", []):
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
                stat_html = c.get("statute_html") or sec.get("statute_html") or ""
                ord_html = c.get("ordinance_html") or sec.get("ordinance_html") or ""
                pairs.append({
                    "sec_num": sec.get("sec_num"),
                    "sec_title": sec.get("sec_title"),
                    "target_statute": c.get("citation") or sec.get("target_statute"),
                    "statute_title": c.get("title") or sec.get("statute_title") or "",
                    "stage1_rank": c.get("rank"),
                    "stage1_similarity": c.get("similarity"),
                    "p_contradiction": c.get("p_contradiction"),
                    "p_entailment": c.get("p_entailment"),
                    "p_neutral": c.get("p_neutral"),
                    "stage2_confidence_pct": c.get("stage2_confidence"),
                    "dynamic_threshold": c.get("dynamic_threshold", 0.45),
                    "dynamic_threshold_pct": c.get("dynamic_threshold_pct", 45.0),
                    "graph_distance_d_g": c.get("graph_distance_d_g"),
                    "domain": c.get("domain"),
                    "relation_type": c.get("relation_type") or sec.get("relation_type"),
                    "salient_token_count": c.get("salient_token_count", sec.get("salient_token_count", 0)),
                    "top_ordinance_xai_tokens": extract_top_xai_tokens(ord_html, top_k=25),
                    "top_statute_xai_tokens": extract_top_xai_tokens(stat_html, top_k=25),
                    "ordinance_text": (sec.get("ordinance_text") or sec.get("text") or "").strip(),
                    "statute_text": (c.get("raw_text") or c.get("prepended_text") or sec.get("statute_text") or "").strip(),
                })
        elif sec.get("verdict") == "CONTRADICTION":
            pairs.append({
                "sec_num": sec.get("sec_num"),
                "sec_title": sec.get("sec_title"),
                "target_statute": sec.get("target_statute"),
                "statute_title": sec.get("statute_title") or "",
                "stage1_rank": "fallback",
                "stage1_similarity": None,
                "p_contradiction": sec.get("conflict_probability"),
                "p_entailment": None,
                "p_neutral": None,
                "stage2_confidence_pct": sec.get("confidence_percentage"),
                "dynamic_threshold": sec.get("dynamic_threshold", 0.45),
                "dynamic_threshold_pct": sec.get("dynamic_threshold_pct", 45.0),
                "graph_distance_d_g": sec.get("graph_distance_d_g"),
                "domain": None,
                "relation_type": sec.get("relation_type"),
                "salient_token_count": sec.get("salient_token_count", 0),
                "top_ordinance_xai_tokens": extract_top_xai_tokens(sec.get("ordinance_html") or "", top_k=25),
                "top_statute_xai_tokens": extract_top_xai_tokens(sec.get("statute_html") or "", top_k=25),
                "ordinance_text": (sec.get("ordinance_text") or sec.get("text") or "").strip(),
                "statute_text": (sec.get("statute_text") or "").strip(),
            })
    return pairs


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    print(f"[Engine] Device={demo_app.NEURAL_ENGINE.device} | Checkpoint={demo_app.DEBERTA_LOCAL_PATH}", flush=True)
    all_results = {}
    if OUT_JSON.exists():
        try:
            all_results = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        except Exception:
            all_results = {}

    hash_cache = {}
    for case_id, pdf_name in FILES:
        pdf_path = PDF_DIR / pdf_name
        file_hash = sha256_file(pdf_path)

        if case_id in all_results:
            print(f"[SKIP] {case_id} already cached.", flush=True)
            hash_cache[file_hash] = all_results[case_id]
            continue

        if file_hash in hash_cache:
            print(f"[REUSE] {case_id} ({pdf_name}) has identical SHA256 to {hash_cache[file_hash]['case_id']}; reusing audit.", flush=True)
            cloned = dict(hash_cache[file_hash])
            cloned["case_id"] = case_id
            cloned["pdf_name"] = pdf_name
            all_results[case_id] = cloned
        else:
            print(f"[START] {case_id} ({pdf_name})...", flush=True)
            reader = pypdf.PdfReader(str(pdf_path))
            raw_text = "\n\n".join(page.extract_text() or "" for page in reader.pages).strip()
            t0 = time.perf_counter()
            audit = demo_app.execute_full_ordinance_audit(raw_text, pdf_name, doc_id=case_id)
            dt = time.perf_counter() - t0
            ui_pairs = extract_ui_conflict_pairs(audit)
            all_results[case_id] = {
                "case_id": case_id,
                "pdf_name": pdf_name,
                "wall_time_s": round(dt, 2),
                "total_sections": audit.get("total_sections"),
                "counts": audit.get("counts"),
                "ui_conflict_count": len(ui_pairs),
                "ui_conflict_pairs": ui_pairs,
                "audit": audit,
            }
            hash_cache[file_hash] = all_results[case_id]
            print(
                f"[DONE] {case_id} | {dt:.1f}s | Secs={audit.get('total_sections')} | UI Conflicts={len(ui_pairs)}",
                flush=True,
            )

        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json.dumps(all_results, indent=2, ensure_ascii=False), encoding="utf-8")

    # Write human-readable XAI + conflict report
    lines = []
    for cid in [f[0] for f in FILES]:
        entry = all_results[cid]
        pairs = entry["ui_conflict_pairs"]
        lines.append("=" * 100)
        lines.append(f"{cid} | {entry['pdf_name']} | Secs={entry['total_sections']} | UI Conflicts={len(pairs)}")
        lines.append("-" * 100)
        for i, p in enumerate(pairs, 1):
            ord_toks = ", ".join(f"{t['token']}({t['weight']})" for t in p["top_ordinance_xai_tokens"][:8])
            stat_toks = ", ".join(f"{t['token']}({t['weight']})" for t in p["top_statute_xai_tokens"][:8])
            lines.append(
                f"  [{i}] Sec {p['sec_num']} ({p['sec_title']}) <-> {p['target_statute']} "
                f"| Stage1_Rank={p['stage1_rank']} | P_c={p['stage2_confidence_pct']}% | tau={p['dynamic_threshold_pct']}% | d_g={p['graph_distance_d_g']}"
            )
            lines.append(f"      XAI Draft Tokens  : {ord_toks}")
            lines.append(f"      XAI Statute Tokens: {stat_toks}")
            lines.append(f"      Draft Text        : {p['ordinance_text'][:400].replace(chr(10), ' ')}")
            lines.append(f"      Statute Text      : {p['statute_text'][:400].replace(chr(10), ' ')}")
            lines.append("")
    OUT_TXT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nSaved full JSON to {OUT_JSON}\nSaved XAI conflict summary to {OUT_TXT}", flush=True)


if __name__ == "__main__":
    main()

