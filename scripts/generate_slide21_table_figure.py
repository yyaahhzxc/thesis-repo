"""
generate_slide21_table_figure.py
================================
Generates a 300 DPI publication-grade graphic of Table 4.1 (OCR Benchmark)
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

def generate_table4_1_card():
    fig = plt.figure(figsize=(13.5, 7.6), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Title Banner
    ax.text(0.04, 0.94, "Table 4.1: Multi-Dimensional Archival Extraction Benchmark",
            fontsize=16, fontweight='bold', color='#7F2723', va='top')
    ax.text(0.04, 0.89, "Comparative Evaluation on Historical Davao City Ordinances Across Accuracy, Entity Fidelity, Privacy, and Cost",
            fontsize=10.5, color='#475569', va='top')

    # Data
    headers = ["Evaluation Metric", "Tesseract v5.x", "Surya v0.6+", "Google Document AI\n(Cloud Commercial)", "Qwen2.5-VL-3B (4-bit NF4)\n(Our Local Edge Model)"]
    rows = [
        ["Architecture Family", "Traditional CNN-LSTM", "Layout-Aware Modular", "Cloud Multimodal Net", "Local Vision-Language"],
        ["Character Error Rate (CER)", "14.82%", "8.45%", "2.15%", "3.12% (Near-Cloud)"],
        ["Word Error Rate (WER)", "22.30%", "12.10%", "4.05%", "5.24%"],
        ["Legal Citation & Entity Acc.", "74.2%", "86.5%", "97.2%", "95.8%"],
        ["Penalty & Monetary Value Acc.", "63.3%", "80.0%", "98.3%", "96.7%"],
        ["Table Structure Fidelity (TEDS)", "41.2%", "76.4%", "94.1%", "91.8%"],
        ["Network Dependency", "100% Offline", "100% Offline", "Mandatory Cloud API", "100% Sovereign Offline"],
        ["Data Privacy (RA 10173)", "Fully Sovereign", "Fully Sovereign", "Third-Party Cloud Route", "Fully Sovereign Edge"],
        ["Operational Cost", "Free Open-Source ($0)", "Free Open-Source ($0)", "Recurring Paywall", "Free Open-Source ($0)"]
    ]

    # Coordinates
    x_positions = [0.04, 0.31, 0.49, 0.68, 0.88] # centers / lefts
    y_start = 0.81
    row_height = 0.075

    # Highlight column for Qwen (column 4)
    qwen_rect = patches.Rectangle(
        (0.775, y_start - len(rows)*row_height - 0.01), 0.205, (len(rows)+1)*row_height + 0.02,
        facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=1.5, zorder=1,
        linestyle='--'
    )
    ax.add_patch(qwen_rect)

    # Top Rule (Booktabs toprule - thick)
    ax.plot([0.03, 0.98], [y_start + 0.02, y_start + 0.02], color='#7F2723', linewidth=2.8, zorder=3)

    # Headers
    for col_idx, (x, h) in enumerate(zip(x_positions, headers)):
        weight = 'bold'
        color = '#1E40AF' if col_idx == 4 else '#7F2723'
        align = 'left' if col_idx == 0 else 'center'
        ax.text(x, y_start - 0.02, h, fontsize=10.5, fontweight=weight, color=color, ha=align, va='center', zorder=4)

    # Mid Rule (Booktabs midrule - medium)
    mid_y = y_start - 0.06
    ax.plot([0.03, 0.98], [mid_y, mid_y], color='#94A3B8', linewidth=1.5, zorder=3)

    # Table Body Rows
    for r_idx, row in enumerate(rows):
        cur_y = mid_y - (r_idx + 0.6) * row_height
        for col_idx, (x, val) in enumerate(zip(x_positions, row)):
            if col_idx == 0:
                ax.text(x, cur_y, val, fontsize=10, fontweight='bold', color='#1E293B', ha='left', va='center', zorder=4)
            elif col_idx == 4:
                # Our model
                ax.text(x, cur_y, val, fontsize=10, fontweight='bold', color='#1E40AF', ha='center', va='center', zorder=4)
            elif col_idx == 3 and ("Paywall" in val or "Third-Party" in val or "Mandatory" in val):
                # Cloud drawback
                ax.text(x, cur_y, val, fontsize=9.5, fontweight='normal', color='#B91C1C', ha='center', va='center', zorder=4)
            else:
                ax.text(x, cur_y, val, fontsize=9.5, fontweight='normal', color='#334155', ha='center', va='center', zorder=4)

        # Subtle row separator line (no vertical lines!)
        if r_idx < len(rows) - 1:
            sep_y = cur_y - 0.5 * row_height
            ax.plot([0.03, 0.98], [sep_y, sep_y], color='#F1F5F9', linewidth=0.8, zorder=2)

    # Bottom Rule (Booktabs bottomrule - thick)
    bot_y = mid_y - len(rows) * row_height
    ax.plot([0.03, 0.98], [bot_y, bot_y], color='#7F2723', linewidth=2.8, zorder=3)

    # Footer note
    note_text = "Note: Evaluated on N = 60 historical enactments. Qwen2.5-VL-3B-Instruct operates offline on Host B (RTX 5050 Laptop GPU) with zero recurring cloud API fees."
    ax.text(0.04, bot_y - 0.04, note_text, fontsize=8.5, color='#64748B', style='italic', va='top')

    plt.tight_layout()
    out1 = OUTPUT_DIR / "slide21_table4_1_ocr_benchmark.png"
    out2 = SLIDES_VIZ_DIR / "slide21_table4_1_ocr_benchmark.png"
    fig.savefig(out1, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    fig.savefig(out2, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close(fig)
    print(f"Generated {out1} and {out2} successfully!")

if __name__ == "__main__":
    generate_table4_1_card()
