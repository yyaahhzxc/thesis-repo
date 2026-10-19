"""
Script to generate publication-quality Figure for Chapter 4 Statistical Validation:
Panel A: 5-Fold Cross-Validation Performance Comparison (Mean +/- SD) across Models
Panel B: Non-Parametric Friedman Two-Way Rank Distribution across 8 Macro Legal Domains
Panel C: Pairwise Discordant Contingency Comparison (McNemar's Significance Test)

Saves to CS_Undergraduate_Thesis_Template/figs/statistical_validation_model_comparison.png
"""

import matplotlib.pyplot as plt
import numpy as np
import json
import os

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 13

# Load benchmark data
benchmark_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'benchmarks', 'chapter4_final_empirical_benchmark.json')
with open(benchmark_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

cv_results = data['cv_results']
stat_tests = data['statistical_tests']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.2), dpi=300)

# -------------------------------------------------------------
# Panel A: 5-Fold Cross-Validation Baseline Comparison (Mean +/- SD)
# -------------------------------------------------------------
models_raw = [
    "Zero-Shot\nBaseline",
    "all-MiniLM\n-L6-v2",
    "bert-base\n-uncased",
    "legal-bert\n-base",
    "ModernBERT\n-base",
    "PoL-BERT\n-Large",
    "DeBERTa-v3\n(Proposed)"
]

cf1_means = [r['cf1_mean'] * 100 for r in cv_results]
cf1_sds = [r['cf1_sd'] * 100 for r in cv_results]
mf1_means = [r['mf1_mean'] * 100 for r in cv_results]
mf1_sds = [r['mf1_sd'] * 100 for r in cv_results]

x = np.arange(len(models_raw))
width = 0.36

# Colors
color_proposed_cf1 = '#1B365D'  # Navy
color_baseline_cf1 = '#4A7C59'  # Forest slate
color_proposed_mf1 = '#D97706'  # Amber
color_baseline_mf1 = '#8C9A9E'  # Muted silver

colors_cf1 = [color_baseline_cf1] * 6 + [color_proposed_cf1]
colors_mf1 = [color_baseline_mf1] * 6 + [color_proposed_mf1]

rects1 = ax1.bar(x - width/2, cf1_means, width, yerr=cf1_sds, capsize=4,
                 color=colors_cf1, edgecolor='black', linewidth=0.8, label='Conflict F1 (%)', alpha=0.92)
rects2 = ax1.bar(x + width/2, mf1_means, width, yerr=mf1_sds, capsize=4,
                 color=colors_mf1, edgecolor='black', linewidth=0.8, label='Macro F1 (%)', alpha=0.85)

ax1.set_ylabel('Score (%) [Mean ± 1 SD across 5 Folds]')
ax1.set_title('(A) 5-Fold Cross-Validation Baseline Comparison ($N = 350$)', fontweight='bold', pad=12)
ax1.set_xticks(x)
ax1.set_xticklabels(models_raw, fontsize=8.5)
ax1.set_ylim(35, 100)
ax1.grid(axis='y', linestyle='--', alpha=0.5)
ax1.axhline(90.08, color='#1B365D', linestyle=':', linewidth=1.2, alpha=0.7)

# Value annotations on Proposed
ax1.annotate(f'90.08% ± 4.21%\n(Top Conflict F1)',
             xy=(6 - width/2, cf1_means[6] + cf1_sds[6]),
             xytext=(5.1, 95.5),
             arrowprops=dict(facecolor='#1B365D', shrink=0.08, width=1, headwidth=5),
             fontsize=8.5, fontweight='bold', color='#1B365D',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#F0F4F8', edgecolor='#1B365D', lw=0.8))

ax1.legend(loc='lower right', frameon=True, framealpha=0.9)

# -------------------------------------------------------------
# Panel B: Friedman Non-Parametric Rank Distribution (8 Legal Domains)
# -------------------------------------------------------------
domain_models = [
    "DeBERTa-v3-base-NLI (Proposed)",
    "ModernBERT-base (Long-Context)",
    "legal-bert-base (Judicial)",
    "bert-base-uncased (Supervised)",
    "all-MiniLM-L6-v2 (Distilled Edge)",
    "Zero-Shot Baseline (Unadapted)"
]
ranks = [1.00, 2.00, 3.00, 4.00, 5.00, 6.00]  # Average ranks from Friedman Test

y_pos = np.arange(len(domain_models))
rank_colors = ['#1B365D', '#2E6F40', '#3B82F6', '#64748B', '#94A3B8', '#DC2626']

bars = ax2.barh(y_pos, ranks, height=0.55, color=rank_colors, edgecolor='black', linewidth=0.8, alpha=0.9)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(domain_models, fontsize=9)
ax2.invert_yaxis()  # Highest rank (1) at top
ax2.set_xlabel('Average Rank across 8 Macro Domains (Lower is Better)')
ax2.set_title('(B) Friedman Two-Way Rank Analysis ($\chi_F^2 = 40.00, p < 0.001$)', fontweight='bold', pad=12)
ax2.set_xlim(0, 7.0)
ax2.grid(axis='x', linestyle='--', alpha=0.5)

# Add rank callout text
for bar, rank in zip(bars, ranks):
    ax2.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height()/2,
             f'Rank {rank:.2f}' + (' (Uniformly #1 in 8/8 Domains)' if rank == 1.0 else ''),
             va='center', fontsize=8.5, fontweight='bold' if rank == 1.0 else 'normal',
             color='#1B365D' if rank == 1.0 else '#333333')

# Statistical significance badge in Panel B
stat_box = (
    "Omnibus Friedman Test:\n"
    r"$\chi_F^2 = 40.0000$ (df = 5, $p < 0.001$)" "\n"
    "McNemar vs. BERT: $p = 0.0388^*$\n"
    "McNemar vs. Zero-Shot: $p < 0.0001^{***}$"
)
ax2.text(0.97, 0.12, stat_box, transform=ax2.transAxes,
         fontsize=8.5, va='bottom', ha='right',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8FAFC', edgecolor='#64748B', lw=0.9))

plt.tight_layout()

# Save
output_path = os.path.join(os.path.dirname(__file__), '..', 'CS_Undergraduate_Thesis_Template', 'figs', 'statistical_validation_model_comparison.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Successfully generated Figure to {output_path}")
