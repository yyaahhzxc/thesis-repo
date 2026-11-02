"""
evaluate_tier2_system_tester.py
===============================
Unbiased, Blind System-Level End-to-End Evaluation on the 6 Typology-Stratified
Full-Document Draft Ordinances (Tier 2).

Methodological Principles Implemented:
1. Full Document PDF Ingestion (Chapter 3 §3.8): Ingests the 6 authentic Philippine Folio
   (8.5 x 13 in) PDFs (`DRAFT-ORD-2026-01.pdf` to `06.pdf`) via `pypdf`, spanning all 6
   functional legislative typologies discovered in Table 4.4.
2. Blind Neural Execution (`execute_full_ordinance_audit` from `demo/app.py`):
   - Passes ONLY raw extracted PDF text and filename to the engine (zero ground-truth hints).
   - Performs automated preamble/attendance stripping and section boundary chunking.
   - Executes genuine Stage 1 Hybrid Retrieval (BM25 + all-MiniLM-L6-v2 dense embeddings)
     over the 176,421-provision dual statutory corpus.
   - Executes genuine Stage 2 DeBERTa-v3 Cross-Encoder NLI evaluation on top retrieved
     national statutory candidates using calibrated threshold tau* = 0.45, plus the single
     RA 7160 §458 integer penalty ceiling rule.
3. Comprehensive Multi-Tier Metrics:
   - Provision-Level: Accuracy, Contradiction Precision, Contradiction Recall (Sensitivity),
     Contradiction F1, Cost-Sensitive F2-Score (beta=2.0), Section Specificity (Eq. 3.20), Macro-F1.
   - Document-Level Triage: Recall of defective drafts requiring legislative committee review.
   - System Latency: Real measured ingestion, retrieval, and neural cross-encoder latency.
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple
import pypdf

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "demo"))

from demo.app import NEURAL_ENGINE, execute_full_ordinance_audit

BENCHMARK_PATH = REPO_ROOT / "data" / "tier2_draft_ordinances_benchmark.jsonl"
PDF_DIR = REPO_ROOT / "data" / "tier2_draft_ordinances_pdf"
OUTPUT_DIR = REPO_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_JSON_PATH = OUTPUT_DIR / "tier2_system_level_test_results.json"


def load_tier2_benchmark() -> List[Dict[str, Any]]:
    if not BENCHMARK_PATH.exists():
        raise FileNotFoundError(f"Tier 2 benchmark file not found at {BENCHMARK_PATH}")
    docs = []
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                docs.append(json.loads(line.strip()))
    return docs


def extract_text_from_pdf(pdf_path: Path) -> Tuple[str, int, float]:
    t0 = time.perf_counter()
    reader = pypdf.PdfReader(str(pdf_path))
    pages_text = [page.extract_text() or "" for page in reader.pages]
    full_text = "\n\n".join(pages_text)
    latency_ms = (time.perf_counter() - t0) * 1000.0
    return full_text, len(reader.pages), latency_ms


def normalize_verdict(v: str) -> str:
    v_up = (v or "").upper()
    if "CONTRADICTION" in v_up:
        return "Contradiction"
    elif "ENTAILMENT" in v_up:
        return "Entailment"
    return "Neutral"


def run_tier2_system_evaluation() -> Dict[str, Any]:
    print("=" * 88)
    print("TIER 2 SYSTEM-LEVEL TESTER: BLIND FULL-DOCUMENT EX-ANTE CONFLICT DETECTION (N = 6)")
    print("=" * 88)
    print(f"[*] Neural Engine Loaded: {NEURAL_ENGINE.is_loaded}")
    print(f"[*] Benchmark Ground Truth: {BENCHMARK_PATH.name}")
    print(f"[*] Authentic PDF Directory: {PDF_DIR.name}")
    print(f"[*] Calibrated Decision Threshold: tau* = 0.45 (Cost Ratio C(FN)/C(FP) = 5.0)")
    print("-" * 88)

    if not NEURAL_ENGINE.is_loaded:
        raise RuntimeError("LocalNeuralEngine failed to load! Refusing to run non-neural fallback.")

    benchmark_docs = load_tier2_benchmark()
    benchmark_map = {d["doc_id"]: d for d in benchmark_docs}

    pdf_files = sorted(list(PDF_DIR.glob("*.pdf")))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {PDF_DIR}")

    print(f"[*] Ingesting and auditing {len(pdf_files)} typology-stratified Folio PDFs...\n")

    doc_results = []
    all_provisions = []
    total_ingestion_time_ms = 0.0
    total_audit_time_ms = 0.0

    for pdf_file in pdf_files:
        doc_id = pdf_file.stem
        gold_doc = benchmark_map.get(doc_id)
        if not gold_doc:
            print(f"[!] Warning: No ground truth metadata found for {doc_id}")
            continue

        # 1. Ingestion via pypdf
        raw_text, page_count, ing_time = extract_text_from_pdf(pdf_file)
        total_ingestion_time_ms += ing_time
        total_pdf_words = len(raw_text.split())

        # 2. Blind End-to-End Neural Audit (pass doc_id=None so zero ground-truth lookup occurs)
        t_audit_start = time.perf_counter()
        audit_res = execute_full_ordinance_audit(
            raw_text=raw_text,
            filename=pdf_file.name,
            doc_id=None
        )
        audit_time_ms = (time.perf_counter() - t_audit_start) * 1000.0
        total_audit_time_ms += audit_time_ms

        audited_sections = audit_res.get("sections", [])
        gold_sections = {s["sec_num"]: s for s in gold_doc.get("sections", [])}

        doc_contradictions_detected = 0
        doc_gold_contradictions = sum(1 for s in gold_doc.get("sections", []) if s["label"] == "Contradiction")
        doc_tp_contradictions = 0
        section_evals = []

        for sec in audited_sections:
            s_num = sec["sec_num"]
            s_title = sec["sec_title"]
            s_text = sec["text"]

            gold_sec = gold_sections.get(s_num, {})
            gold_label = gold_sec.get("label", "Neutral")
            gold_statute = gold_sec.get("target_statute")

            pred_label = normalize_verdict(sec.get("verdict", "NEUTRAL"))
            conflict_prob = float(sec.get("conflict_probability", 0.0))
            retrieved_statute = sec.get("target_statute", "")
            rationale = sec.get("legal_rationale", "")

            is_correct = (pred_label == gold_label)
            if pred_label == "Contradiction":
                doc_contradictions_detected += 1
                if gold_label == "Contradiction":
                    doc_tp_contradictions += 1

            sec_eval = {
                "doc_id": doc_id,
                "sec_num": s_num,
                "sec_title": s_title,
                "word_count": len(s_text.split()),
                "text_snippet": s_text[:90] + ("..." if len(s_text) > 90 else ""),
                "gold_label": gold_label,
                "predicted_label": pred_label,
                "conflict_probability": round(conflict_prob, 4),
                "gold_target_statute": gold_statute,
                "retrieved_top_statute": retrieved_statute,
                "is_correct": is_correct,
                "is_boilerplate": sec.get("is_boilerplate", False),
                "rationale": rationale
            }
            section_evals.append(sec_eval)
            all_provisions.append(sec_eval)

        doc_is_flagged = (doc_contradictions_detected > 0)
        doc_should_flag = (doc_gold_contradictions > 0)
        triage_success = (doc_is_flagged == doc_should_flag)

        operative_words = sum(len(s.get("text", "").split()) for s in gold_doc.get("sections", []))

        doc_summary = {
            "doc_id": doc_id,
            "typology_id": gold_doc.get("typology_id"),
            "functional_typology": gold_doc.get("functional_typology", ""),
            "statutory_authority": gold_doc.get("statutory_authority", ""),
            "proposed_ordinance_no": gold_doc.get("proposed_ordinance_no", ""),
            "title": gold_doc.get("title", ""),
            "pages": page_count,
            "total_document_words": total_pdf_words,
            "operative_section_words": operative_words,
            "provisions_count": len(audited_sections),
            "gold_contradictions": doc_gold_contradictions,
            "detected_contradictions": doc_contradictions_detected,
            "true_positive_contradictions": doc_tp_contradictions,
            "triage_flagged": doc_is_flagged,
            "triage_success": triage_success,
            "ingestion_latency_ms": round(ing_time, 2),
            "neural_audit_latency_ms": round(audit_time_ms, 2),
            "sections": section_evals
        }
        doc_results.append(doc_summary)

        status_tag = "[FLAGGED - RISK DETECTED]" if doc_is_flagged else "[PASS - NO CONFLICT]"
        print(
            f"[*] {doc_id} ({gold_doc.get('functional_typology', '')[:26]:<26}) | "
            f"{page_count} pgs | {total_pdf_words:>4} wds | {len(audited_sections):>2} secs | "
            f"Gold C: {doc_gold_contradictions} | Pred C: {doc_contradictions_detected} (TP={doc_tp_contradictions}) | {status_tag}"
        )

    # =========================================================================
    # METRICS CALCULATION
    # =========================================================================
    total_provs = len(all_provisions)
    correct_provs = sum(1 for p in all_provisions if p["is_correct"])
    prov_accuracy = (correct_provs / total_provs) * 100.0 if total_provs > 0 else 0.0

    # Binary Contradiction Detection Metrics (Positive Class = Contradiction)
    tp_c = sum(1 for p in all_provisions if p["gold_label"] == "Contradiction" and p["predicted_label"] == "Contradiction")
    fp_c = sum(1 for p in all_provisions if p["gold_label"] != "Contradiction" and p["predicted_label"] == "Contradiction")
    fn_c = sum(1 for p in all_provisions if p["gold_label"] == "Contradiction" and p["predicted_label"] != "Contradiction")
    tn_c = sum(1 for p in all_provisions if p["gold_label"] != "Contradiction" and p["predicted_label"] != "Contradiction")

    prec_c = (tp_c / (tp_c + fp_c)) if (tp_c + fp_c) > 0 else 0.0
    rec_c = (tp_c / (tp_c + fn_c)) if (tp_c + fn_c) > 0 else 0.0
    f1_c = (2 * prec_c * rec_c / (prec_c + rec_c)) if (prec_c + rec_c) > 0 else 0.0
    f2_c = (5 * prec_c * rec_c / (4 * prec_c + rec_c)) if (4 * prec_c + rec_c) > 0 else 0.0
    sec_specificity = (tn_c / (tn_c + fp_c)) * 100.0 if (tn_c + fp_c) > 0 else 0.0

    classes = ["Neutral", "Entailment", "Contradiction"]
    class_stats = {}
    f1_list = []
    for cls in classes:
        tp = sum(1 for p in all_provisions if p["gold_label"] == cls and p["predicted_label"] == cls)
        fp = sum(1 for p in all_provisions if p["gold_label"] != cls and p["predicted_label"] == cls)
        fn = sum(1 for p in all_provisions if p["gold_label"] == cls and p["predicted_label"] != cls)
        p_cls = (tp / (tp + fp)) if (tp + fp) > 0 else 0.0
        r_cls = (tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        f_cls = (2 * p_cls * r_cls / (p_cls + r_cls)) if (p_cls + r_cls) > 0 else 0.0
        f1_list.append(f_cls)
        class_stats[cls] = {
            "support": sum(1 for p in all_provisions if p["gold_label"] == cls),
            "precision": round(p_cls, 4),
            "recall": round(r_cls, 4),
            "f1": round(f_cls, 4)
        }
    macro_f1 = sum(f1_list) / len(f1_list)

    total_docs = len(doc_results)
    flagged_docs = sum(1 for d in doc_results if d["triage_flagged"])
    doc_triage_recall = (flagged_docs / total_docs) * 100.0 if total_docs > 0 else 0.0

    avg_ingestion_ms = total_ingestion_time_ms / total_docs if total_docs > 0 else 0.0
    avg_audit_ms = total_audit_time_ms / total_docs if total_docs > 0 else 0.0
    avg_infer_per_prov_ms = total_audit_time_ms / total_provs if total_provs > 0 else 0.0

    results_payload = {
        "benchmark_tier": "Tier 2: System-Level Full Document Stress Test (6 Typologies)",
        "description": "Blind end-to-end evaluation on 6 typology-stratified multi-section draft ordinances (52 provisions) in authentic PDF format.",
        "documents_evaluated": total_docs,
        "provisions_evaluated": total_provs,
        "calibrated_decision_threshold_tau": 0.45,
        "cost_penalty_ratio": 5.0,
        "summary_metrics": {
            "provision_accuracy": round(prov_accuracy, 2),
            "contradiction_precision": round(prec_c, 4),
            "contradiction_recall": round(rec_c, 4),
            "contradiction_f1": round(f1_c, 4),
            "cost_sensitive_f2": round(f2_c, 4),
            "section_level_specificity": round(sec_specificity, 2),
            "macro_f1": round(macro_f1, 4),
            "document_triage_recall": round(doc_triage_recall, 2)
        },
        "per_class_performance": class_stats,
        "confusion_matrix_contradiction": {
            "true_positives": tp_c,
            "false_positives": fp_c,
            "true_negatives": tn_c,
            "false_negatives": fn_c
        },
        "system_latency": {
            "avg_pdf_ingestion_ms_per_doc": round(avg_ingestion_ms, 2),
            "avg_inference_ms_per_provision": round(avg_infer_per_prov_ms, 2),
            "avg_total_audit_ms_per_full_ordinance": round(avg_ingestion_ms + avg_audit_ms, 2)
        },
        "document_level_results": doc_results
    }

    with open(RESULTS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(results_payload, f, indent=2)

    print("\n" + "=" * 88)
    print("TIER 2 BLIND SYSTEM-LEVEL EVALUATION SUMMARY")
    print("=" * 88)
    print(f"Total Documents Audited:         {total_docs} (1 per Table 4.4 Functional Typology)")
    print(f"Total Provisions Evaluated:      {total_provs}")
    print(f"Document-Level Triage Recall:    {doc_triage_recall:.2f}% ({flagged_docs}/{total_docs})")
    print(f"Contradiction Confusion Matrix:  TP={tp_c}, FP={fp_c}, TN={tn_c}, FN={fn_c}")
    print(f"Contradiction Recall (Sens.):    {rec_c*100:.2f}% ({tp_c}/{tp_c+fn_c})")
    print(f"Contradiction Precision:         {prec_c*100:.2f}% ({tp_c}/{tp_c+fp_c})")
    print(f"Contradiction F1 / F2 Score:     F1={f1_c:.4f} | F2={f2_c:.4f}")
    print(f"Section-Level Specificity:       {sec_specificity:.2f}% ({tn_c}/{tn_c+fp_c})")
    print(f"Overall 3-Class Accuracy:        {prov_accuracy:.2f}% ({correct_provs}/{total_provs})")
    print(f"Macro-F1 Score:                  {macro_f1:.4f}")
    print(f"Mean Full-Document Audit Time:   {(avg_ingestion_ms + avg_audit_ms):.1f} ms / document")
    print("=" * 88)

    return results_payload


if __name__ == "__main__":
    run_tier2_system_evaluation()
