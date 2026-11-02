"""
generate_slide_tables_4_17_and_4_20.py
======================================
Generates 300 DPI publication-grade graphics of:
1. Table 4.17 (Audit Latency Scaling on 4-Thread CPU)
2. Table 4.20 (Tier 2 Full-Document Stress Test & Section Accuracy Rate)
Specifically formatted for presentation slides and Canva drag-and-drop (Booktabs style).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

OUTPUT_DIR = Path("CS_Undergraduate_Thesis_Template/figs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SLIDES_VIZ_DIR = Path("output/visualizations")
SLIDES_VIZ_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# -------------------------------------------------------------
# 1. Table 4.17: Audit Latency Scaling
# -------------------------------------------------------------
def generate_table4_17_card():
    fig = plt.figure(figsize=(13.5, 6.2), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Title Banner
    ax.text(0.04, 0.94, "Table 4.17: Pre-Enactment Audit Latency Scaling on 4-Thread CPU",
            fontsize=15.5, fontweight='bold', color='#7F2723', va='top')
    ax.text(0.04, 0.88, "Runtime Profiling on LGU Edge Emulation Testbed (Host A: Core i3-10105F, 8 GB RAM, 14-Section Draft)",
            fontsize=10.0, color='#475569', va='top')

    headers = ["Shortlist Depth (k)", "Evaluated Pairs (N)", "Batch Tokens (L)", "Mean Pair Latency", "Audit Time", "Operational Edge Feasibility"]
    rows = [
        ["Top-5 Candidates", "35 pairs", "105 tokens", "130.2 ms", "4.56 s", "Near-Instantaneous Review (< 5 s)"],
        ["Top-10 Candidates", "70 pairs", "105 tokens", "129.5 ms", "9.07 s", "Responsive Interactive Audit (< 10 s)"],
        ["Top-15 Candidates", "105 pairs", "105 tokens", "120.8 ms", "12.68 s", "Comprehensive Statutory Audit (< 15 s)"],
        ["Top-25 Candidates", "175 pairs", "105 tokens", "139.7 ms", "24.45 s", "Deep Archival Verification (< 30 s)"]
    ]

    x_pos = [0.045, 0.22, 0.38, 0.52, 0.65, 0.77]
    y_start = 0.78
    row_height = 0.095

    # Highlight Top-15 (Standard Operating Depth)
    h_rect = patches.Rectangle(
        (0.03, y_start - 3 * row_height - 0.015), 0.95, row_height,
        facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=1.5, zorder=1, linestyle='--'
    )
    ax.add_patch(h_rect)

    # Top Rule
    ax.plot([0.03, 0.98], [y_start + 0.02, y_start + 0.02], color='#7F2723', linewidth=2.8, zorder=3)

    # Headers
    for col_idx, (x, h) in enumerate(zip(x_pos, headers)):
        align = 'center' if col_idx in [1, 2, 3, 4] else 'left'
        color = '#1E40AF' if col_idx == 4 else '#7F2723'
        ax.text(x, y_start - 0.02, h, fontsize=9.8, fontweight='bold', color=color, ha=align, va='center', zorder=4)

    # Mid Rule
    mid_y = y_start - 0.055
    ax.plot([0.03, 0.98], [mid_y, mid_y], color='#94A3B8', linewidth=1.5, zorder=3)

    # Rows
    for r_idx, row in enumerate(rows):
        cur_y = mid_y - (r_idx + 0.6) * row_height
        for col_idx, (x, val) in enumerate(zip(x_pos, row)):
            align = 'center' if col_idx in [1, 2, 3, 4] else 'left'
            weight = 'bold' if (col_idx == 4 or r_idx == 2) else ('bold' if col_idx == 0 else 'normal')
            color = '#1E40AF' if col_idx == 4 else ('#1E293B' if col_idx == 0 else '#334155')
            ax.text(x, cur_y, val, fontsize=9.5, fontweight=weight, color=color, ha=align, va='center', zorder=4)

        if r_idx < len(rows) - 1:
            sep_y = cur_y - 0.5 * row_height
            ax.plot([0.03, 0.98], [sep_y, sep_y], color='#F1F5F9', linewidth=0.8, zorder=2)

    # Bottom Rule
    bot_y = mid_y - len(rows) * row_height
    ax.plot([0.03, 0.98], [bot_y, bot_y], color='#7F2723', linewidth=2.8, zorder=3)

    # Note
    note_text = "Note: Standard review depth Top-15 finishes in 12.68 s on 4-thread CPU without GPU acceleration, proving LGU desktop viability."
    ax.text(0.04, bot_y - 0.05, note_text, fontsize=8.5, color='#64748B', style='italic', va='top')

    plt.tight_layout()
    out1 = OUTPUT_DIR / "slide25_table4_17_latency_scaling.png"
    out2 = SLIDES_VIZ_DIR / "slide25_table4_17_latency_scaling.png"
    fig.savefig(out1, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    fig.savefig(out2, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close(fig)
    print(f"Generated {out1} and {out2} successfully!")

# -------------------------------------------------------------
# 2. Table 4.20: Tier 2 Full-Document Section Accuracy
# -------------------------------------------------------------
def generate_table4_20_card():
    fig = plt.figure(figsize=(14.5, 8.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Title Banner
    ax.text(0.03, 0.96, "Table 4.20: Tier 2 Injected-Fault Full-Document Stress Testing Benchmark",
            fontsize=15.0, fontweight='bold', color='#7F2723', va='top')
    ax.text(0.03, 0.915, "Evaluation on 10 Multi-Section Draft Ordinances (140 Provisions) on Host A LGU Edge Emulation Workstation",
            fontsize=10.0, color='#475569', va='top')

    headers = ["Draft ID", "Regulatory Domain", "Total Sec.", "Defects", "Controlling National Statute", "Max Conflict Risk", "Verdict", "Section Acc."]
    rows = [
        ["DRAFT-01", "Organic Agriculture / Buffer Zones", "14", "1", "PD 1144 §§6, 9 (Fertilizer Authority)", "94.0%", "FLAGGED", "92.86%"],
        ["DRAFT-02", "Traffic / Warrantless Vehicle Search", "14", "1", "1987 Const. Art. III §2; RA 4136", "95.0%", "FLAGGED", "100.0%"],
        ["DRAFT-03", "Anti-Vagrancy / Curfew for Minors", "14", "2", "RA 9344 §6; RA 7160 §458", "96.0%", "FLAGGED", "100.0%"],
        ["DRAFT-04", "Freight Transit / Municipal Speed Limits", "14", "1", "RA 4136 §35; Joint JAO 2018-01", "94.0%", "FLAGGED", "100.0%"],
        ["DRAFT-05", "Commodity Price Freeze / Essential Goods", "14", "2", "RA 7581 §6; RA 7160 §16", "95.0%", "FLAGGED", "100.0%"],
        ["DRAFT-06", "Biometric CCTV Surveillance & Retention", "14", "1", "RA 10173 §§11, 12 (Data Privacy)", "94.0%", "FLAGGED", "100.0%"],
        ["DRAFT-07", "Coastal Municipal Fisheries / Penalties", "14", "2", "RA 8550 §86; RA 7160 §458", "97.0%", "FLAGGED", "100.0%"],
        ["DRAFT-08", "Building Construction & Fire Setbacks", "14", "1", "PD 1096 §301; RA 9514 §7", "94.0%", "FLAGGED", "100.0%"],
        ["DRAFT-09", "Small-Scale Mining Ban / Mineral Permits", "14", "2", "RA 7942 §19; RA 7076 §5", "95.0%", "FLAGGED", "100.0%"],
        ["DRAFT-10", "Local Revenue Dividend & Tax Assessment", "14", "2", "RA 7160 §133(a); RA 8291 §39", "99.9%", "FLAGGED", "100.0%"]
    ]
    total_row = ["Summary", "Overall Full-Document Pipeline Performance", "140", "15", "100% Contradiction Precision & Recall", "Mean: 95.4%", "10/10 FLAGGED", "97.86% (137/140)"]

    x_pos = [0.035, 0.11, 0.35, 0.405, 0.46, 0.725, 0.835, 0.93]
    y_start = 0.85
    row_height = 0.054

    # Top Rule
    ax.plot([0.025, 0.985], [y_start + 0.02, y_start + 0.02], color='#7F2723', linewidth=2.8, zorder=3)

    # Headers
    for col_idx, (x, h) in enumerate(zip(x_pos, headers)):
        align = 'center' if col_idx in [2, 3, 5, 6, 7] else 'left'
        ax.text(x, y_start - 0.015, h, fontsize=9.2, fontweight='bold', color='#7F2723', ha=align, va='center', zorder=4)

    # Mid Rule
    mid_y = y_start - 0.042
    ax.plot([0.025, 0.985], [mid_y, mid_y], color='#94A3B8', linewidth=1.5, zorder=3)

    cur_y = mid_y
    for r_idx, row in enumerate(rows):
        cur_y -= row_height
        for col_idx, (x, val) in enumerate(zip(x_pos, row)):
            align = 'center' if col_idx in [2, 3, 5, 6, 7] else 'left'
            weight = 'bold' if col_idx in [0, 6, 7] else 'normal'
            color = '#B91C1C' if col_idx == 6 else ('#1E40AF' if col_idx == 7 else ('#1E293B' if col_idx == 0 else '#334155'))
            font_size = 8.5 if col_idx in [1, 4] else 9.0
            ax.text(x, cur_y + 0.008, val, fontsize=font_size, fontweight=weight, color=color, ha=align, va='center', zorder=4)

        if r_idx < len(rows) - 1:
            ax.plot([0.025, 0.985], [cur_y - 0.015, cur_y - 0.015], color='#F1F5F9', linewidth=0.7, zorder=2)

    # Pre-total divider
    cur_y -= row_height * 0.7
    ax.plot([0.025, 0.985], [cur_y + 0.01, cur_y + 0.01], color='#CBD5E1', linewidth=1.3, zorder=3)

    # Total Row Highlight
    tot_rect = patches.Rectangle(
        (0.025, cur_y - row_height + 0.005), 0.96, row_height,
        facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=1.2, zorder=1
    )
    ax.add_patch(tot_rect)

    cur_y -= row_height * 0.5
    for col_idx, (x, val) in enumerate(zip(x_pos, total_row)):
        align = 'center' if col_idx in [2, 3, 5, 6, 7] else 'left'
        color = '#B91C1C' if col_idx == 6 else ('#1E40AF' if col_idx == 7 else '#1E293B')
        font_size = 8.8 if col_idx in [1, 4] else 9.2
        ax.text(x, cur_y + 0.006, val, fontsize=font_size, fontweight='bold', color=color, ha=align, va='center', zorder=4)

    # Bottom Rule
    bot_y = cur_y - 0.03
    ax.plot([0.025, 0.985], [bot_y, bot_y], color='#7F2723', linewidth=2.8, zorder=3)

    # Note
    note_text = "Note: Tested on 140 provisions. Overall Section Accuracy: 97.86% (137/140). Triage Document Recall: 100.0% (10/10). Cost-Sensitive F2 Score: 1.0000."
    ax.text(0.03, bot_y - 0.035, note_text, fontsize=8.2, color='#64748B', style='italic', va='top')

    plt.tight_layout()
    out1 = OUTPUT_DIR / "slide25_table4_20_stress_test.png"
    out2 = SLIDES_VIZ_DIR / "slide25_table4_20_stress_test.png"
    fig.savefig(out1, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    fig.savefig(out2, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close(fig)
    print(f"Generated {out1} and {out2} successfully!")

if __name__ == "__main__":
    generate_table4_17_card()
    generate_table4_20_card()

