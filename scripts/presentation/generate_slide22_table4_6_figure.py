"""
generate_slide22_table4_6_figure.py
===================================
Generates a 300 DPI publication-grade graphic of Table 4.6 (Dual Statutory Corpus Parameters)
specifically formatted for presentation slides and Canva drag-and-drop.
Strictly adheres to academic booktabs conventions (zero vertical lines).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

OUTPUT_DIR = Path("CS_Undergraduate_Thesis_Template/figs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SLIDES_VIZ_DIR = Path("output/visualizations")
SLIDES_VIZ_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

def generate_table4_6_card():
    fig = plt.figure(figsize=(14.2, 8.2), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Title Banner
    ax.text(0.04, 0.95, "Table 4.6: Structural Parameters of the Dual Statutory Search Space",
            fontsize=15.5, fontweight='bold', color='#7F2723', va='top')
    ax.text(0.04, 0.90, "Comparative Metrics: National Legislation vs Davao City Local Ordinances (N = 27,357 Enactments, 178,494 Provisions)",
            fontsize=10.0, color='#475569', va='top')

    # Headers
    headers = ["Empirical Dimension / Metric", "National Corpus", "Local Corpus", "Combined Corpus", "Analytical Significance"]
    
    rows = [
        ["Total Enactments (N)", "25,432", "1,925", "27,357", "Comprehensive legislative space across both jurisdictions"],
        ["Total Section Provisions", "164,620", "13,874", "178,494", "Total searchable provision-level retrieval units"],
        ["Operative Provisions", "164,620", "9,487", "174,107", "Substantive regulatory provisions evaluated for conflict"],
        ["Procedural Boilerplate Sections", "0", "4,387 (31.62%)", "4,387", "Pruned procedural clauses (Title, Separability, Repealing)"],
        ["Historical Enactment Span", "1900–2026 (126 yrs)", "1950–2025 (75 yrs)", "1900–2026", "Longitudinal statutory breadth spanning all legal regimes"],
        ["Median Enactment Words", "1,512 words", "914 words", "1,476 words", "Local enactments exhibit concise municipal focus"],
        ["Median Provision Tokens", "122.0 tokens", "90.0 tokens", "120.0 tokens", "Granular provision baseline for dense vector retrieval"],
        ["512-Token Compliance Rate", "94.83%", "93.82%", "94.75%", "Overwhelming natural compatibility with 512 context limit"],
        ["Normative Conflict Scope", "Vertical Preemption", "Horizontal Coherence", "Dual Scope", "Statutory preemption (Magtajas) + local intra-coherence"]
    ]

    # Column x positions
    # Metric: 0.045, National: 0.32, Local: 0.47, Combined: 0.62, Significance: 0.74
    x_pos = [0.045, 0.32, 0.47, 0.62, 0.75]
    y_start = 0.83
    row_height = 0.060

    # Top Rule
    ax.plot([0.03, 0.98], [y_start + 0.02, y_start + 0.02], color='#7F2723', linewidth=2.8, zorder=3)

    # Headers
    for col_idx, (x, h) in enumerate(zip(x_pos, headers)):
        align = 'center' if col_idx in [1, 2, 3] else 'left'
        color = '#1E40AF' if col_idx == 3 else '#7F2723'
        ax.text(x, y_start - 0.015, h, fontsize=9.8, fontweight='bold', color=color, ha=align, va='center', zorder=4)

    # Mid Rule
    mid_y = y_start - 0.045
    ax.plot([0.03, 0.98], [mid_y, mid_y], color='#94A3B8', linewidth=1.5, zorder=3)

    # Highlight Combined Column
    comb_rect = patches.Rectangle(
        (0.55, mid_y - len(rows)*row_height - 0.01), 0.14, len(rows)*row_height + 0.01,
        facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=1.2, zorder=1, linestyle='--'
    )
    ax.add_patch(comb_rect)

    cur_y = mid_y
    for r_idx, row in enumerate(rows):
        cur_y -= row_height
        for col_idx, (x, val) in enumerate(zip(x_pos, row)):
            align = 'center' if col_idx in [1, 2, 3] else 'left'
            weight = 'bold' if col_idx in [0, 3] else 'normal'
            if col_idx == 3:
                color = '#1E40AF'
            elif col_idx == 0:
                color = '#1E293B'
            else:
                color = '#334155'
            font_size = 9.0 if col_idx == 4 else 9.5
            ax.text(x, cur_y + 0.01, val, fontsize=font_size, fontweight=weight, color=color, ha=align, va='center', zorder=4)

        if r_idx < len(rows) - 1:
            ax.plot([0.03, 0.98], [cur_y - 0.015, cur_y - 0.015], color='#F1F5F9', linewidth=0.7, zorder=2)

    # Bottom Rule
    bot_y = cur_y - 0.025
    ax.plot([0.03, 0.98], [bot_y, bot_y], color='#7F2723', linewidth=2.8, zorder=3)

    # Footer note
    note_text = "Note: Unified dual corpus compiled into data/unified_dual_statutory_provisions.jsonl (400.4 MB). 94.75% of provisions naturally fit the standard 512-token context window."
    ax.text(0.04, bot_y - 0.035, note_text, fontsize=8.2, color='#64748B', style='italic', va='top')

    plt.tight_layout()
    out1 = OUTPUT_DIR / "slide22_table4_6_dual_corpus.png"
    out2 = SLIDES_VIZ_DIR / "slide22_table4_6_dual_corpus.png"
    out3 = OUTPUT_DIR / "slide25_table4_6_dual_corpus.png"
    out4 = SLIDES_VIZ_DIR / "slide25_table4_6_dual_corpus.png"
    fig.savefig(out1, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    fig.savefig(out2, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    fig.savefig(out3, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    fig.savefig(out4, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close(fig)
    print(f"Generated {out1}, {out2}, {out3}, and {out4} successfully!")

if __name__ == "__main__":
    generate_table4_6_card()
