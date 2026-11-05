"""
experiment_stage1_proposals.py
==============================
Empirical evaluation comparing Stage 1 Information Retrieval configurations:
1. Baseline Sparse BM25 (AIIR Lab Baseline)
2. BM25 + Strict Hard Domain Filter (The Flawed Baseline)
3. BM25 + Soft Domain Prior Boosting (Gentle Scaling)
4. Pure Dense Bi-Encoder (SentenceTransformer all-MiniLM-L6-v2)
5. Hybrid JNLP Weighted Sum (alpha = 0.5)
6. Hybrid Dense-Biased (alpha = 0.7)
7. Reciprocal Rank Fusion (RRF k = 60)

Evaluates on the 350 Ground Truth queries from Davao City ordinances against 
verified statutory section provisions, measuring:
- Recall@1, Recall@3, Recall@5, Recall@10, Recall@20
- MRR (Mean Reciprocal Rank)
- Stratified breakdowns across Difficulty Tiers (Tier 1, Tier 2, Tier 3)
- Query Latency (ms)
"""

import os
import sys
import re
import json
import time
from typing import List, Dict, Any, Tuple
import numpy as np

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

# Mapping from Ground Truth statute title + citation to premise key in corpus_statute_premises.json
def resolve_premise_key(statute_title: str, citation: str) -> str:
    title_lower = statute_title.lower()
    cit_lower = citation.lower()
    
    if "7581" in title_lower and "6" in cit_lower:
        return "RA_7581_Sec_6"
    elif "10121" in title_lower:
        if "12" in cit_lower:
            return "RA_10121_Sec_12"
        elif "21" in cit_lower:
            return "RA_10121_Sec_21"
    elif "11032" in title_lower and "9" in cit_lower:
        return "RA_11032_Sec_9"
    elif "10931" in title_lower and "4" in cit_lower:
        return "RA_10931_Sec_4"
    elif "9165" in title_lower and "36" in cit_lower:
        return "RA_9165_Sec_36c"
    elif "11314" in title_lower and "5" in cit_lower:
        return "RA_11314_Sec_5"
    elif "7160" in title_lower:
        if "458" in cit_lower:
            return "RA_7160_Sec_458"
        elif "152" in cit_lower:
            return "RA_7160_Sec_152c"
        elif "287" in cit_lower:
            return "RA_7160_Sec_287"
        elif "233" in cit_lower:
            return "RA_7160_Sec_233"
        elif "140" in cit_lower:
            return "RA_7160_Sec_140"
    elif "9344" in title_lower and "6" in cit_lower:
        return "RA_9344_Sec_6"
    elif "4136" in title_lower and "35" in cit_lower:
        return "RA_4136_Sec_35"
    elif "7925" in title_lower and "4" in cit_lower:
        return "RA_7925_Sec_4"
    elif "9136" in title_lower and "43" in cit_lower:
        return "RA_9136_Sec_43u"
    elif "11223" in title_lower and "6" in cit_lower:
        return "RA_11223_Sec_6"
    elif "11332" in title_lower and "9" in cit_lower:
        return "RA_11332_Sec_9"
    elif "9211" in title_lower and "5" in cit_lower:
        return "RA_9211_Sec_5"
    elif "7942" in title_lower and "70" in cit_lower:
        return "RA_7942_Sec_70"
    elif "8550" in title_lower and "18" in cit_lower:
        return "RA_8550_Sec_18"
    elif "10591" in title_lower and "31" in cit_lower:
        return "RA_10591_Sec_31"
        
    return ""


# Premise to Macro Domain Mapping
PREMISE_DOMAINS = {
    "RA_7581_Sec_6": [0],         # Executive / Price Control
    "RA_10121_Sec_12": [0, 6],    # DRRM Office / Calamity Fund
    "RA_11032_Sec_9": [0],        # Ease of Doing Business
    "RA_10931_Sec_4": [1],        # Free Higher Education
    "RA_9165_Sec_36c": [1],       # Mandatory Drug Testing in Schools
    "RA_11314_Sec_5": [1],        # Student Fare Discount
    "RA_7160_Sec_458": [2],       # City Council Penal Limits
    "RA_9344_Sec_6": [2],         # Minimum Age of Criminal Responsibility
    "RA_7160_Sec_152c": [2, 7],   # Barangay Clearance
    "RA_4136_Sec_35": [3],        # Speed Limits
    "RA_7925_Sec_4": [3],         # Telecom Policy
    "RA_9136_Sec_43u": [3],       # Electric Power Industry
    "RA_11223_Sec_6": [4],        # Universal Health Care
    "RA_11332_Sec_9": [4],        # Notifiable Diseases
    "RA_9211_Sec_5": [4],         # Tobacco Regulation
    "RA_10591_Sec_31": [5],       # Firearms Carrying
    "RA_7942_Sec_70": [5],        # Mining Environmental Clearance
    "RA_8550_Sec_18": [5],        # Fisheries Code
    "RA_10121_Sec_21": [0, 6],    # Calamity Fund
    "RA_7160_Sec_287": [2, 6],    # Development Projects (IRA Fund)
    "RA_7160_Sec_233": [2, 7],    # Real Property Tax Rate
    "RA_7160_Sec_140": [2, 7],    # Amusement Tax
}


