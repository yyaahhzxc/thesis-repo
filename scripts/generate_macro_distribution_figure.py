import os
import matplotlib.pyplot as plt
import pandas as pd

# Define the 8 consolidated macro domains matching Table 3.2 and statutory_topic_model.pkl
domains = [
    {"id": "00", "name": "Executive Issuances & Policy Reorganization", "count": 12210, "pct": 48.01},
    {"id": "01", "name": "Education & Academic Institutions", "count": 3492, "pct": 13.73},
    {"id": "02", "name": "Local Government & Territorial Boundaries", "count": 2134, "pct": 8.39},
    {"id": "03", "name": "Public Utilities & Telecom Franchises", "count": 2041, "pct": 8.03},
    {"id": "04", "name": "Public Health, Hospitals & Medical Services", "count": 1890, "pct": 7.43},
    {"id": "05", "name": "Statutory Codes & General Legal Amendments", "count": 1873, "pct": 7.36},
    {"id": "06", "name": "Public Finance & General Appropriations", "count": 1335, "pct": 5.25},
    {"id": "07", "name": "Taxation, Tariffs & Revenue Administration", "count": 457, "pct": 1.80},
]

# For horizontal bar chart, order ascending from bottom to top so largest is at the top
df = pd.DataFrame(domains).iloc[::-1].reset_index(drop=True)
df["label"] = df.apply(lambda r: f"[{r['id']}] {r['name']}", axis=1)

# Style configuration
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

fig, ax = plt.subplots(figsize=(10.5, 5.5), dpi=300)

# Create bars
bars = ax.barh(df["label"], df["count"], color="#2b7bba", edgecolor="#1a4c73", height=0.68, alpha=0.9)

# Set x-axis limits with ample headroom so text never touches or crosses the right border
ax.set_xlim(0, 14500)
ax.set_xlabel("Number of Enacted Statutes", fontsize=10.5, fontweight="bold", labelpad=8)
ax.set_title("Philippine Statutory Corpus: Discovered Legal Domains (≥ 1.0% Threshold)", fontsize=12, fontweight="bold", pad=12)

# Grid lines
ax.xaxis.grid(True, linestyle="--", alpha=0.5, color="#cccccc")
ax.set_axisbelow(True)

# Add data labels
for bar, count, pct in zip(bars, df["count"], df["pct"]):
    width = bar.get_width()
    # Format label with percentage and statute count
    label_text = f"{pct:.1f}% ({count:,})"
    ax.text(
        width + 180,
        bar.get_y() + bar.get_height() / 2,
        label_text,
        va="center",
        ha="left",
        fontsize=9,
        fontweight="medium",
        color="#222222"
    )

# Formatting ticks
ax.tick_params(axis='both', which='major', labelsize=9.5)
ax.tick_params(axis='y', length=0)

plt.tight_layout()

# Save to output directory and to thesis template figs directory
output_paths = [
    "output/visualizations/01_macro_domain_distribution.png",
    "CS_Undergraduate_Thesis_Template/figs/macro_domain_distribution.png"
]

for p in output_paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    fig.savefig(p, dpi=300, bbox_inches="tight")
    print(f"Saved: {p}")

plt.close()
