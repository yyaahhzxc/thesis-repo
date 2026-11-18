"""
scripts/generate_feature_importance_figure.py
=============================================
Generates publication-quality Figure 4.4 for Chapter 4:
Panel A: Component Ablation Delta F1 Bar Chart (Feature Importance)
Panel B: Cross-Encoder Token Attention Saliency Heatmap on Authentic Conflict Pair
"""

import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = next((p for p in Path(__file__).resolve().parents if (p / ".git").exists() or (p / "README.md").exists()), Path(__file__).resolve().parents[2])
FIG_DIR = BASE_DIR / "CS_Undergraduate_Thesis_Template" / "figs"
FIG_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = FIG_DIR / "feature_importance_attention_saliency.png"

# Publication styling
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.titlesize": 12,
    "text.usetex": False
})

fig = plt.figure(figsize=(10.5, 9.2), dpi=300)
# Panel A: y-tick labels take 0.03 to 0.26, bars take 0.27 to 0.97
ax1 = fig.add_axes([0.27, 0.60, 0.70, 0.34])
# Panel B: spans full width from 0.03 to 0.97 matching Panel A
ax2 = fig.add_axes([0.03, 0.04, 0.94, 0.42])

# ---------------------------------------------------------------------------
# Panel A: Component Ablation (Feature Importance Delta F1)
# ---------------------------------------------------------------------------
components = [
    "Full Pipeline Architecture\n(DeBERTa-v3 + RRF + Meta + Fine Rule)",
    "w/o Structural Prepending\n(Raw Unanchored Text)",
    "w/o Lexical BM25\n(Dense Vectors Only)",
    "w/o Symbolic Fine Rule\n(RA 7160 §458 Ceiling)",
    "w/o NLI Pre-Alignment\n(Cold MLM deberta-v3)",
    "w/o Task Fine-Tuning\n(Zero-Shot Baseline)"
]
deltas = [0.0, -6.52, -1.95, -0.97, -2.58, -39.70]
colors = ["#2b5c8f", "#d95f02", "#7570b3", "#e7298a", "#e6ab02", "#a6761d"]

y_pos = np.arange(len(components))[::-1]
bars = ax1.barh(y_pos, [abs(d) for d in deltas], color=colors, height=0.62, edgecolor="black", linewidth=0.8)

# Label values
for idx, (b, d) in enumerate(zip(bars, deltas)):
    w = b.get_width()
    if d == 0.0:
        ax1.text(w + 0.8, b.get_y() + b.get_height()/2, "Reference Pipeline (F1 = 0.8803)", 
                 va="center", ha="left", fontsize=8.5, fontweight="bold", color="#2b5c8f")
    else:
        ax1.text(w + 0.8, b.get_y() + b.get_height()/2, f"-{abs(d):.2f}% Delta F1", 
                 va="center", ha="left", fontsize=8.5, fontweight="bold", color="#333333")

ax1.set_yticks(y_pos)
ax1.set_yticklabels(components, fontsize=8.5)
ax1.set_xlabel("Absolute Performance Degradation on Conflict F1-Score (%)", fontweight="bold", labelpad=8)
ax1.set_title("(A) Pipeline Component & Feature Ablation", fontweight="bold", pad=10)
ax1.set_xlim(0, 46)
ax1.grid(axis="x", linestyle="--", alpha=0.5)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# ---------------------------------------------------------------------------
# Panel B: Cross-Encoder Token Attention Saliency Heatmap
# ---------------------------------------------------------------------------
tokens = [
    "[CLS]", "Section", "3", ".", "Aerial", "spraying", "of", "agricultural", "chemicals", 
    "is", "strictly", "prohibited", "[SEP]", 
    "FPA", "shall", "have", "exclusive", "jurisdiction", "to", "regulate", "and", "license", "[SEP]"
]
weights = [
    0.05, 0.08, 0.06, 0.02, 0.65, 0.72, 0.12, 0.38, 0.45, 
    0.15, 0.88, 0.98, 0.10, 
    0.82, 0.25, 0.20, 0.94, 0.91, 0.18, 0.78, 0.15, 0.70, 0.10
]

