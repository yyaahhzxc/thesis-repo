"""
generate_slide22_table4_4_figure.py
===================================
Generates a 300 DPI publication-grade graphic of Table 4.4 (Local Legislative Typology)
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

def generate_table4_4_card():
    fig = plt.figure(figsize=(14.0, 7.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Title Banner
    ax.text(0.04, 0.94, "Table 4.4: Functional Typology of the Davao City Legislative Corpus",
            fontsize=15.5, fontweight='bold', color='#7F2723', va='top')
    ax.text(0.04, 0.89, "Corpus Composition, Statutory Delegated Authority, and Salient c-TF-IDF Keywords (N = 1,925 Enactments, 1950–2025)",
            fontsize=10.0, color='#475569', va='top')

    # Data
    headers = ["ID", "Functional Legislative Typology", "Count", "Share", "Statutory Authority", "Core Salient c-TF-IDF Keywords"]
    rows = [
        ["01", "Substantive Regulatory & Penal", "770", "40.00%", "RA 7160 §458", "public, safety, fine, penal, violation, fee, health, traffic"],
        ["02", "Inter-Agency Agreements (MOA/MOU)", "553", "28.73%", "RA 7160 §§22(c), 455", "pursuant, local, sign, panlungsod, contracts, agreement"],
        ["03", "Disaster Relief & QRF Funds", "199", "10.34%", "RA 10121 §21", "fund, calamity, disaster, risk, reduction, quick response"],
        ["04", "Deeds of Donation & Usufruct", "168", "8.73%", "RA 7160 §22(a)(4)", "donation, local, powers, pursuant, contracts, deed, usufruct"],
        ["05", "Temporary Road Closures", "172", "8.94%", "RA 7160 §21", "road, closure, temporary, vehicular traffic, street, route"],
        ["06", "Zoning & Subdivision Permits", "63", "3.27%", "RA 7160 §20, BP 220", "zoning, zone, land, reclassification, residential, commercial"]
    ]
    total_row = ["Total", "All Digitized Ordinances (1950–2025)", "1,925", "100.00%", "Full Local Corpus", "13,874 Total Extracted Provisions"]

    # Coordinates
    # ID: 0.04, Typology: 0.08, Count: 0.38, Share: 0.46, Authority: 0.55, Keywords: 0.72
    x_positions = [0.045, 0.09, 0.385, 0.465, 0.55, 0.73]
    y_start = 0.81
    row_height = 0.082

    # Top Rule (Booktabs toprule - thick)
    ax.plot([0.03, 0.98], [y_start + 0.02, y_start + 0.02], color='#7F2723', linewidth=2.8, zorder=3)

    # Headers
    for col_idx, (x, h) in enumerate(zip(x_positions, headers)):
        align = 'center' if col_idx in [0, 2, 3] else 'left'
        ax.text(x, y_start - 0.02, h, fontsize=10.0, fontweight='bold', color='#7F2723', ha=align, va='center', zorder=4)

    # Mid Rule (Booktabs midrule - medium)
    mid_y = y_start - 0.055
    ax.plot([0.03, 0.98], [mid_y, mid_y], color='#94A3B8', linewidth=1.5, zorder=3)

    # Highlight Regulatory/Penal (Top Category)
    penal_rect = patches.Rectangle(
        (0.03, mid_y - row_height), 0.95, row_height,
        facecolor='#FEF3C7', edgecolor='none', zorder=1
    )
    ax.add_patch(penal_rect)

    # Table Body Rows
    for r_idx, row in enumerate(rows):
        cur_y = mid_y - (r_idx + 0.55) * row_height
        for col_idx, (x, val) in enumerate(zip(x_positions, row)):
            align = 'center' if col_idx in [0, 2, 3] else 'left'
            weight = 'bold' if (r_idx == 0 and col_idx in [1, 2, 3]) else ('bold' if col_idx in [0, 1] else 'normal')
            color = '#92400E' if (r_idx == 0 and col_idx in [1, 2, 3]) else ('#1E293B' if col_idx in [0, 1] else '#334155')
            font_size = 9.0 if col_idx == 5 else 9.5
            ax.text(x, cur_y, val, fontsize=font_size, fontweight=weight, color=color, ha=align, va='center', zorder=4)

        # Subtle row separator line (no vertical lines!)
        if r_idx < len(rows) - 1:
            sep_y = cur_y - 0.5 * row_height
            ax.plot([0.03, 0.98], [sep_y, sep_y], color='#F1F5F9', linewidth=0.8, zorder=2)

    # Mid-lower Rule before Total
    pre_total_y = mid_y - len(rows) * row_height
    ax.plot([0.03, 0.98], [pre_total_y, pre_total_y], color='#CBD5E1', linewidth=1.2, zorder=3)

    # Total Row
    total_y = pre_total_y - 0.55 * row_height
    for col_idx, (x, val) in enumerate(zip(x_positions, total_row)):
        align = 'center' if col_idx in [0, 2, 3] else 'left'
        ax.text(x, total_y, val, fontsize=9.5, fontweight='bold', color='#7F2723', ha=align, va='center', zorder=4)

    # Bottom Rule (Booktabs bottomrule - thick)
    bot_y = pre_total_y - row_height
    ax.plot([0.03, 0.98], [bot_y, bot_y], color='#7F2723', linewidth=2.8, zorder=3)

    # Footer note
    note_text = "Note: Discovered via BERTopic and Latency-Optimized SVD Topic Space. Typology 01 (Substantive Regulatory & Penal, 40.00%) constitutes the primary target for pre-enactment conflict detection."
    ax.text(0.04, bot_y - 0.04, note_text, fontsize=8.5, color='#64748B', style='italic', va='top')

    plt.tight_layout()
    out1 = OUTPUT_DIR / "slide22_table4_4_local_typology.png"
    out2 = SLIDES_VIZ_DIR / "slide22_table4_4_local_typology.png"
    fig.savefig(out1, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    fig.savefig(out2, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close(fig)
    print(f"Generated {out1} and {out2} successfully!")

if __name__ == "__main__":
    generate_table4_4_card()

