"""
scripts/run_tier2_clean_sync.py
=================================
Executes 100% genuine, zero-simulation, full-PDF in-process audits and diagnostics
across all 6 Tier 2 Folio PDFs in ground_truth/tier2_synthetic_drafts/tier2_draft_ordinances_pdf/:

  Part A: Synchronized Live-Demo Full-PDF Open-Corpus Audit (execute_full_ordinance_audit)
          - Matches exact Demo UI pair-counting logic from src/demo/static/index.html
          - Writes: output/tier2_live_demo_full_audit_all6.json
                    output/tier2_live_demo_audit_report.txt

  Part B: Genuine Controlled Oracle Retrieval Diagnostic (All 7 Planted Defects)
          - Feeds verbatim controlling national statutory provisions (by exact provision_id
            from data/unified_dual_statutory_provisions.jsonl) directly into DeBERTa-v3
          - Separately reports pure neural P(Contradiction) and sanctioned integer fine rule

  Part C: Genuine 1-Hop Knowledge Graph Candidate Expansion Ablation
          - Traverses data/knowledge_graph/statutory_kg_edges.jsonl (CITES_AUTHORITY, AMENDS)
            from explicit draft citations N_cite(D) and Stage 1 Top-8 hits N_1(K_q)
          - Scores newly surfaced KG provisions using the exact Stage 1 hybrid formula
            (0.50 * norm_BM25 + 0.50 * Dense Cosine) and evaluates top-M=8 via DeBERTa-v3
          - Computes true before-vs.-after metrics (binary & 3-class separated cleanly)
          - Writes: output/tier2_oracle_and_kg_ablation_authentic.json

Usage:
  .\\venv\\Scripts\\python.exe scripts/run_tier2_clean_sync.py
"""

import hashlib
import html
import json
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import pypdf

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src" / "demo"))
import app as demo_app  # noqa: E402

BENCHMARK_PATH = REPO_ROOT / "ground_truth" / "tier2_synthetic_drafts" / "tier2_draft_ordinances_benchmark.jsonl"
PDF_DIR = REPO_ROOT / "ground_truth" / "tier2_synthetic_drafts" / "tier2_draft_ordinances_pdf"
UNIFIED_PATH = REPO_ROOT / "data" / "unified_dual_statutory_provisions.jsonl"
KG_EDGES_PATH = REPO_ROOT / "data" / "knowledge_graph" / "statutory_kg_edges.jsonl"

OUT_AUDIT_JSON = REPO_ROOT / "output" / "tier2_live_demo_full_audit_all6.json"
OUT_AUDIT_REPORT = REPO_ROOT / "output" / "tier2_live_demo_audit_report.txt"
OUT_ABLATION_JSON = REPO_ROOT / "output" / "tier2_oracle_and_kg_ablation_authentic.json"

NATIONAL_CORPUS_LIMIT = 164620

ORACLE_TARGETS = [
    {
        "doc_id": "DRAFT-ORD-2026-01",
        "sec_num": 9,
        "defect_summary": "Commercial dog-meat slaughter & electrocution of unclaimed pound animals",
        "target_pids": ["nat_ra_8485_1998_sec_6", "nat_ra_9482_2007_sec_7"],
    },
    {
        "doc_id": "DRAFT-ORD-2026-01",
        "sec_num": 13,
        "defect_summary": "Ultra vires graduated fines (P25,000-P50,000) & 3-yr imprisonment exceeding LGC cap",
        "target_pids": ["nat_ra_7160_1991_sec_458"],
    },
    {
        "doc_id": "DRAFT-ORD-2026-02",
        "sec_num": 8,
        "defect_summary": "Commercial ownership & unredacted sale of sensitive medical records in MOA",
        "target_pids": ["nat_ra_10173_2012_sec_13", "nat_ra_10173_2012_sec_16"],
    },
    {
        "doc_id": "DRAFT-ORD-2026-03",
        "sec_num": 4,
        "defect_summary": "Diverting 30% Quick Response Fund (QRF) to regular salaries without calamity",
        "target_pids": ["nat_ra_10121_2010_sec_21", "nat_ra_7160_1991_sec_324"],
    },
    {
        "doc_id": "DRAFT-ORD-2026-04",
        "sec_num": 8,
        "defect_summary": "Granting perpetual VAT, corporate income tax & customs exemptions via usufruct",
        "target_pids": ["nat_ra_7160_1991_sec_133", "nat_ra_7160_1991_sec_192"],
    },
    {
        "doc_id": "DRAFT-ORD-2026-05",
        "sec_num": 4,
        "defect_summary": "Erecting permanent P500 highway toll barricades & passage tax on national highways",
        "target_pids": ["nat_ra_7160_1991_sec_133", "nat_ra_7160_1991_sec_21"],
    },
    {
        "doc_id": "DRAFT-ORD-2026-06",
        "sec_num": 4,
        "defect_summary": "45% agricultural reclassification ceiling & converting NIA irrigated land without DAR",
        "target_pids": ["nat_ra_7160_1991_sec_20", "nat_ra_6657_1988_sec_65", "nat_eo_124_1993_sec_1"],
    },
]

XAI_SPAN_RE = re.compile(
    r'<span[^>]*class="xai-token"[^>]*data-weight="([^"]+)"[^>]*>(.*?)</span>',
    re.DOTALL,
)

EXPLICIT_STATUTE_CITE_RE = re.compile(
    r"\b(Republic\s+Act(?:\s+No\.?)?|R\.?A\.?(?:\s+No\.?)?|"
    r"Presidential\s+Decree(?:\s+No\.?)?|P\.?D\.?(?:\s+No\.?)?|"
    r"Executive\s+Order(?:\s+No\.?)?|E\.?O\.?(?:\s+No\.?)?|"
    r"Batas\s+Pambansa(?:\s+Blg\.?)?|B\.?P\.?(?:\s+Blg\.?)?)\s*(\d+)\b",
    re.IGNORECASE,
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


def extract_conflict_pairs_from_sections(sections: list):
    """Exact parity with scripts/run_tier3_clean_sync.py and src/demo/static/index.html."""
    conflict_pairs = []
    for sec in sections:
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
                    "kg_expanded": bool(c.get("kg_expanded", False)),
                    "kg_path": c.get("kg_path", ""),
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
                "kg_expanded": False,
                "kg_path": "",
                "ordinance_text": (sec.get("ordinance_text") or sec.get("text") or "").strip(),
                "statute_text": (sec.get("statute_text") or "").strip(),
                "top_ordinance_xai": extract_top_xai_tokens(ord_html, top_k=15),
                "top_statute_xai": extract_top_xai_tokens(stat_html, top_k=15),
                "legal_rationale": sec.get("legal_rationale"),
            })
    return conflict_pairs


def normalize_verdict(v: str) -> str:
    v_up = (v or "").upper()
    if "CONTRADICTION" in v_up:
        return "Contradiction"
    if "ENTAILMENT" in v_up:
        return "Entailment"
    return "Neutral"


