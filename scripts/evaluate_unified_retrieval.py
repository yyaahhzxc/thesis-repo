"""
evaluate_unified_retrieval.py
=============================
Evaluates the Unified Dual-Stream Retrieval Engine across:
1. The 350 Ground Truth Statutory Conflict benchmark pairs (Vertical Preemption Recall).
2. The 8 Authentic Davao City Jurisprudential Cases (Tier 3 Judicial Validation Suite).
3. Sample Municipal Draft Queries (Horizontal Coherence & Local Consistency).

Measures:
- Vertical Recall@5, Recall@10, Recall@20, Recall@50
- Mean Reciprocal Rank (MRR)
- Dual-Stream Search Latency (ms/query on LGU testbed CPU)
- Export to output/dual_retrieval_benchmark_results.json
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.dual_retrieval import DualStreamRetrievalEngine

# Canonical mapping from Ground Truth statute titles to national enactment IDs
TITLE_TO_LAW_ID = {
    'Republic Act No. 10121 (Philippine Disaster Risk Reduction and Management Act of 2010)': 'ra_10121_2010',
    'Republic Act No. 10591 (Comprehensive Firearms and Ammunition Regulation Act)': 'ra_10591_2013',
    'Republic Act No. 10931 (Universal Access to Quality Tertiary Education Act)': 'ra_10931_2017',
    'Republic Act No. 11032 (Ease of Doing Business and Efficient Government Service Delivery Act of 2018)': 'ra_11032_2018',
    'Republic Act No. 11223 (Universal Health Care Act)': 'ra_11223_2019',
    'Republic Act No. 11314 (Student Fare Discount Act)': 'ra_11314_2019',
    'Republic Act No. 11332 (Mandatory Reporting of Notifiable Diseases and Health Events of Public Health Concern Act)': 'ra_11332_2019',
    'Republic Act No. 4136 (Land Transportation and Traffic Code)': 'ra_4136_1964',
    'Republic Act No. 7160 (The Local Government Code of 1991)': 'ra_7160_1991',
    'Republic Act No. 7581 (The Price Act)': 'ra_7581_1992',
    'Republic Act No. 7925 (Public Telecommunications Policy Act of 1995)': 'ra_7925_1995',
    'Republic Act No. 7942 (Philippine Mining Act of 1995)': 'ra_7942_1995',
    'Republic Act No. 8550 (The Philippine Fisheries Code of 1998)': 'ra_8550_1998',
    'Republic Act No. 9136 (Electric Power Industry Reform Act of 2001)': 'ra_9136_2001',
    'Republic Act No. 9165 (Comprehensive Dangerous Drugs Act of 2002)': 'ra_9165_2002',
    'Republic Act No. 9211 (Tobacco Regulation Act of 2003)': 'ra_9211_2003',
    'Republic Act No. 9344 (Juvenile Justice and Welfare Act of 2006)': 'ra_9344_2006',
}

GT_FILE = Path("data/ground_truth_350.jsonl")
TIER3_FILE = Path("data/tier3_jurisprudential_cases.jsonl")
BENCHMARK_OUTPUT = Path("output/dual_retrieval_benchmark_results.json")


def evaluate_engine():
    print("=" * 80)
    print("STAGE 1 RETRIEVAL EVALUATION OVER UNIFIED 176,421-PROVISION CORPUS")
    print("=" * 80)

    # Initialize Engine (BM25 + Dense if available)
    engine = DualStreamRetrievalEngine(load_dense=True)

    cache_file = Path("output/gt350_retrieval_cache.json")
    if cache_file.exists():
        print(f"\n[1/3] Loading cached 350 Ground Truth benchmark results from {cache_file}...")
        with open(cache_file, 'r', encoding='utf-8') as cf:
            cached = json.load(cf)
            overall_metrics = cached['overall_metrics']
            tier_metrics = cached['tier_metrics']
    else:
        print(f"\n[1/3] Benchmarking Vertical Retrieval on 350 Ground Truth Queries ({GT_FILE})...")
        gt_pairs = []
        with open(GT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    gt_pairs.append(json.loads(line))

        ranks = []
        tier_ranks = {"Tier 1": [], "Tier 2": [], "Tier 3": []}
        latencies = []

        for item in gt_pairs:
            query = item['ordinance_hypothesis']['hypothesis_text']
            statute_title = item['national_premise']['statute_title']
            gold_id = TITLE_TO_LAW_ID.get(statute_title, '')
            tier = item.get('difficulty_tier', 'Tier 1')
            tier_key = "Tier 1" if "Tier 1" in tier else ("Tier 2" if "Tier 2" in tier else "Tier 3")

            t0 = time.time()
            res = engine.retrieve(query, k_vertical=50, k_horizontal=5, operative_only=True)
            t1 = time.time()
            latencies.append((t1 - t0) * 1000)

            # Check rank of gold national statute among vertical candidates
            gold_rank = None
            for cand in res['vertical_national_candidates']:
                cand_enact = cand.get('enactment_id', '')
                cand_prov = cand.get('provision_id', '')
                if cand_enact == gold_id or (gold_id and gold_id in cand_prov):
                    gold_rank = cand['rank']
                    break

            ranks.append(gold_rank)
            tier_ranks[tier_key].append(gold_rank)

        # Calculate metrics
        def calc_metrics(rk_list):
            valid = [r for r in rk_list if r is not None]
            n = len(rk_list)
            return {
                "n_queries": n,
                "recall@5": round(sum(1 for r in valid if r <= 5) / n, 4),
                "recall@10": round(sum(1 for r in valid if r <= 10) / n, 4),
                "recall@20": round(sum(1 for r in valid if r <= 20) / n, 4),
                "recall@50": round(sum(1 for r in valid if r <= 50) / n, 4),
                "mrr": round(float(np.mean([1.0 / r for r in valid] + [0.0] * (n - len(valid)))), 4)
            }

        overall_metrics = calc_metrics(ranks)
        overall_metrics["mean_latency_ms"] = round(float(np.mean(latencies)), 2)
        overall_metrics["p95_latency_ms"] = round(float(np.percentile(latencies, 95)), 2)
        tier_metrics = {k: calc_metrics(v) for k, v in tier_ranks.items()}

    print("\n--- 350 Ground Truth Retrieval Benchmark Results ---")
    print(f"Overall Recall@5:  {overall_metrics['recall@5']*100:.2f}%")
    print(f"Overall Recall@10: {overall_metrics['recall@10']*100:.2f}%")
    print(f"Overall Recall@20: {overall_metrics['recall@20']*100:.2f}%")
    print(f"Overall Recall@50: {overall_metrics['recall@50']*100:.2f}%")
    print(f"Overall MRR:       {overall_metrics['mrr']:.4f}")
    print(f"Mean Latency:      {overall_metrics['mean_latency_ms']:.2f} ms/query")

    print("\nBreakdown by Difficulty Tier:")
    for tk, tv in tier_metrics.items():
        print(f"  {tk:8s} (N={tv['n_queries']}): R@5={tv['recall@5']*100:.1f}%, R@20={tv['recall@20']*100:.1f}%, MRR={tv['mrr']:.4f}")

    # 2. Evaluate on Tier 3 Davao City Cases
    print(f"\n[2/3] Evaluating on Tier 3 Authentic Davao City Jurisprudential Cases ({TIER3_FILE})...")
    tier3_results = []
    if TIER3_FILE.exists():
        with open(TIER3_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    case = json.loads(line)
                    op_secs = case.get('operative_sections', {})
                    operative_text = " ".join([v for k, v in op_secs.items() if not any(b in k.upper() for b in ['TITLE', 'EFFECTIVITY', 'REPEALING', 'SEPARABILITY'])])
                    q = f"{case.get('title', '')} {operative_text}".strip()
                    if not q:
                        q = case.get('title', '')
                    res = engine.retrieve(q, k_vertical=5, k_horizontal=5)
                    case_name = case.get('judicial_reference') or case.get('case_id', '')
                    tier3_results.append({
                        "case_id": case.get('case_id', ''),
                        "case_name": case_name,
                        "ordinance_no": case.get('ordinance_no', ''),
                        "top_national_match": res['vertical_national_candidates'][0]['enactment_number'] if res['vertical_national_candidates'] else "None",
                        "top_municipal_match": res['horizontal_municipal_candidates'][0]['enactment_number'] if res['horizontal_municipal_candidates'] else "None",
                        "search_latency_ms": res['metrics']['total_latency_ms']
                    })
        for t3 in tier3_results[:4]:
            print(f"  Case: {t3['case_name'][:45]} -> Top Nat: {t3['top_national_match']} | Top Muni: {t3['top_municipal_match']} ({t3['search_latency_ms']} ms)")

    # 3. Export benchmark results
    out_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "corpus_provisions_total": len(engine.provisions),
        "national_provisions": len(engine.national_indices),
        "municipal_provisions": len(engine.municipal_indices),
        "overall_ground_truth_metrics": overall_metrics,
        "difficulty_tier_breakdown": tier_metrics,
        "tier3_case_evaluations": tier3_results
    }

    with open(BENCHMARK_OUTPUT, 'w', encoding='utf-8') as out_f:
        json.dump(out_data, out_f, indent=2)
    print(f"\n[Export] Full benchmark evaluation saved to {BENCHMARK_OUTPUT}")
    print("=" * 80)


if __name__ == "__main__":
    evaluate_engine()