ax2.set_xlim(0, 100)
ax2.set_ylim(0, 100)
ax2.axis("off")
ax2.set_title(r"(B) Sample Cross-Encoder Token Attention Map (Mosqueda v. PBGEA)", fontweight="bold", pad=12)

# Outer card container for Panel B
card = patches.FancyBboxPatch((0.5, 1.0), 99.0, 96.0, boxstyle="round,pad=1.0",
                              facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1.0)
ax2.add_patch(card)

ax2.text(2.5, 91, "Draft Ordinance Hypothesis (Davao City Ordinance No. 0309-07 §3):", fontsize=9.5, fontweight="bold", color="#1a365d")

# Render hypothesis tokens
x_start = 2.5
y_start = 81
for t, w in zip(tokens[1:12], weights[1:12]):
    bg_color = plt.cm.YlOrRd(w * 0.85 + 0.1)
    t_len = len(t) * 1.55 + 3.2
    if x_start + t_len > 98:
        x_start = 2.5
        y_start -= 10
    rect = patches.FancyBboxPatch((x_start, y_start - 2.5), t_len, 7.0, boxstyle="round,pad=0.5", 
                                  facecolor=bg_color, edgecolor="#666666", linewidth=0.6)
    ax2.add_patch(rect)
    text_color = "white" if w > 0.75 else "black"
    ax2.text(x_start + t_len/2, y_start + 1.0, t, ha="center", va="center", fontsize=9.0, 
             fontweight="bold" if w > 0.6 else "normal", color=text_color)
    x_start += t_len + 1.2

ax2.text(2.5, 56, "Statutory Premise (Presidential Decree No. 1144 §6):", fontsize=9.5, fontweight="bold", color="#1a365d")

# Render premise tokens
x_start = 2.5
y_start = 46
for t, w in zip(tokens[13:], weights[13:]):
    bg_color = plt.cm.YlOrRd(w * 0.85 + 0.1)
    t_len = len(t) * 1.55 + 3.2
    if x_start + t_len > 98:
        x_start = 2.5
        y_start -= 10
    rect = patches.FancyBboxPatch((x_start, y_start - 2.5), t_len, 7.0, boxstyle="round,pad=0.5", 
                                  facecolor=bg_color, edgecolor="#666666", linewidth=0.6)
    ax2.add_patch(rect)
    text_color = "white" if w > 0.75 else "black"
    ax2.text(x_start + t_len/2, y_start + 1.0, t, ha="center", va="center", fontsize=9.0, 
             fontweight="bold" if w > 0.6 else "normal", color=text_color)
    x_start += t_len + 1.2

# Color scheme legend bar at bottom of Panel B card
ax2.text(2.5, 19.5, "Normalized Cross-Attention Weight Legend (YlOrRd Scale):", fontsize=9.0, fontweight="bold", color="#1e293b")
bar_x0, bar_w, bar_y, bar_h = 2.5, 56.0, 10.5, 5.2
n_steps = 80
step_w = bar_w / n_steps
for i in range(n_steps):
    w_val = i / (n_steps - 1)
    c_val = plt.cm.YlOrRd(w_val * 0.85 + 0.1)
    ax2.add_patch(patches.Rectangle((bar_x0 + i * step_w, bar_y), step_w + 0.1, bar_h,
                                    facecolor=c_val, edgecolor="none"))
ax2.add_patch(patches.Rectangle((bar_x0, bar_y), bar_w, bar_h, facecolor="none", edgecolor="#475569", linewidth=0.8))
for tick_w, tick_lbl in [(0.0, "0.0 (Low)"), (0.25, "0.25"), (0.5, "0.50"), (0.75, "0.75"), (1.0, "1.0 (High)")]:
    tx = bar_x0 + tick_w * bar_w
    ax2.plot([tx, tx], [bar_y - 1.2, bar_y], color="#475569", linewidth=0.8)
    ax2.text(tx, bar_y - 2.4, tick_lbl, ha="center", va="top", fontsize=8.0, color="#334155")

plt.savefig(OUT_PATH, dpi=300, bbox_inches="tight")
print(f"Successfully generated Figure 4.4 to {OUT_PATH}")