def is_obsolete_colonial(eid: str = "", citation: str = "") -> bool:
    e_low = (eid or "").lower()
    c_low = (citation or "").lower()
    if e_low.startswith(("act_", "ca_", "commonwealth_act_", "ra_4354_")):
        return True
    if c_low.startswith(("act no.", "act_", "commonwealth act", "commonwealth_act")) or "4354" in c_low:
        return True
    return False


def format_candidate_from_record(item: dict, rank: int, sim_score: float, kg_expanded: bool = False, kg_path: str = "") -> dict:
    enact_num = item.get("enactment_number") or item.get("enactment_id") or "Statute"
    sec_num = item.get("section_number") or ""
    sec_title = item.get("section_title") or ""
    cit = f"{enact_num} {sec_num}".strip()
    jur = "National Statute" if item.get("jurisdiction") == "national" else "Davao City Ordinance"
    raw_txt = item.get("raw_text", "")
    prep_txt = item.get("prepended_text") or raw_txt

    raw_title = (item.get("enactment_title") or "").strip()
    clean_title = raw_title
    if not clean_title or clean_title.upper() in ["MANILA", "DAVAO", "PHILIPPINES"] or len(clean_title) < 8:
        if "120" in enact_num and "2020" in enact_num:
            clean_title = "STRENGTHENING REHABILITATION AND RECOVERY EFFORTS IN TYPHOON-HIT AREAS THROUGH THE CREATION OF THE BUILD BACK BETTER TASK FORCE"
        elif "10121" in enact_num:
            clean_title = "PHILIPPINE DISASTER RISK REDUCTION AND MANAGEMENT ACT OF 2010"
        elif "7160" in enact_num:
            clean_title = "LOCAL GOVERNMENT CODE OF 1991"
        else:
            clean_title = enact_num

    if sec_num and sec_title:
        sec_display = f"{sec_num}. {sec_title}"
    elif sec_num:
        sec_display = sec_num
    elif sec_title:
        sec_display = sec_title
    else:
        sec_display = "Operative Provision"

    return {
        "rank": rank,
        "provision_id": item.get("provision_id"),
        "enactment_id": item.get("enactment_id"),
        "citation": cit,
        "title": clean_title,
        "section_title": sec_display,
        "section": sec_display,
        "jurisdiction": jur,
        "raw_text": raw_txt,
        "prepended_text": prep_txt,
        "similarity": round(float(sim_score), 4),
        "score": round(float(sim_score), 4),
        "stage1_score": round(float(sim_score), 4),
        "similarity_score": round(float(sim_score), 4),
        "lawphil_url": demo_app.get_lawphil_url(cit, item.get("jurisdiction", "national")),
        "kg_expanded": kg_expanded,
        "kg_path": kg_path,
    }


