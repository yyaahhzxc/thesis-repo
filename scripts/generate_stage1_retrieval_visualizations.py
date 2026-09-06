"""
generate_stage1_retrieval_visualizations.py
=============================================
Generates publication-ready (300 DPI) LaTeX figure for Chapter 3 (Methodology)
comparing candidate Stage 1 coarse retrieval architectures across difficulty tiers:
1. Pure BM25 Baseline
2. BM25 + Hard Domain Filter (Illustrating catastrophic drop)
3. BM25 + Hierarchy Priority Safeguard
4. Dense Bi-Encoder (MiniLM)
5. Hybrid Weighted Aggregation (alpha=0.5)
6. Hybrid Reciprocal Rank Fusion (RRF k=60)
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Output directories
TEMPLATE_FIGS_DIR = os.path.join("CS_Undergraduate_Thesis_Template", "figs")
OUTPUT_VIZ_DIR = os.path.join("output", "visualizations")
os.makedirs(TEMPLATE_FIGS_DIR, exist_ok=True)
os.makedirs(OUTPUT_VIZ_DIR, exist_ok=True)

# Publication styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#222222'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#e0e0e0'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.6


def generate_stage1_ablation_figure():
    print("Generating Stage 1 Retrieval Ablation Figure...")
    
    # Selected key configurations to showcase the progression
    configs = [
        "Pure BM25\nBaseline",
        "BM25 + Hard\nDomain Filter",
        "BM25 + Hierarchy\nPriority",
        "Dense Bi-Encoder\n(MiniLM)",
        "Hybrid RRF\n(k=60)",
        "Hybrid RRF +\nSoft Prior"
    ]
    
    # Recall@10 metrics
    r10_overall = [83.1, 100.0, 89.4, 98.3, 94.0, 91.4]
    # Note: On full corpus (25,432), BM25 baseline R@10 is 29.7%, Hard Filter is 7.7%, Hierarchy is 34.9%.
    # In verified premise benchmark:
    # BM25 baseline: R@5=75.1%, R@10=83.1%, MRR=0.6172
    # Hard Filter: artificially high when domain matches, but fails on full corpus (7.7% on full 25k).
    # Let's show both the 350-Premise Benchmark across Difficulty Tiers AND Full-Corpus Sensitivity!
    
    # Let's inspect the exact results from stage1_proposals_experiment_results.json
    with open("output/stage1_proposals_experiment_results.json", "r") as f:
        data = json.load(f)
    
    cfg_names = [
        "1. Pure BM25 (AIIR Lab Baseline)",
        "4. Pure Dense Bi-Encoder (MiniLM)",
        "5. Hybrid JNLP (Weighted Sum α=0.5)",
        "8. Reciprocal Rank Fusion (RRF k=60)",
        "9. Hybrid + Soft Domain Prior (α=0.5)"
    ]
    
    filtered_data = [d for d in data if d["Configuration"] in cfg_names]
    
    # Colors: Academic Slate, Amber, Navy, Teal, Crimson
    colors = {
        "bm25": "#4B6584",
        "dense": "#20BF6B",
        "weighted": "#FA8231",
        "rrf": "#3867D6",
        "soft_rrf": "#8854D0"
    }
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.2), dpi=300)
    
    # Panel A: Recall@k Progression across candidate retrievers
    k_vals = [1, 3, 5, 10, 20]
    
    arch_labels = [
        ("1. Pure BM25 Baseline", "#4B6584", "o-", 2.0),
        ("4. Pure Dense Bi-Encoder", "#20BF6B", "s--", 2.2),
        ("5. Hybrid Weighted Sum (α=0.5)", "#FA8231", "^-.", 2.0),
        ("8. Reciprocal Rank Fusion (RRF)", "#3867D6", "D-", 2.6),
        ("9. Hybrid RRF + Soft Prior", "#8854D0", "v-", 2.0)
    ]
    
    for cfg_key, col, style, lw in arch_labels:
        item = next(d for d in data if d["Configuration"].startswith(cfg_key[:2]))
        recalls = [item[f"Overall_R@{k}"] for k in k_vals]
        ax1.plot(k_vals, recalls, style, color=col, linewidth=lw, markersize=7, label=item["Configuration"])
        
    ax1.set_title("Panel A: Multi-Candidate Recall@k Progression ($N = 350$)", fontsize=11, fontweight='bold', pad=10)
    ax1.set_xlabel("Candidate Shortlist Size ($k$)", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Candidate Retrieval Recall (%)", fontsize=10, fontweight='bold')
    ax1.set_xticks(k_vals)
    ax1.set_ylim(45, 103)
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend(loc="lower right", framealpha=0.92, fontsize=8.5)
    
    # Annotate Top Recall@10 for RRF and Dense
    ax1.annotate(f"RRF R@10 = 94.0%\nMRR = 0.7109", 
                 xy=(10, 94.0), xytext=(8.0, 84.0),
                 arrowprops=dict(arrowstyle="->", color="#3867D6", lw=1.5),
                 fontsize=8.5, fontweight='bold', color="#3867D6",
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#3867D6", lw=1.0))
    
    ax1.annotate(f"BM25 Baseline R@10 = 83.1%\nMRR = 0.6172", 
                 xy=(10, 83.1), xytext=(11.5, 72.0),
                 arrowprops=dict(arrowstyle="->", color="#4B6584", lw=1.5),
                 fontsize=8.5, fontweight='bold', color="#4B6584",
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#4B6584", lw=1.0))

    # Panel B: Breakdown by Jurisprudential Difficulty Tier (Recall@5)
    tiers = [
        "Tier 1: Surface &\nQuantitative",
        "Tier 2: Preemption &\nCarve-Outs",
        "Tier 3: Latent &\nParaphrastic"
    ]
    
    x = np.arange(len(tiers))
    bar_width = 0.22
    
    bm25_item = next(d for d in data if d["Configuration"].startswith("1."))
    dense_item = next(d for d in data if d["Configuration"].startswith("4."))
    rrf_item = next(d for d in data if d["Configuration"].startswith("8."))
    
    bm25_tier_r5 = [
        bm25_item["Tier 1: Surface & Quantitative_R@5"],
        bm25_item["Tier 2: Preemption & Carve-Outs_R@5"],
        bm25_item["Tier 3: Latent & Paraphrastic_R@5"]
    ]
    
    dense_tier_r5 = [
        dense_item["Tier 1: Surface & Quantitative_R@5"],
        dense_item["Tier 2: Preemption & Carve-Outs_R@5"],
        dense_item["Tier 3: Latent & Paraphrastic_R@5"]
    ]
    
    rrf_tier_r5 = [
        rrf_item["Tier 1: Surface & Quantitative_R@5"],
        rrf_item["Tier 2: Preemption & Carve-Outs_R@5"],
        rrf_item["Tier 3: Latent & Paraphrastic_R@5"]
    ]
    
    rects1 = ax2.bar(x - bar_width, bm25_tier_r5, bar_width, label="Pure BM25 (AIIR)", color="#4B6584", edgecolor="#222222", lw=0.8)
    rects2 = ax2.bar(x, dense_tier_r5, bar_width, label="Dense Bi-Encoder (MiniLM)", color="#20BF6B", edgecolor="#222222", lw=0.8)
    rects3 = ax2.bar(x + bar_width, rrf_tier_r5, bar_width, label="Hybrid RRF (k=60)", color="#3867D6", edgecolor="#222222", lw=0.8)
    
    ax2.set_title("Panel B: Candidate Recall@5 by Difficulty Tier", fontsize=11, fontweight='bold', pad=10)
    ax2.set_ylabel("Recall@5 (%)", fontsize=10, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(tiers, fontsize=9.5, fontweight='bold')
    ax2.set_ylim(45, 105)
    ax2.grid(True, linestyle="--", alpha=0.6, axis="y")
    ax2.legend(loc="upper left", framealpha=0.92, fontsize=8.5)
    
    # Value labels on top of bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax2.annotate(f"{height:.1f}%",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, fontweight='bold')
            
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    
    # Highlight the Tier 3 semantic gap
    gap = dense_tier_r5[2] - bm25_tier_r5[2]
    ax2.annotate(f"Semantic Gap:\n+{gap:.1f}% Absolute Gain",
                 xy=(2 - bar_width, bm25_tier_r5[2]), xytext=(1.45, 52.0),
                 arrowprops=dict(arrowstyle="->", color="#D63031", lw=1.5),
                 fontsize=8.5, fontweight='bold', color="#D63031",
                 bbox=dict(boxstyle="round,pad=0.3", fc="#FFF5F5", ec="#D63031", lw=1.0))
    
    plt.tight_layout()
    
    # Save outputs
    out_fig_template = os.path.join(TEMPLATE_FIGS_DIR, "stage1_retrieval_ablation_performance.png")
    out_fig_viz = os.path.join(OUTPUT_VIZ_DIR, "stage1_retrieval_ablation_performance.png")
    
    fig.savefig(out_fig_template, dpi=300, bbox_inches='tight')
    fig.savefig(out_fig_viz, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure saved to {out_fig_template} and {out_fig_viz}")

if __name__ == "__main__":
    generate_stage1_ablation_figure()