def tokenize(text: str) -> List[str]:
    return re.findall(r'[a-zA-Z0-9]+', text.lower())


def main():
    print("=" * 80)
    print("STAGE 1 CANDIDATE RETRIEVAL EXPERIMENT: BASELINE vs. PROPOSED EXTENSIONS")
    print("=" * 80)
    
    # 1. Load Ground Truth
    gt_path = os.path.join("data", "ground_truth_350.jsonl")
    with open(gt_path, 'r', encoding='utf-8') as f:
        gt_records = [json.loads(line) for line in f if line.strip()]
    print(f"[*] Loaded {len(gt_records)} Ground Truth query records.")
    
    # 2. Load Statutory Premises
    prem_path = os.path.join("data", "corpus_statute_premises.json")
    with open(prem_path, 'r', encoding='utf-8') as f:
        premises_dict = json.load(f)
    print(f"[*] Loaded {len(premises_dict)} verified statutory provisions.")
    
    premise_ids = list(premises_dict.keys())
    id_to_idx = {pid: i for i, pid in enumerate(premise_ids)}
    
    # Build passages with hierarchical headers (Section 3.2.3.2)
    # x_chunk = [Statute Title, Section S_i: Catchline] || t_verbatim
    passages = []
    for pid in premise_ids:
        p = premises_dict[pid]
        passage_str = f"{p['statute']} {p['citation']}: {p['text']}"
        passages.append(passage_str)
        
    print(f"[*] Built {len(passages)} hierarchical statutory passage representations.")
    
    # 3. Build BM25 Index
    print("[*] Building BM25 index on statutory provisions...")
    tokenized_passages = [tokenize(p) for p in passages]
    bm25 = BM25Okapi(tokenized_passages)
    
    # 4. Dense Bi-Encoder Embeddings
    print("[*] Loading SentenceTransformer (sentence-transformers/all-MiniLM-L6-v2)...")
    dense_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    
    print("[*] Encoding statutory passage embeddings (offline pre-computation)...")
    passage_embeddings = dense_model.encode(passages, normalize_embeddings=True, show_progress_bar=False)
    
    print("[*] Pre-encoding 350 query hypotheses...")
    queries = [r['ordinance_hypothesis']['hypothesis_text'] for r in gt_records]
    query_embeddings = dense_model.encode(queries, normalize_embeddings=True, show_progress_bar=False)
    
    # Pre-resolve target premise indices
    target_indices = []
    unresolved = 0
    for r in gt_records:
        title = r['national_premise']['statute_title']
        cit = r['national_premise']['citation']
        k = resolve_premise_key(title, cit)
        if k in id_to_idx:
            target_indices.append(id_to_idx[k])
        else:
            unresolved += 1
            target_indices.append(-1)
            
    print(f"[*] Resolved {len(target_indices) - unresolved}/{len(gt_records)} target provision references.")
    
    # Define Configurations
    configurations = [
        {"name": "1. Pure BM25 (AIIR Lab Baseline)", "type": "bm25", "domain_mode": "none"},
        {"name": "2. BM25 + Hard Domain Filter", "type": "bm25", "domain_mode": "hard"},
        {"name": "3. BM25 + Soft Domain Prior (+20% boost)", "type": "bm25", "domain_mode": "soft"},
        {"name": "4. Pure Dense Bi-Encoder (MiniLM)", "type": "dense", "domain_mode": "none"},
        {"name": "5. Hybrid JNLP (Weighted Sum α=0.5)", "type": "hybrid", "alpha": 0.5, "domain_mode": "none"},
        {"name": "6. Hybrid Dense-Biased (α=0.7)", "type": "hybrid", "alpha": 0.7, "domain_mode": "none"},
        {"name": "7. Hybrid BM25-Biased (α=0.3)", "type": "hybrid", "alpha": 0.3, "domain_mode": "none"},
        {"name": "8. Reciprocal Rank Fusion (RRF k=60)", "type": "rrf", "domain_mode": "none"},
        {"name": "9. Hybrid + Soft Domain Prior (α=0.5)", "type": "hybrid", "alpha": 0.5, "domain_mode": "soft"}
    ]
    
    all_results = []
    k_vals = [1, 3, 5, 10, 20]
    
    for cfg in configurations:
        cfg_name = cfg["name"]
        cfg_type = cfg["type"]
        domain_mode = cfg["domain_mode"]
        alpha = cfg.get("alpha", 0.5)
        
        latencies = []
        tier_ranks = {
            "Overall": [],
            "Tier 1: Surface & Quantitative": [],
            "Tier 2: Preemption & Carve-Outs": [],
            "Tier 3: Latent & Paraphrastic": []
        }
        
        for q_idx, r in enumerate(gt_records):
            target_idx = target_indices[q_idx]
            if target_idx == -1:
                continue
                
            query = queries[q_idx]
            tier = r.get("difficulty_tier", "Unknown")
            query_domain = r.get("macro_domain_id")
            
            t_start = time.perf_counter()
            
            # 1. Compute BM25 raw scores
            q_tokens = tokenize(query)
            bm25_raw = np.array(bm25.get_scores(q_tokens), dtype=np.float32)
            
            # 2. Compute Dense cosine scores
            q_emb = query_embeddings[q_idx]
            dense_raw = np.dot(passage_embeddings, q_emb)  # Normalized embeddings -> dot product = cosine
            
            # Combine scores according to cfg_type
            if cfg_type == "bm25":
                final_scores = bm25_raw.copy()
            elif cfg_type == "dense":
                final_scores = dense_raw.copy()
            elif cfg_type == "hybrid":
                # Min-max normalization for BM25
                b_min, b_max = bm25_raw.min(), bm25_raw.max()
                bm25_norm = (bm25_raw - b_min) / (b_max - b_min) if b_max > b_min else bm25_raw
                # Cosine [-1, 1] to [0, 1]
                dense_norm = (dense_raw + 1.0) / 2.0
                final_scores = alpha * dense_norm + (1.0 - alpha) * bm25_norm
            elif cfg_type == "rrf":
                # Rank-based Reciprocal Rank Fusion
                bm25_order = np.argsort(bm25_raw)[::-1]
                dense_order = np.argsort(dense_raw)[::-1]
                
                bm25_ranks = np.empty_like(bm25_order)
                bm25_ranks[bm25_order] = np.arange(1, len(passages) + 1)
                
                dense_ranks = np.empty_like(dense_order)
                dense_ranks[dense_order] = np.arange(1, len(passages) + 1)
                
                final_scores = (1.0 / (60.0 + bm25_ranks)) + (1.0 / (60.0 + dense_ranks))
                
            # Domain Modulation
            if domain_mode == "hard":
                # Hard Filter: zero out or slash scores where premise domain doesn't match query domain
                for p_idx, pid in enumerate(premise_ids):
                    p_domains = PREMISE_DOMAINS.get(pid, [])
                    if query_domain not in p_domains:
                        final_scores[p_idx] *= 0.10  # Harsh penalty
            elif domain_mode == "soft":
                # Soft Prior: mild boost (+20%) for premises in matching domain
                for p_idx, pid in enumerate(premise_ids):
                    p_domains = PREMISE_DOMAINS.get(pid, [])
                    if query_domain in p_domains:
                        final_scores[p_idx] *= 1.20  # Mild boost
                        
            # Determine Rank
            target_score = final_scores[target_idx]
            rank = int(np.sum(final_scores > target_score)) + 1
            
            t_end = time.perf_counter()
            latencies.append((t_end - t_start) * 1000.0)
            
            tier_ranks["Overall"].append(rank)
            if tier in tier_ranks:
                tier_ranks[tier].append(rank)
                
        # Metrics computation
        res = {
            "Configuration": cfg_name,
            "Latency_ms": round(float(np.mean(latencies)), 2)
        }
        
        for group in ["Overall", "Tier 1: Surface & Quantitative", "Tier 2: Preemption & Carve-Outs", "Tier 3: Latent & Paraphrastic"]:
            ranks = tier_ranks[group]
            n = len(ranks)
            for k in k_vals:
                rec = round(float(np.mean([1.0 if r <= k else 0.0 for r in ranks])) * 100.0, 1)
                res[f"{group}_R@{k}"] = rec
            mrr = round(float(np.mean([1.0 / r for r in ranks])), 4)
            res[f"{group}_MRR"] = mrr
            
        all_results.append(res)
        
    # Print formatted comparison table
    print("\n" + "=" * 120)
    print(f"{'Configuration':<42} | {'R@1':<6} | {'R@3':<6} | {'R@5':<6} | {'R@10':<6} | {'MRR':<7} | {'Tier1 R@5':<10} | {'Tier2 R@5':<10} | {'Tier3 R@5':<10} | {'Latency':<8}")
    print("-" * 120)
    for r in all_results:
        cfg = r["Configuration"]
        r1 = f"{r['Overall_R@1']}%"
        r3 = f"{r['Overall_R@3']}%"
        r5 = f"{r['Overall_R@5']}%"
        r10 = f"{r['Overall_R@10']}%"
        mrr = f"{r['Overall_MRR']:.4f}"
        t1 = f"{r['Tier 1: Surface & Quantitative_R@5']}%"
        t2 = f"{r['Tier 2: Preemption & Carve-Outs_R@5']}%"
        t3 = f"{r['Tier 3: Latent & Paraphrastic_R@5']}%"
        lat = f"{r['Latency_ms']} ms"
        print(f"{cfg:<42} | {r1:<6} | {r3:<6} | {r5:<6} | {r10:<6} | {mrr:<7} | {t1:<10} | {t2:<10} | {t3:<10} | {lat:<8}")
    print("=" * 120)
    
    # Save results to JSON
    out_json = os.path.join("output", "stage1_proposals_experiment_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n[+] Detailed benchmark results saved to: {out_json}")


if __name__ == "__main__":
    main()