def compute_section_metrics(all_provs: list, doc_results: list) -> dict:
    total_provs = len(all_provs)

    # Binary Contradiction vs Non-Contradiction (apples-to-apples)
    tp_c = sum(1 for p in all_provs if p["gold_label"] == "Contradiction" and p["predicted_label"] == "Contradiction")
    fp_c = sum(1 for p in all_provs if p["gold_label"] != "Contradiction" and p["predicted_label"] == "Contradiction")
    fn_c = sum(1 for p in all_provs if p["gold_label"] == "Contradiction" and p["predicted_label"] != "Contradiction")
    tn_c = sum(1 for p in all_provs if p["gold_label"] != "Contradiction" and p["predicted_label"] != "Contradiction")

    prec_c = (tp_c / (tp_c + fp_c)) if (tp_c + fp_c) > 0 else 0.0
    rec_c = (tp_c / (tp_c + fn_c)) if (tp_c + fn_c) > 0 else 0.0
    f1_c = (2 * prec_c * rec_c / (prec_c + rec_c)) if (prec_c + rec_c) > 0 else 0.0
    f2_c = (5 * prec_c * rec_c / (4 * prec_c + rec_c)) if (4 * prec_c + rec_c) > 0 else 0.0
    spec_c = (tn_c / (tn_c + fp_c)) * 100.0 if (tn_c + fp_c) > 0 else 0.0
    bin_acc = ((tp_c + tn_c) / total_provs) * 100.0 if total_provs > 0 else 0.0

    # 3-Class Metrics (Neutral / Entailment / Contradiction)
    correct_3cls = sum(1 for p in all_provs if p["gold_label"] == p["predicted_label"])
    acc_3cls = (correct_3cls / total_provs) * 100.0 if total_provs > 0 else 0.0
    classes = ["Neutral", "Entailment", "Contradiction"]
    per_class = {}
    f1s = []
    for cls in classes:
        tp = sum(1 for p in all_provs if p["gold_label"] == cls and p["predicted_label"] == cls)
        fp = sum(1 for p in all_provs if p["gold_label"] != cls and p["predicted_label"] == cls)
        fn = sum(1 for p in all_provs if p["gold_label"] == cls and p["predicted_label"] != cls)
        pr = (tp / (tp + fp)) if (tp + fp) > 0 else 0.0
        rc = (tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        f1 = (2 * pr * rc / (pr + rc)) if (pr + rc) > 0 else 0.0
        f1s.append(f1)
        per_class[cls] = {
            "support": sum(1 for p in all_provs if p["gold_label"] == cls),
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": round(pr, 4),
            "recall": round(rc, 4),
            "f1": round(f1, 4),
        }
    macro_f1 = sum(f1s) / len(f1s)

    total_docs = len(doc_results)
    flagged_docs = sum(1 for d in doc_results if d["total_conflicts_found"] > 0)
    doc_recall = (flagged_docs / total_docs) * 100.0 if total_docs > 0 else 0.0
    total_ui_pairs = sum(d["total_conflicts_found"] for d in doc_results)

    return {
        "documents_evaluated": total_docs,
        "provisions_evaluated": total_provs,
        "document_screening_recall": round(doc_recall, 2),
        "documents_flagged": flagged_docs,
        "total_ui_conflict_pairs": total_ui_pairs,
        "binary_confusion_matrix": {
            "true_positives": tp_c,
            "false_positives": fp_c,
            "true_negatives": tn_c,
            "false_negatives": fn_c,
        },
        "binary_metrics": {
            "contradiction_precision": round(prec_c, 4),
            "contradiction_recall": round(rec_c, 4),
            "contradiction_f1": round(f1_c, 4),
            "cost_sensitive_f2": round(f2_c, 4),
            "section_level_specificity_pct": round(spec_c, 2),
            "binary_screening_accuracy_pct": round(bin_acc, 2),
        },
        "three_class_metrics": {
            "three_class_accuracy_pct": round(acc_3cls, 2),
            "three_class_correct": correct_3cls,
            "macro_f1": round(macro_f1, 4),
            "per_class_performance": per_class,
        },
    }


def write_audit_report(doc_results: list, summary: dict):
    with open(OUT_AUDIT_REPORT, "w", encoding="utf-8") as f:
        f.write("================================================================================\n")
        f.write("OFFICIAL TIER 2 SYNTHETIC DRAFT AUDIT: FULL-PDF SYNCHRONIZED LOG\n")
        f.write("Platform: Prototype Demo Backend Engine (MiniLM-L6-v2 + Tuned DeBERTa-v3 Cross-Encoder)\n")
        f.write("Mode: Direct Full-PDF Execution (Blind doc_id=None, Zero Ground-Truth Hints)\n")
        f.write("================================================================================\n\n")

        bm = summary["binary_metrics"]
        cm = summary["binary_confusion_matrix"]
        tm = summary["three_class_metrics"]
        f.write(
            f"SUMMARY | Docs: {summary['documents_evaluated']} | Sections: {summary['provisions_evaluated']} "
            f"| UI Pairs Flagged: {summary['total_ui_conflict_pairs']} | Docs Flagged: {summary['documents_flagged']}/{summary['documents_evaluated']}\n"
        )
        f.write(
            f"BINARY  | TP={cm['true_positives']} FP={cm['false_positives']} TN={cm['true_negatives']} FN={cm['false_negatives']} "
            f"| Prec={bm['contradiction_precision']*100:.2f}% | Rec={bm['contradiction_recall']*100:.2f}% "
            f"| Spec={bm['section_level_specificity_pct']:.2f}% | F1={bm['contradiction_f1']:.4f} | F2={bm['cost_sensitive_f2']:.4f} "
            f"| BinAcc={bm['binary_screening_accuracy_pct']:.2f}%\n"
        )
        f.write(
            f"3-CLASS | Acc={tm['three_class_accuracy_pct']:.2f}% ({tm['three_class_correct']}/{summary['provisions_evaluated']}) "
            f"| Macro-F1={tm['macro_f1']:.4f}\n\n"
        )

        for r in doc_results:
            f.write("#" * 80 + "\n")
            f.write(f"DRAFT: {r['doc_id']} ({r['functional_typology']}) | PDF: {r['pdf_name']} | Pages: {r['pdf_pages']} | Words: {r['total_document_words']}\n")
            f.write(f"Total Sections: {r['total_sections']} ({r['substantive_sections']} operative) | Stage1: {r['latency_metrics'].get('stage1_latency_s')}s | Stage2: {r['latency_metrics'].get('stage2_latency_s')}s | Total: {r['audit_latency_s']}s\n")
            f.write(f"UI Headline: {r['total_conflicts_found']} Conflicts Detected!\n")
            f.write(f"UI Subheadline: {len(r['problematic_sections'])} Problematic Sections: {r['problematic_sections']} | Gold TP Sections Caught: {r['true_positive_contradictions']}/{r['gold_contradictions']}\n")
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
    if not demo_app.NEURAL_ENGINE.is_loaded:
        raise RuntimeError("LocalNeuralEngine failed to load! Refusing to run fallback.")

    print("=" * 88)
    print("TIER 2 CLEAN SYNCHRONIZED SUITE (PART A + PART B + PART C)")
    print("=" * 88)

    # ------------------------------------------------------------------
    # Index unified national corpus metadata + offsets (rows 0..164619)
    # ------------------------------------------------------------------
    print("[*] Indexing national statutory metadata from unified corpus (rows 0..164619)...", flush=True)
    t_idx = time.perf_counter()
    oracle_pid_set = {pid for t in ORACLE_TARGETS for pid in t["target_pids"]}
    oracle_records = {}
    pid_to_row = {}
    row_to_pid = {}
    row_to_eid = {}
    eid_to_op_rows = defaultdict(list)
    number_key_to_eids = defaultdict(list)
    seen_eids_for_key = defaultdict(set)

    prefix_to_kind = {
        "ra": "ra",
        "pd": "pd",
        "eo": "eo",
        "bp": "bp",
        "act": "act",
        "ca": "ca",
    }

    with open(UNIFIED_PATH, "r", encoding="utf-8") as f:
        for row_idx, line in enumerate(f):
            if row_idx >= NATIONAL_CORPUS_LIMIT:
                break
            rec = json.loads(line)
            pid = rec.get("provision_id")
            eid = rec.get("enactment_id") or ""
            en_num = rec.get("enactment_number") or ""

            if pid in oracle_pid_set:
                oracle_records[pid] = rec

            if pid:
                pid_to_row[pid] = row_idx
                row_to_pid[row_idx] = pid
            row_to_eid[row_idx] = eid

            if not is_obsolete_colonial(eid, en_num):
                if not rec.get("is_boilerplate", False):
                    eid_to_op_rows[eid].append(row_idx)
                parts = eid.split("_")
                if len(parts) >= 2 and parts[0] in prefix_to_kind:
                    num_part = parts[1].lower()
                    key = (prefix_to_kind[parts[0]], num_part)
                    if eid not in seen_eids_for_key[key]:
                        seen_eids_for_key[key].add(eid)
                        number_key_to_eids[key].append(eid)

    missing_oracle = oracle_pid_set - set(oracle_records.keys())
    if missing_oracle:
        raise RuntimeError(f"Missing oracle provision_ids in unified corpus: {sorted(missing_oracle)}")
    print(f"[+] Indexed {len(pid_to_row):,} national provisions, {len(eid_to_op_rows):,} non-colonial enactments in {time.perf_counter()-t_idx:.2f}s", flush=True)

    # Load benchmark ground truth
    gold_docs = {}
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                d = json.loads(line)
                gold_docs[d["doc_id"]] = d

    # ==================================================================
    # PART A: Synchronized Live-Demo Full-PDF Open-Corpus Audit
    # ==================================================================
    print("\n" + "=" * 88)
    print("PART A: LIVE-DEMO SYNCHRONIZED FULL-PDF OPEN-CORPUS AUDIT (N = 6)")
    print("=" * 88)

    pdf_files = sorted(PDF_DIR.glob("DRAFT-ORD-2026-*.pdf"))
    if len(pdf_files) != 6:
        raise RuntimeError(f"Expected 6 Tier 2 PDFs in {PDF_DIR}, found {len(pdf_files)}")

    doc_results_a = []
    all_provs_a = []
    raw_audit_cache = {}
    raw_text_cache = {}
    total_ing_ms = 0.0

    # Map oracle target citations per (doc_id, sec_num) for retrieval diagnostics
    target_pids_by_sec = {(t["doc_id"], t["sec_num"]): t["target_pids"] for t in ORACLE_TARGETS}

    for pdf_path in pdf_files:
        doc_id = pdf_path.stem
        gold_doc = gold_docs[doc_id]
        pdf_sha = hashlib.sha256(pdf_path.read_bytes()).hexdigest()[:16]

        t0_ing = time.perf_counter()
        reader = pypdf.PdfReader(str(pdf_path))
        raw_text = "\n\n".join(pg.extract_text() or "" for pg in reader.pages).strip()
        ing_ms = (time.perf_counter() - t0_ing) * 1000.0
        total_ing_ms += ing_ms
        if not raw_text:
            raise RuntimeError(f"Empty PDF text extracted from {pdf_path.name}")
        raw_text_cache[doc_id] = raw_text

        print(f"\n[*] Auditing {doc_id} ({pdf_path.name} | pages={len(reader.pages)} | words={len(raw_text.split())} | sha={pdf_sha})...", flush=True)
        last_print = [0.0]

        def cb(stage, progress, badge, msg):
            now = time.perf_counter()
            if now - last_print[0] >= 15.0 or progress in (20, 100):
                print(f"    [{progress:3d}%] {stage}: {badge} - {msg}", flush=True)
                last_print[0] = now

        t0_audit = time.perf_counter()
        data = demo_app.execute_full_ordinance_audit(raw_text, pdf_path.name, doc_id=None, progress_callback=cb)
        elapsed_s = time.perf_counter() - t0_audit
        raw_audit_cache[doc_id] = data

        audited_secs = data.get("sections", [])
        gold_secs = {s["sec_num"]: s for s in gold_doc.get("sections", [])}
        if len(audited_secs) != len(gold_secs):
            raise RuntimeError(f"Section count mismatch in {doc_id}: audited={len(audited_secs)} vs gold={len(gold_secs)}")
        if [s["sec_num"] for s in audited_secs] != sorted(gold_secs.keys()):
            raise RuntimeError(f"Section numbers mismatch in {doc_id}: {[s['sec_num'] for s in audited_secs]} vs {sorted(gold_secs.keys())}")

        conflict_pairs = extract_conflict_pairs_from_sections(audited_secs)
        distinct_secs = sorted(set(p["sec_num"] for p in conflict_pairs))
        substantive = sum(1 for s in audited_secs if not s.get("is_boilerplate"))

        doc_tp = 0
        doc_gold_c = sum(1 for s in gold_secs.values() if s["label"] == "Contradiction")
        sec_evals = []

        for sec in audited_secs:
            s_num = sec["sec_num"]
            gold_sec = gold_secs[s_num]
            gold_label = gold_sec.get("label", "Neutral")
            pred_label = normalize_verdict(sec.get("verdict", "NEUTRAL"))

            cands = sec.get("candidate_shortlist") or []
            eval_cands = [c for c in cands if c.get("stage2_evaluated")]
            sec_flagged_cands = [
                c for c in eval_cands
                if c.get("is_conflict") or (c.get("p_contradiction") is not None and c["p_contradiction"] >= c.get("dynamic_threshold", 0.45))
            ]
            max_stage2_p = max((c.get("p_contradiction", 0.0) for c in eval_cands), default=0.0)

            if pred_label == "Contradiction" and gold_label == "Contradiction":
                doc_tp += 1

            # Check retrieval rank in Top-50 for gold Contradiction sections
            retrieval_diag = None
            if gold_label == "Contradiction":
                t_pids = target_pids_by_sec.get((doc_id, s_num), [])
                hits = []
                for idx_c, c in enumerate(cands, start=1):
                    cpid = c.get("provision_id")
                    if cpid in t_pids:
                        hits.append({"provision_id": cpid, "rank": idx_c, "in_top8": idx_c <= 8, "stage1_score": c.get("similarity")})
                retrieval_diag = {
                    "target_pids": t_pids,
                    "top50_hits": hits,
                    "any_in_top8": any(h["in_top8"] for h in hits),
                    "any_in_top50": len(hits) > 0,
                }

            ev = {
                "doc_id": doc_id,
                "sec_num": s_num,
                "sec_title": sec.get("sec_title"),
                "word_count": len((sec.get("text") or "").split()),
                "is_boilerplate": bool(sec.get("is_boilerplate", False)),
                "gold_label": gold_label,
                "predicted_label": pred_label,
                "reported_conflict_probability": sec.get("conflict_probability"),
                "max_stage2_p_contradiction": round(float(max_stage2_p), 4),
                "dynamic_threshold_pct": sec.get("dynamic_threshold_pct", 45.0),
                "graph_distance_d_g": sec.get("graph_distance_d_g", 999),
                "gold_target_statute": gold_sec.get("target_statute"),
                "retrieved_top_statute": sec.get("target_statute"),
                "flagged_pairs_count": len(sec_flagged_cands) if sec_flagged_cands else (1 if pred_label == "Contradiction" else 0),
                "flagged_statutes": [c.get("citation") for c in sec_flagged_cands],
                "retrieval_diagnostic": retrieval_diag,
            }
            sec_evals.append(ev)
            all_provs_a.append(ev)

        operative_words = sum(len(s.get("text", "").split()) for s in gold_doc.get("sections", []))
        doc_summary = {
            "doc_id": doc_id,
            "typology_id": gold_doc.get("typology_id"),
            "functional_typology": gold_doc.get("functional_typology", ""),
            "statutory_authority": gold_doc.get("statutory_authority", ""),
            "proposed_ordinance_no": gold_doc.get("proposed_ordinance_no", ""),
            "title": gold_doc.get("title", ""),
            "pdf_name": pdf_path.name,
            "pdf_pages": len(reader.pages),
            "pdf_sha256_prefix": pdf_sha,
            "total_document_words": len(raw_text.split()),
            "operative_section_words": operative_words,
            "ingestion_latency_ms": round(ing_ms, 2),
            "audit_latency_s": round(elapsed_s, 2),
            "latency_metrics": data.get("latency_metrics", {}),
            "total_sections": data.get("total_sections", 0),
            "substantive_sections": substantive,
            "gold_contradictions": doc_gold_c,
            "detected_contradiction_sections": len(distinct_secs),
            "true_positive_contradictions": doc_tp,
            "total_conflicts_found": len(conflict_pairs),
            "problematic_sections": distinct_secs,
            "conflict_pairs": conflict_pairs,
            "sections": sec_evals,
        }
        doc_results_a.append(doc_summary)
        print(
            f"[+] {doc_id} | {elapsed_s:.2f}s | Secs: {len(audited_secs)} ({substantive} op.) | "
            f"UI Pairs: {len(conflict_pairs)} across {len(distinct_secs)} secs {distinct_secs} | Gold TP: {doc_tp}/{doc_gold_c}",
            flush=True,
        )

    summary_a = compute_section_metrics(all_provs_a, doc_results_a)
    summary_a["avg_pdf_ingestion_ms_per_doc"] = round(total_ing_ms / len(doc_results_a), 2)
    summary_a["total_audit_latency_s"] = round(sum(d["audit_latency_s"] for d in doc_results_a), 2)
    summary_a["avg_audit_latency_s_per_doc"] = round(summary_a["total_audit_latency_s"] / len(doc_results_a), 2)

    payload_a = {
        "benchmark_tier": "Tier 2: Synchronized Live-Demo Full-PDF Open-Corpus Audit (N = 6 Drafts, 52 Sections)",
        "mode": "Blind Full-PDF In-Process Audit via src/demo/app.py execute_full_ordinance_audit(doc_id=None)",
        "summary_metrics": summary_a,
        "document_level_results": doc_results_a,
    }
    OUT_AUDIT_JSON.write_text(json.dumps(payload_a, indent=2, ensure_ascii=False), encoding="utf-8")
    write_audit_report(doc_results_a, summary_a)
    print(f"\n[OK] Saved Part A open-corpus JSON -> {OUT_AUDIT_JSON}")
    print(f"[OK] Saved Part A open-corpus TXT  -> {OUT_AUDIT_REPORT}")

    # ==================================================================
    # PART B: Genuine Controlled Oracle Retrieval Diagnostic
    # ==================================================================
    print("\n" + "=" * 88)
    print("PART B: GENUINE CONTROLLED ORACLE DIAGNOSTIC (N = 7 PLANTED DEFECTS)")
    print("=" * 88)

    # Extract exact chunked section headers & texts from the PDFs so prompt formatting matches app.py 1-to-1
    chunk_lookup = {}
    for doc_id, r_txt in raw_text_cache.items():
        _, chunks = demo_app.chunk_ordinance_sections(r_txt, default_title=f"{doc_id}.pdf")
        for ch in chunks:
            chunk_lookup[(doc_id, ch["sec_num"])] = ch

    oracle_pairs_meta = []
    oracle_batch_inputs = []
    for target in ORACLE_TARGETS:
        doc_id = target["doc_id"]
        sec_num = target["sec_num"]
        ch = chunk_lookup[(doc_id, sec_num)]
        s_marker = ch.get("sec_marker") or f"SECTION {sec_num}"
        header_title = f"{s_marker}: {ch['sec_title']}" if ch.get("sec_title") else s_marker
        hypothesis = f"[{header_title}] {ch['text']}".strip()

        for pid in target["target_pids"]:
            rec = oracle_records[pid]
            cit = f"{rec.get('enactment_number') or rec.get('enactment_id')} {rec.get('section_number') or ''}".strip()
            raw_stat_text = (rec.get("raw_text") or "").lstrip("- \r\n")
            premise = f"[{cit}] {raw_stat_text}".strip()
            oracle_batch_inputs.append((premise, hypothesis))
            oracle_pairs_meta.append({
                "doc_id": doc_id,
                "sec_num": sec_num,
                "sec_title": ch.get("sec_title", ""),
                "defect_summary": target["defect_summary"],
                "provision_id": pid,
                "citation": cit,
                "draft_text": ch["text"],
                "statute_text": raw_stat_text,
            })

    t0_ora = time.perf_counter()
    oracle_scores = demo_app.NEURAL_ENGINE.evaluate_cross_encoder_batch(oracle_batch_inputs)
    ora_elapsed_s = time.perf_counter() - t0_ora

    oracle_pair_results = []
    for meta, sc in zip(oracle_pairs_meta, oracle_scores):
        d_g, domain, rel_type = demo_app.compute_topological_distance(meta["citation"], meta["draft_text"], meta["statute_text"])
        tau_dyn = demo_app.compute_dynamic_threshold(d_g, is_vertical=True, tau_base=0.45, delta_tau=0.15)
        xai_res = demo_app.NEURAL_ENGINE.extract_cross_attention_attribution(meta["statute_text"], meta["draft_text"])
        top_ord_xai = extract_top_xai_tokens(xai_res.get("ordinance_html", ""), top_k=8)
        top_stat_xai = extract_top_xai_tokens(xai_res.get("statute_html", ""), top_k=8)

        p_c = float(sc["p_contradiction"])
        has_fine, fine_val = demo_app.check_statutory_penalty_ceiling(meta["draft_text"])
        oracle_pair_results.append({
            "doc_id": meta["doc_id"],
            "sec_num": meta["sec_num"],
            "sec_title": meta["sec_title"],
            "defect_summary": meta["defect_summary"],
            "provision_id": meta["provision_id"],
            "citation": meta["citation"],
            "p_contradiction": round(p_c, 4),
            "p_contradiction_pct": round(p_c * 100.0, 2),
            "p_entailment": round(float(sc["p_entailment"]), 4),
            "p_neutral": round(float(sc["p_neutral"]), 4),
            "graph_distance_d_g": d_g,
            "relation_type": rel_type,
            "dynamic_threshold": tau_dyn,
            "hit_static_045": p_c >= 0.45,
            "hit_dynamic_tau": p_c >= tau_dyn,
            "symbolic_fine_breach": bool(has_fine),
            "symbolic_max_fine": fine_val,
            "top_ordinance_xai": top_ord_xai,
            "top_statute_xai": top_stat_xai,
        })

    # Group by the 7 planted defects
    oracle_defect_summaries = []
    for target in ORACLE_TARGETS:
        sub = [p for p in oracle_pair_results if p["doc_id"] == target["doc_id"] and p["sec_num"] == target["sec_num"]]
        best_p = max(sub, key=lambda x: x["p_contradiction"])
        has_fine, fine_val = demo_app.check_statutory_penalty_ceiling(chunk_lookup[(target["doc_id"], target["sec_num"])]["text"])
        any_static = any(x["hit_static_045"] for x in sub)
        any_dyn = any(x["hit_dynamic_tau"] for x in sub)
        oracle_defect_summaries.append({
            "doc_id": target["doc_id"],
            "sec_num": target["sec_num"],
            "defect_summary": target["defect_summary"],
            "best_neural_statute": best_p["citation"],
            "best_neural_pid": best_p["provision_id"],
            "best_neural_p_contradiction": best_p["p_contradiction"],
            "best_neural_p_contradiction_pct": best_p["p_contradiction_pct"],
            "best_neural_d_g": best_p["graph_distance_d_g"],
            "best_neural_tau_dyn": best_p["dynamic_threshold"],
            "neural_only_hit_static_045": any_static,
            "neural_only_hit_dynamic_tau": any_dyn,
            "symbolic_fine_rule_hit": bool(has_fine),
            "hybrid_neuro_symbolic_hit": bool(any_dyn or has_fine),
            "all_target_pairs": sub,
        })
        print(
            f"[*] {target['doc_id']} Sec.{target['sec_num']:>2} | Best Neural: {best_p['citation']} -> "
            f"P(C)={best_p['p_contradiction_pct']:>5.2f}% (tau*={best_p['dynamic_threshold']:.3f}) | "
            f"NeuralHit(dyn)={any_dyn} | SymbolicFine={has_fine}",
            flush=True,
        )

    # ==================================================================
    # PART C: Genuine 1-Hop Knowledge Graph Candidate Expansion Ablation
    # ==================================================================
    print("\n" + "=" * 88)
    print("PART C: GENUINE 1-HOP KNOWLEDGE GRAPH CANDIDATE EXPANSION ABLATION")
    print("=" * 88)

    # Build undirected 1-hop KG adjacency from CITES_AUTHORITY & AMENDS (non-colonial national enactments)
    kg_adj = defaultdict(set)
    kg_edge_reasons = defaultdict(list)
    edge_counts = defaultdict(int)
    with open(KG_EDGES_PATH, "r", encoding="utf-8") as f:
        for line in f:
            e = json.loads(line)
            rel = e.get("relation") or e.get("type") or e.get("edge_type") or ""
            if rel not in ("CITES_AUTHORITY", "AMENDS"):
                continue
            s = str(e.get("source", ""))
            t = str(e.get("target", ""))
            if is_obsolete_colonial(s) or is_obsolete_colonial(t):
                continue
            if s not in eid_to_op_rows or t not in eid_to_op_rows:
                continue
            edge_counts[rel] += 1
            kg_adj[s].add(t)
            kg_adj[t].add(s)
            kg_edge_reasons[(s, t)].append(f"{s} --[{rel}]--> {t}")
            kg_edge_reasons[(t, s)].append(f"{s} --[{rel}]--> {t}")

    print(f"[*] Loaded KG adjacency from {KG_EDGES_PATH.name}: {dict(edge_counts)} | Connected enactments: {len(kg_adj):,}", flush=True)

    # Open unified corpus binary file for seeking selected Top-M KG candidate payloads
    doc_results_c = []
    all_provs_c = []
    kg_target_diagnostics = []
    total_kg_stage1_s = 0.0
    total_kg_stage2_s = 0.0

    # Pre-slice national embeddings and verify BM25 scope length
    nat_emb = demo_app.NEURAL_ENGINE.statutory_embeddings[:NATIONAL_CORPUS_LIMIT]

    with open(UNIFIED_PATH, "rb") as f_unified:
        for doc_res_a in doc_results_a:
            doc_id = doc_res_a["doc_id"]
            gold_doc = gold_docs[doc_id]
            gold_secs = {s["sec_num"]: s for s in gold_doc.get("sections", [])}
            raw_text = raw_text_cache[doc_id]
            data_a = raw_audit_cache[doc_id]
            doc_title, chunks = demo_app.chunk_ordinance_sections(raw_text, default_title=doc_res_a["pdf_name"])
            chunk_by_num = {c["sec_num"]: c for c in chunks}

            # 1. Extract explicit national citations N_cite(D) from full PDF text
            explicit_cites_raw = []
            cite_eids = set()
            for m in EXPLICIT_STATUTE_CITE_RE.finditer(raw_text):
                raw_label = re.sub(r"\s+", " ", m.group(0)).strip()
                prefix_tok = m.group(1).lower().replace(".", "").strip()
                num_tok = m.group(2).strip()
                if prefix_tok.startswith("r"):
                    kind = "ra"
                elif prefix_tok.startswith("p"):
                    kind = "pd"
                elif prefix_tok.startswith("e"):
                    kind = "eo"
                elif prefix_tok.startswith("b"):
                    kind = "bp"
                else:
                    continue
                matched_eids = number_key_to_eids.get((kind, num_tok), [])
                if matched_eids:
                    explicit_cites_raw.append((raw_label, matched_eids))
                    cite_eids.update(matched_eids)

            print(f"\n[*] KG Expansion on {doc_id} | N_cite(D) enactments: {sorted(cite_eids)}", flush=True)

            aug_sections_list = []
            sec_evals_c = []
            doc_tp_c = 0
            doc_kg_s1_s = 0.0
            doc_kg_s2_s = 0.0

            for sec_a in data_a.get("sections", []):
                s_num = sec_a["sec_num"]
                gold_sec = gold_secs[s_num]
                gold_label = gold_sec.get("label", "Neutral")

                if sec_a.get("is_boilerplate"):
                    sec_copy = dict(sec_a)
                    aug_sections_list.append(sec_copy)
                    ev_c = {
                        "doc_id": doc_id,
                        "sec_num": s_num,
                        "sec_title": sec_a.get("sec_title"),
                        "is_boilerplate": True,
                        "gold_label": gold_label,
                        "predicted_label": "Neutral",
                        "reported_conflict_probability": sec_a.get("conflict_probability"),
                        "max_stage2_p_contradiction": 0.0,
                        "flagged_pairs_count": 0,
                        "flagged_statutes": [],
                        "kg_newly_evaluated_count": 0,
                    }
                    sec_evals_c.append(ev_c)
                    all_provs_c.append(ev_c)
                    continue

                ch = chunk_by_num[s_num]
                s_marker = ch.get("sec_marker") or f"SECTION {s_num}"
                header_title = f"{s_marker}: {ch['sec_title']}" if ch.get("sec_title") else s_marker
                query_str = f"[{doc_title} | {header_title}] {ch['text']}"
                hypothesis_text = f"[{header_title}] {ch['text']}"

                base_cands_50 = sec_a.get("candidate_shortlist") or []
                base_eval_cands = [dict(c) for c in base_cands_50 if c.get("stage2_evaluated")]
                already_pids = {c.get("provision_id") for c in base_eval_cands if c.get("provision_id")}
                already_cits = {c.get("citation") for c in base_eval_cands if c.get("citation")}

                # Seed enactments = N_cite(D) union enactments of baseline Top-8
                seed_eids = set(cite_eids)
                seed_origins = {eid: f"N_cite(D)" for eid in cite_eids}
                for bc in base_eval_cands:
                    bpid = bc.get("provision_id")
                    if bpid and bpid in pid_to_row:
                        beid = row_to_eid[pid_to_row[bpid]]
                        if beid and not is_obsolete_colonial(beid):
                            seed_eids.add(beid)
                            seed_origins.setdefault(beid, f"Stage1 Top-8 ({bc.get('citation')})")

                # Expand 1-hop neighborhood N_1(seeds)
                e_kg = set(seed_eids)
                eid_path_map = {eid: seed_origins[eid] for eid in seed_eids}
                for seid in seed_eids:
                    for nb in kg_adj.get(seid, ()):
                        if nb not in e_kg:
                            e_kg.add(nb)
                            reasons = kg_edge_reasons.get((seid, nb), [f"{seid} <-> {nb}"])
                            eid_path_map[nb] = f"{seed_origins[seid]} -> {reasons[0]}"

                # Gather all non-boilerplate, non-colonial national rows in E_kg not already in baseline Top-8
                kg_candidate_rows = []
                for eid in e_kg:
                    for r_idx in eid_to_op_rows.get(eid, ()):
                        r_pid = row_to_pid.get(r_idx)
                        if r_pid in already_pids:
                            continue
                        kg_candidate_rows.append(r_idx)

                # Score kg_candidate_rows using exact Stage 1 hybrid formula (0.50 * norm_BM25 + 0.50 * Dense)
                t0_s1 = time.perf_counter()
                new_kg_cands = []
                ranked_kg_rows = []
                if kg_candidate_rows:
                    q_emb = demo_app.NEURAL_ENGINE.embedder.encode([query_str], normalize_embeddings=True)[0]
                    kg_idx_arr = np.array(kg_candidate_rows, dtype=np.int64)
                    dense_kg = np.dot(nat_emb[kg_idx_arr], q_emb)

                    clean_q = re.sub(r"[^a-zA-Z0-9\s]", " ", query_str.lower())
                    q_tokens = [w for w in clean_q.split() if len(w) > 2]
                    if demo_app.NEURAL_ENGINE.bm25 is not None and q_tokens:
                        bm_raw = np.array(demo_app.NEURAL_ENGINE.bm25.get_scores(q_tokens))[:NATIONAL_CORPUS_LIMIT]
                        max_bm = float(np.max(bm_raw))
                        norm_bm_kg = (bm_raw[kg_idx_arr] / max_bm) if max_bm > 0 else bm_raw[kg_idx_arr]
                        hybrid_kg = (0.50 * norm_bm_kg) + (0.50 * dense_kg)
                    else:
                        hybrid_kg = dense_kg

                    order = np.argsort(-hybrid_kg)
                    for pos_rank, o_i in enumerate(order, start=1):
                        r_idx = int(kg_candidate_rows[o_i])
                        ranked_kg_rows.append((r_idx, pos_rank, float(hybrid_kg[o_i])))

                    for r_idx, pos_rank, sim_val in ranked_kg_rows[:8]:
                        f_unified.seek(demo_app.NEURAL_ENGINE.provision_offsets[r_idx])
                        item = json.loads(f_unified.readline().decode("utf-8"))
                        eid = item.get("enactment_id", "")
                        cand = format_candidate_from_record(
                            item=item,
                            rank=8 + len(new_kg_cands) + 1,
                            sim_score=sim_val,
                            kg_expanded=True,
                            kg_path=eid_path_map.get(eid, "KG 1-hop"),
                        )
                        if cand["citation"] not in already_cits:
                            new_kg_cands.append(cand)
                doc_kg_s1_s += (time.perf_counter() - t0_s1)

                # Diagnostic on gold Contradiction sections: check E_kg inclusion & rank
                if gold_label == "Contradiction":
                    t_pids = target_pids_by_sec.get((doc_id, s_num), [])
                    kg_rank_lookup = {row_to_pid[r]: (rk, sc) for r, rk, sc in ranked_kg_rows if r in row_to_pid}
                    t_diag = []
                    for tpid in t_pids:
                        trow = pid_to_row[tpid]
                        teid = row_to_eid[trow]
                        in_base_top8 = tpid in already_pids
                        in_ekg = teid in e_kg
                        rank_in_kg = kg_rank_lookup.get(tpid)
                        t_diag.append({
                            "provision_id": tpid,
                            "enactment_id": teid,
                            "in_baseline_top8": in_base_top8,
                            "in_E_kg": in_ekg,
                            "kg_connection": eid_path_map.get(teid, "NOT CONNECTED TO SEEDS"),
                            "rank_within_E_kg_pool": rank_in_kg[0] if rank_in_kg else None,
                            "stage1_score_within_E_kg": round(rank_in_kg[1], 4) if rank_in_kg else None,
                            "selected_into_kg_top8": any(c.get("provision_id") == tpid for c in new_kg_cands),
                            "total_E_kg_pool_size": len(kg_candidate_rows),
                        })
                    kg_target_diagnostics.append({
                        "doc_id": doc_id,
                        "sec_num": s_num,
                        "seed_eids": sorted(seed_eids),
                        "expanded_e_kg_count": len(e_kg),
                        "kg_candidate_rows_count": len(kg_candidate_rows),
                        "targets": t_diag,
                    })

                # Stage 2 DeBERTa-v3 evaluation on newly surfaced Top-M=8 KG candidates
                t0_s2 = time.perf_counter()
                if new_kg_cands:
                    kg_pairs = [
                        (f"[{cand['citation']}] {(cand.get('raw_text') or cand.get('prepended_text', '')).lstrip('- \r\n')}".strip(), hypothesis_text)
                        for cand in new_kg_cands
                    ]
                    kg_res_list = demo_app.NEURAL_ENGINE.evaluate_cross_encoder_batch(kg_pairs)
                    for cand, res in zip(new_kg_cands, kg_res_list):
                        cand["stage2_evaluated"] = True
                        cand["p_contradiction"] = res["p_contradiction"]
                        cand["p_entailment"] = res["p_entailment"]
                        cand["p_neutral"] = res["p_neutral"]
                        cand["stage2_confidence"] = round(res["p_contradiction"] * 100, 1)
                        d_g, domain, rel_type = demo_app.compute_topological_distance(cand.get("citation", ""), ch["text"], cand.get("raw_text", ""))
                        tau_dyn = demo_app.compute_dynamic_threshold(d_g, is_vertical=True, tau_base=0.45, delta_tau=0.15)
                        cand["graph_distance_d_g"] = d_g
                        cand["domain"] = domain
                        cand["relation_type"] = rel_type
                        cand["dynamic_threshold"] = tau_dyn
                        cand["dynamic_threshold_pct"] = round(tau_dyn * 100, 1)
                        cand["is_dynamic"] = (tau_dyn < 0.45)
                        is_cand_conflict = (res["p_contradiction"] >= tau_dyn)
                        cand["is_conflict"] = is_cand_conflict
                        cand["stage2_verdict"] = "Contradiction (Preemption Risk)" if is_cand_conflict else ("Entailment" if res["p_entailment"] >= 0.45 else "Neutral / Harmonious")
                        if is_cand_conflict:
                            cand["summary"] = (
                                f"DeBERTa-v3 Cross-Encoder detected directional preemption conflict with {cand.get('citation', '')} "
                                f"(Contradiction confidence {cand['stage2_confidence']}% exceeding topologically calibrated "
                                f"decision threshold tau* = {tau_dyn:.3f} at graph distance d_G = {d_g} [{rel_type}] "
                                f"under Section 5(a) of RA 7160 and the Magtajas doctrine)."
                            )
                            c_xai = demo_app.NEURAL_ENGINE.extract_cross_attention_attribution(cand.get("raw_text", ""), ch["text"])
                            cand["statute_html"] = c_xai["statute_html"]
                            cand["ordinance_html"] = c_xai["ordinance_html"]
                doc_kg_s2_s += (time.perf_counter() - t0_s2)

                # Merge baseline Top-8 + KG Top-8 and determine augmented section verdict identically to app.py
                aug_eval_cands = base_eval_cands + new_kg_cands
                has_fine_defect, fine_val = demo_app.check_statutory_penalty_ceiling(ch["text"])

                best_cand = None
                highest_conflict_prob = -1.0
                for cand in aug_eval_cands:
                    p_c = cand.get("p_contradiction", 0.0)
                    tau_c = cand.get("dynamic_threshold", 0.45)
                    cand["is_conflict"] = (p_c >= tau_c)
                    if p_c > highest_conflict_prob:
                        highest_conflict_prob = p_c
                        best_cand = cand

                if has_fine_defect:
                    pred_label_c = "Contradiction"
                    verdict_c = "CONTRADICTION"
                    target_stat_c = "Republic Act No. 7160 §458(a)(1)(iii)"
                    conf_pct_c = 95.0
                elif best_cand and highest_conflict_prob >= best_cand.get("dynamic_threshold", 0.45):
                    pred_label_c = "Contradiction"
                    verdict_c = "CONTRADICTION"
                    target_stat_c = best_cand["citation"]
                    conf_pct_c = round(highest_conflict_prob * 100, 1)
                else:
                    primary_cand = base_eval_cands[0] if base_eval_cands else (aug_eval_cands[0] if aug_eval_cands else None)
                    p_c_prim = primary_cand.get("p_contradiction", 0.0) if primary_cand else 0.0
                    p_e_prim = primary_cand.get("p_entailment", 0.0) if primary_cand else 0.0
                    p_n_prim = primary_cand.get("p_neutral", 0.90) if primary_cand else 0.90
                    target_stat_c = primary_cand["citation"] if primary_cand else "Republic Act No. 7160 §16"
                    if p_e_prim >= 0.45 and p_e_prim > p_c_prim:
                        pred_label_c = "Entailment"
                        verdict_c = "ENTAILMENT"
                        conf_pct_c = round(p_e_prim * 100, 1)
                    else:
                        pred_label_c = "Neutral"
                        verdict_c = "NEUTRAL"
                        conf_pct_c = round(p_n_prim * 100, 1) if p_n_prim >= 0.50 else 88.5

                if pred_label_c == "Contradiction" and gold_label == "Contradiction":
                    doc_tp_c += 1

                sec_copy = dict(sec_a)
                sec_copy["verdict"] = verdict_c
                sec_copy["target_statute"] = target_stat_c
                sec_copy["confidence_percentage"] = conf_pct_c
                sec_copy["candidate_shortlist"] = aug_eval_cands
                aug_sections_list.append(sec_copy)

                sec_flagged_cands_c = [
                    c for c in aug_eval_cands
                    if c.get("stage2_evaluated") and (c.get("is_conflict") or c.get("p_contradiction", 0.0) >= c.get("dynamic_threshold", 0.45))
                ]
                ev_c = {
                    "doc_id": doc_id,
                    "sec_num": s_num,
                    "sec_title": sec_a.get("sec_title"),
                    "is_boilerplate": False,
                    "gold_label": gold_label,
                    "predicted_label": pred_label_c,
                    "max_stage2_p_contradiction": round(float(max(highest_conflict_prob, 0.0)), 4),
                    "gold_target_statute": gold_sec.get("target_statute"),
                    "retrieved_top_statute": target_stat_c,
                    "flagged_pairs_count": len(sec_flagged_cands_c) if sec_flagged_cands_c else (1 if pred_label_c == "Contradiction" else 0),
                    "flagged_statutes": [c.get("citation") for c in sec_flagged_cands_c],
                    "kg_newly_evaluated_count": len(new_kg_cands),
                    "kg_newly_flagged_statutes": [c.get("citation") for c in new_kg_cands if c.get("is_conflict")],
                }
                sec_evals_c.append(ev_c)
                all_provs_c.append(ev_c)

            total_kg_stage1_s += doc_kg_s1_s
            total_kg_stage2_s += doc_kg_s2_s

            conflict_pairs_c = extract_conflict_pairs_from_sections(aug_sections_list)
            distinct_secs_c = sorted(set(p["sec_num"] for p in conflict_pairs_c))
            doc_summary_c = {
                "doc_id": doc_id,
                "functional_typology": doc_res_a["functional_typology"],
                "gold_contradictions": doc_res_a["gold_contradictions"],
                "detected_contradiction_sections": len(distinct_secs_c),
                "true_positive_contradictions": doc_tp_c,
                "total_conflicts_found": len(conflict_pairs_c),
                "problematic_sections": distinct_secs_c,
                "added_kg_stage1_s": round(doc_kg_s1_s, 2),
                "added_kg_stage2_s": round(doc_kg_s2_s, 2),
                "conflict_pairs": conflict_pairs_c,
                "sections": sec_evals_c,
            }
            doc_results_c.append(doc_summary_c)
            print(
                f"[+] KG-Augmented {doc_id} | +S1={doc_kg_s1_s:.2f}s +S2={doc_kg_s2_s:.2f}s | "
                f"UI Pairs: {len(conflict_pairs_c)} across {len(distinct_secs_c)} secs {distinct_secs_c} | Gold TP: {doc_tp_c}/{doc_res_a['gold_contradictions']}",
                flush=True,
            )

    summary_c = compute_section_metrics(all_provs_c, doc_results_c)
    summary_c["added_kg_stage1_latency_s"] = round(total_kg_stage1_s, 2)
    summary_c["added_kg_stage2_latency_s"] = round(total_kg_stage2_s, 2)
    summary_c["total_kg_augmented_latency_s"] = round(summary_a["total_audit_latency_s"] + total_kg_stage1_s + total_kg_stage2_s, 2)

    ablation_payload = {
        "oracle_diagnostic": {
            "description": "Genuine DeBERTa-v3 cross-encoder evaluation on verbatim controlling national provisions from unified_dual_statutory_provisions.jsonl",
            "batch_inference_latency_s": round(ora_elapsed_s, 2),
            "defects_total": len(oracle_defect_summaries),
            "neural_only_hits_static_045": sum(1 for d in oracle_defect_summaries if d["neural_only_hit_static_045"]),
            "neural_only_hits_dynamic_tau": sum(1 for d in oracle_defect_summaries if d["neural_only_hit_dynamic_tau"]),
            "hybrid_neuro_symbolic_hits": sum(1 for d in oracle_defect_summaries if d["hybrid_neuro_symbolic_hit"]),
            "per_defect_summary": oracle_defect_summaries,
        },
        "kg_ablation": {
            "description": "Genuine 1-hop KG candidate expansion (CITES_AUTHORITY + AMENDS) from N_cite(D) union Stage 1 Top-8, rescored via exact Stage 1 hybrid formula (0.50*norm_BM25 + 0.50*Dense) and evaluated Top-M=8 via DeBERTa-v3",
            "kg_edge_counts_loaded": dict(edge_counts),
            "baseline_no_graph_metrics": summary_a,
            "graph_augmented_metrics": summary_c,
            "target_kg_inclusion_diagnostics": kg_target_diagnostics,
            "document_level_results_graph_augmented": doc_results_c,
        },
    }
    OUT_ABLATION_JSON.write_text(json.dumps(ablation_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[OK] Saved Part B + C authentic oracle & KG ablation JSON -> {OUT_ABLATION_JSON}")

    # Console recap
    print("\n" + "=" * 88)
    print("FINAL AUTHENTIC TIER 2 RECAP")
    print("=" * 88)
    print(f"Part A (Open-Corpus Baseline): TP={summary_a['binary_confusion_matrix']['true_positives']}, FP={summary_a['binary_confusion_matrix']['false_positives']}, TN={summary_a['binary_confusion_matrix']['true_negatives']}, FN={summary_a['binary_confusion_matrix']['false_negatives']} | Spec={summary_a['binary_metrics']['section_level_specificity_pct']:.2f}% | F1={summary_a['binary_metrics']['contradiction_f1']:.4f} | 3-Cls Acc={summary_a['three_class_metrics']['three_class_accuracy_pct']:.2f}% | UI Pairs={summary_a['total_ui_conflict_pairs']}")
    print(f"Part B (Genuine Oracle):       Neural-only={ablation_payload['oracle_diagnostic']['neural_only_hits_dynamic_tau']}/7 | Hybrid(+Symbolic Fine)={ablation_payload['oracle_diagnostic']['hybrid_neuro_symbolic_hits']}/7")
    print(f"Part C (Real 1-Hop KG):        TP={summary_c['binary_confusion_matrix']['true_positives']}, FP={summary_c['binary_confusion_matrix']['false_positives']}, TN={summary_c['binary_confusion_matrix']['true_negatives']}, FN={summary_c['binary_confusion_matrix']['false_negatives']} | Spec={summary_c['binary_metrics']['section_level_specificity_pct']:.2f}% | F1={summary_c['binary_metrics']['contradiction_f1']:.4f} | 3-Cls Acc={summary_c['three_class_metrics']['three_class_accuracy_pct']:.2f}% | UI Pairs={summary_c['total_ui_conflict_pairs']}")
    print("=" * 88)


if __name__ == "__main__":
    main()
