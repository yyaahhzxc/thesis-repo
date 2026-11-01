"""
generate_presentation_ch3_figures.py
====================================
Generates 4 publication-grade, high-contrast visual figures specifically
tailored for defense presentation slides (16:9 ratio, clean card aesthetics):
1. slide14_corpus_acquisition_comparison.png (Figures 3.2, 3.3, 3.4 composite)
2. slide15_ground_truth_benchmark_card.png (Benchmark Dataset & Human Study)
3. slide16_two_stage_architecture_card.png (Stage 1 vs Stage 2 comparison)
4. slide17_evaluation_and_testing_card.png (Metrics + Hypothesis Testing)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from pathlib import Path
import numpy as np

OUTPUT_DIR = Path("CS_Undergraduate_Thesis_Template/figs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SLIDES_VIZ_DIR = Path("output/visualizations")
SLIDES_VIZ_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# -------------------------------------------------------------------
# 1. Slide 14: Corpus Acquisition & Media Comparison (Fig 3.2, 3.3, 3.4)
# -------------------------------------------------------------------
def generate_slide14_figure():
    print("[1/4] Generating slide14_corpus_acquisition_comparison.png...")
    img1_path = OUTPUT_DIR / "lawphil_republic_act_sample.png"
    img2_path = OUTPUT_DIR / "davao_ordinance_scan_sample.png"
    img3_path = OUTPUT_DIR / "davao_ordinance_scan_extreme_degradation.png"

    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    img3 = Image.open(img3_path)

    # Crop to relevant text portions for clear presentation readability
    w1, h1 = img1.size
    crop1 = img1.crop((0, int(h1 * 0.12), w1, int(h1 * 0.88)))

    w2, h2 = img2.size
    crop2 = img2.crop((int(w2 * 0.04), int(h2 * 0.04), int(w2 * 0.96), int(h2 * 0.50)))

    w3, h3 = img3.size
    crop3 = img3.crop((int(w3 * 0.04), int(h3 * 0.04), int(w3 * 0.96), int(h3 * 0.50)))

    fig, axes = plt.subplots(1, 3, figsize=(14.0, 7.2), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    panels = [
        (crop1, "National Statutes (Lawphil HTML)", "Clean, modern, machine-readable text structure", "#1b5e20"),
        (crop2, "Davao City Ordinances (Modern Scan)", "Clean scan from Sangguniang Panlungsod LISSP portal", "#0d47a1"),
        (crop3, "Pre-LGC Archival Scan (Extreme Noise)", "Faded typewriter text, severe bleed-through, dark noise", "#b71c1c")
    ]

    for ax, (img, title, subtitle, color) in zip(axes, panels):
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(f"{title}\n", fontsize=11, fontweight='bold', color=color, pad=8)
        ax.text(0.5, 1.01, subtitle, transform=ax.transAxes, fontsize=8.2, ha='center', va='bottom', color='#555555', style='italic')
        for spine in ['top', 'bottom', 'left', 'right']:
            ax.spines[spine].set_visible(True)
            ax.spines[spine].set_color('#cccccc')
            ax.spines[spine].set_linewidth(1.0)

    plt.tight_layout(pad=2.0)
    p1 = OUTPUT_DIR / "slide14_corpus_acquisition_comparison.png"
    p2 = SLIDES_VIZ_DIR / "slide14_corpus_acquisition_comparison.png"
    fig.savefig(p1, dpi=300, bbox_inches='tight')
    fig.savefig(p2, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {p1}")

# -------------------------------------------------------------------
# 2. Slide 15: Ground Truth Benchmark & Expert Human Evaluation Card
# -------------------------------------------------------------------
def generate_slide15_figure():
    print("[2/4] Generating slide15_ground_truth_benchmark_card.png...")
    fig, ax = plt.subplots(figsize=(14.0, 7.5), dpi=300)
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    ax.axis('off')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7.5)

    # Left Container: Ground-Truth Dataset Construction
    rect1 = patches.FancyBboxPatch((0.4, 0.5), 6.3, 6.4, boxstyle="round,pad=0.2,rounding_size=0.25",
                                   facecolor='#ffffff', edgecolor='#d97706', linewidth=2.4)
    ax.add_patch(rect1)

    # Header 1
    h_box1 = patches.FancyBboxPatch((0.4, 5.9), 6.3, 1.0, boxstyle="round,pad=0.1,rounding_size=0.15",
                                    facecolor='#d97706', edgecolor='#d97706')
    ax.add_patch(h_box1)
    ax.text(3.55, 6.45, "GROUND-TRUTH BENCHMARK DATASET", ha='center', va='center',
            fontsize=13.0, fontweight='bold', color='#ffffff')
    ax.text(3.55, 6.08, "350 Curated Pairs • Power Analysis > 98.5% (§3.5)", ha='center', va='center',
            fontsize=9.2, color='#fef3c7')

    # Content 1
    s1_text = [
        ("Curated Sample Size", "350 Ground-Truth Statutory Pairs across 8 macro domains"),
        ("Partition Split", "70% Train (245) • 15% Validation (52) • 15% Test (53 pairs)"),
        ("Directional Framing", "Premise = Controlling Statute; Hypothesis = Draft Ordinance"),
        ("Class Distribution", "Balanced across Entailment, Contradiction, and Neutral"),
        ("Adversarial Mining", "Hard negatives & near-miss penalty pairs to defeat bias"),
        ("Difficulty Stratification", "Tier 1: Lexical • Tier 2: Structural • Tier 3: Semantic")
    ]
    y_pos = 5.4
    for title, desc in s1_text:
        ax.text(0.75, y_pos, f"• {title}:", fontsize=9.8, fontweight='bold', color='#d97706')
        ax.text(0.75, y_pos - 0.32, f"   {desc}", fontsize=8.8, color='#333333')
        y_pos -= 0.78

    # Right Container: 15 Legal Researchers Study
    rect2 = patches.FancyBboxPatch((7.3, 0.5), 6.3, 6.4, boxstyle="round,pad=0.2,rounding_size=0.25",
                                   facecolor='#ffffff', edgecolor='#0d9488', linewidth=2.4)
    ax.add_patch(rect2)

    # Header 2
    h_box2 = patches.FancyBboxPatch((7.3, 5.9), 6.3, 1.0, boxstyle="round,pad=0.1,rounding_size=0.15",
                                    facecolor='#0d9488', edgecolor='#0d9488')
    ax.add_patch(h_box2)
    ax.text(10.45, 6.45, "15 LEGAL RESEARCHERS USER STUDY", ha='center', va='center',
            fontsize=13.0, fontweight='bold', color='#ffffff')
    ax.text(10.45, 6.08, "Davao City Sangguniang Panlungsod Protocol (§3.5)", ha='center', va='center',
            fontsize=9.2, color='#ccfbf1')

    # Content 2
    s2_text = [
        ("Domain Expert Cohort", "15 Davao City Sangguniang Panlungsod legal researchers"),
        ("Panel Allocation", "5 Independent Review Panels of 3 Evaluators (70 pairs / panel)"),
        ("Triple Redundancy", "3-Fold blind evaluation for every statutory conflict candidate"),
        ("Agreement Metric", "Fleiss' Multi-Rater Kappa (kappa) + Blind Adjudication Panel"),
        ("Usability Evaluation", "Standardized SUS (System Usability Scale) & PSSUQ instruments"),
        ("Institutional Commendation", "Civil Service 201 Commendation Certificates awarded by SP")
    ]
    y_pos = 5.4
    for title, desc in s2_text:
        ax.text(7.65, y_pos, f"• {title}:", fontsize=9.8, fontweight='bold', color='#0d9488')
        ax.text(7.65, y_pos - 0.32, f"   {desc}", fontsize=8.8, color='#333333')
        y_pos -= 0.78

    p1 = OUTPUT_DIR / "slide15_ground_truth_benchmark_card.png"
    p2 = SLIDES_VIZ_DIR / "slide15_ground_truth_benchmark_card.png"
    fig.savefig(p1, dpi=300, bbox_inches='tight')
    fig.savefig(p2, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {p1}")

# -------------------------------------------------------------------
# 3. Slide 16: Two-Stage Architecture Comparison Card
# -------------------------------------------------------------------
def generate_slide16_figure():
    print("[3/4] Generating slide16_two_stage_architecture_card.png...")
    fig, ax = plt.subplots(figsize=(14.0, 7.5), dpi=300)
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    ax.axis('off')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7.5)

    # Left Container: Stage 1 Hybrid Retrieval
    rect1 = patches.FancyBboxPatch((0.4, 0.5), 6.3, 6.4, boxstyle="round,pad=0.2,rounding_size=0.25",
                                   facecolor='#ffffff', edgecolor='#1f77b4', linewidth=2.4)
    ax.add_patch(rect1)

    # Header 1
    h_box1 = patches.FancyBboxPatch((0.4, 5.9), 6.3, 1.0, boxstyle="round,pad=0.1,rounding_size=0.15",
                                    facecolor='#1f77b4', edgecolor='#1f77b4')
    ax.add_patch(h_box1)
    ax.text(3.55, 6.45, "STAGE 1: HYBRID RETRIEVAL", ha='center', va='center',
            fontsize=13.0, fontweight='bold', color='#ffffff')
    ax.text(3.55, 6.08, "High-Throughput Coarse Search (Top-50 Candidates)", ha='center', va='center',
            fontsize=9.2, color='#e0f0ff')

    # Content 1
    s1_text = [
        ("Search Space", "27,357 Enactments • 178,494 Searchable Provisions"),
        ("Dual-Stream Fusion", "Sparse BM25 (Exact terms/fines) + Dense all-MiniLM-L6-v2"),
        ("Rank Aggregation", "Reciprocal Rank Fusion (RRF, k = 60) without score bias"),
        ("Hierarchy Safeguard", "National statutes explicitly prioritized over municipal history"),
        ("Candidate Shortlist", "Narrows 178k provisions down to top k = 50 in 14.8 ms"),
        ("Edge Performance", "Executes sub-second CPU search under 4 threads (< 1.5 GB RAM)")
    ]
    y_pos = 5.4
    for title, desc in s1_text:
        ax.text(0.75, y_pos, f"• {title}:", fontsize=9.8, fontweight='bold', color='#1f77b4')
        ax.text(0.75, y_pos - 0.32, f"   {desc}", fontsize=8.8, color='#333333')
        y_pos -= 0.78

    # Right Container: Stage 2 Cross-Encoder Inference
    rect2 = patches.FancyBboxPatch((7.3, 0.5), 6.3, 6.4, boxstyle="round,pad=0.2,rounding_size=0.25",
                                   facecolor='#ffffff', edgecolor='#7F2723', linewidth=2.4)
    ax.add_patch(rect2)

    # Header 2
    h_box2 = patches.FancyBboxPatch((7.3, 5.9), 6.3, 1.0, boxstyle="round,pad=0.1,rounding_size=0.15",
                                    facecolor='#7F2723', edgecolor='#7F2723')
    ax.add_patch(h_box2)
    ax.text(10.45, 6.45, "STAGE 2: CROSS-ENCODER NLI", ha='center', va='center',
            fontsize=13.0, fontweight='bold', color='#ffffff')
    ax.text(10.45, 6.08, "Deep Logical Reasoning & Threshold Calibration", ha='center', va='center',
            fontsize=9.2, color='#ffd5d4')

    # Content 2
    s2_text = [
        ("Input Sequence", "[CLS] Controlling Statute Premise [SEP] Draft Hypothesis [SEP]"),
        ("Neural Engine", "Fine-Tuned DeBERTa-v3 Cross-Encoder (AVX2 CPU execution)"),
        ("Cross-Attention", "Every draft token directly attends to statutory mandate words"),
        ("Bias Elimination", "Eliminates foundation model affirmative entailment bias (+39.7%)"),
        ("Threshold Tuning", "Calibrated decision threshold tau* = 0.45 for safety margin"),
        ("Asymmetric Cost", "Penalizes false negatives 5:1 (C_FN / C_FP) under Magtajas")
    ]
    y_pos = 5.4
    for title, desc in s2_text:
        ax.text(7.65, y_pos, f"• {title}:", fontsize=9.8, fontweight='bold', color='#7F2723')
        ax.text(7.65, y_pos - 0.32, f"   {desc}", fontsize=8.8, color='#333333')
        y_pos -= 0.78

    p1 = OUTPUT_DIR / "slide16_two_stage_architecture_card.png"
    p2 = SLIDES_VIZ_DIR / "slide16_two_stage_architecture_card.png"
    fig.savefig(p1, dpi=300, bbox_inches='tight')
    fig.savefig(p2, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {p1}")

# -------------------------------------------------------------------
# 4. Slide 17: Evaluation Metrics & Statistical Testing Card
# -------------------------------------------------------------------
def generate_slide17_figure():
    print("[4/4] Generating slide17_evaluation_and_testing_card.png...")
    fig, ax = plt.subplots(figsize=(14.0, 7.5), dpi=300)
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    ax.axis('off')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7.5)

    # Left Container: Performance Metrics
    rect1 = patches.FancyBboxPatch((0.4, 0.5), 6.3, 6.4, boxstyle="round,pad=0.2,rounding_size=0.25",
                                   facecolor='#ffffff', edgecolor='#28a745', linewidth=2.4)
    ax.add_patch(rect1)

    h_box1 = patches.FancyBboxPatch((0.4, 5.9), 6.3, 1.0, boxstyle="round,pad=0.1,rounding_size=0.15",
                                    facecolor='#28a745', edgecolor='#28a745')
    ax.add_patch(h_box1)
    ax.text(3.55, 6.45, "SYSTEM PERFORMANCE METRICS", ha='center', va='center',
            fontsize=13.0, fontweight='bold', color='#ffffff')
    ax.text(3.55, 6.08, "Recall, Ranking & Edge Latency Standards (§3.8)", ha='center', va='center',
            fontsize=9.2, color='#e0f7e9')

    m1_text = [
        ("Candidate Recall", "Recall@k (k in {5, 10, 20, 50}): Target 100% preemption coverage"),
        ("Mean Reciprocal Rank", "MRR: Measures top-rank proximity of governing national statute"),
        ("Classification Loss", "Macro F1 & Conflict Class F1 (evaluating rare legal clashes)"),
        ("End-to-End Recall", "FEVER Metric: Requires both correct statute retrieval & NLI verdict"),
        ("Edge Latency Profiling", "Throttled 4-thread CPU benchmark on Host A (< 15 s full audit)"),
        ("Memory Footprint", "Resident RAM tracking verifying compliance with 8 GB LGU cap")
    ]
    y_pos = 5.4
    for title, desc in m1_text:
        ax.text(0.75, y_pos, f"• {title}:", fontsize=9.8, fontweight='bold', color='#28a745')
        ax.text(0.75, y_pos - 0.32, f"   {desc}", fontsize=8.8, color='#333333')
        y_pos -= 0.78

    # Right Container: Statistical Hypothesis Testing
    rect2 = patches.FancyBboxPatch((7.3, 0.5), 6.3, 6.4, boxstyle="round,pad=0.2,rounding_size=0.25",
                                   facecolor='#ffffff', edgecolor='#6f42c1', linewidth=2.4)
    ax.add_patch(rect2)

    h_box2 = patches.FancyBboxPatch((7.3, 5.9), 6.3, 1.0, boxstyle="round,pad=0.1,rounding_size=0.15",
                                    facecolor='#6f42c1', edgecolor='#6f42c1')
    ax.add_patch(h_box2)
    ax.text(10.45, 6.45, "STATISTICAL HYPOTHESIS TESTING", ha='center', va='center',
            fontsize=13.0, fontweight='bold', color='#ffffff')
    ax.text(10.45, 6.08, "Non-Parametric Significance Protocols (§3.9)", ha='center', va='center',
            fontsize=9.2, color='#f0e8ff')

    m2_text = [
        ("Domain Invariance", "Non-parametric Friedman ANOVA across all 8 macro legal domains"),
        ("Critical Threshold", "Friedman chi_F^2 statistic verifying consistent cross-domain rank"),
        ("Pairwise Significance", "McNemar's test analyzing discordant prediction pairs (b vs c)"),
        ("Edwards Correction", "Applies (|b - c| - 1)^2 / (b + c) to prevent small-sample alpha inflation"),
        ("Deceptive Accuracy", "Rejects raw accuracy averages due to 3-class skewed distributions"),
        ("Significance Level", "Rigorous alpha = 0.05 rejection boundary across all test partitions")
    ]
    y_pos = 5.4
    for title, desc in m2_text:
        ax.text(7.65, y_pos, f"• {title}:", fontsize=9.8, fontweight='bold', color='#6f42c1')
        ax.text(7.65, y_pos - 0.32, f"   {desc}", fontsize=8.8, color='#333333')
        y_pos -= 0.78

    p1 = OUTPUT_DIR / "slide17_evaluation_and_testing_card.png"
    p2 = SLIDES_VIZ_DIR / "slide17_evaluation_and_testing_card.png"
    fig.savefig(p1, dpi=300, bbox_inches='tight')
    fig.savefig(p2, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {p1}")

if __name__ == "__main__":
    generate_slide14_figure()
    generate_slide15_figure()
    generate_slide16_figure()
    generate_slide17_figure()
