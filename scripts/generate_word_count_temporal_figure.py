"""
generate_word_count_temporal_figure.py
=======================================
Generates publication-ready (300 DPI) LaTeX figure for Chapter 3 (Methodology):
figs/statutory_word_count_temporal_evolution.png

Visualizes the longitudinal word count evolution per enactment alongside annual
legislative volumes across both the Philippine National Statutory Corpus (1900-2026, N = 25,432)
and the Davao City Local Legislative Corpus (1950-2025, N = 1,664).
"""

import os
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec

# Ensure output directories exist
TEMPLATE_FIGS_DIR = Path("CS_Undergraduate_Thesis_Template/figs")
OUTPUT_VIZ_DIR = Path("output/visualizations")
TEMPLATE_FIGS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_VIZ_DIR.mkdir(parents=True, exist_ok=True)

# Set clean, publication-grade academic style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#222222'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#e8e8e8'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.70

def load_data():
    print("Loading National Laws...")
    nat_records = []
    with open("corpus/categorized_national_laws.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            yr = d.get("year")
            if yr and 1900 <= yr <= 2026:
                nat_records.append({
                    "year": yr,
                    "words": d.get("word_count", 0),
                    "category": d.get("category", "")
                })
    df_nat = pd.DataFrame(nat_records)

    print("Loading Local Ordinances...")
    loc_records = []
    with open("corpus/city_ordinances/categorized_davao_ordinances.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            yr = d.get("year")
            if yr and 1950 <= yr <= 2026:
                loc_records.append({
                    "year": yr,
                    "words": d.get("word_count", 0),
                    "typology": d.get("typology", "")
                })
    df_loc = pd.DataFrame(loc_records)
    return df_nat, df_loc

def aggregate_national(df_nat):
    all_years = pd.DataFrame({"year": range(1900, 2026)})
    ann = df_nat.groupby("year").agg(
        count=("words", "count"),
        median=("words", "median"),
        q25=("words", lambda x: x.quantile(0.25)),
        q75=("words", lambda x: x.quantile(0.75)),
        mean=("words", "mean"),
        max=("words", "max")
    ).reset_index()
    m = pd.merge(all_years, ann, on="year", how="left")
    m["count"] = m["count"].fillna(0)
    m["median"] = m["median"].interpolate(method="linear")
    m["q25"] = m["q25"].interpolate(method="linear")
    m["q75"] = m["q75"].interpolate(method="linear")
    m["mean"] = m["mean"].interpolate(method="linear")
    return m

def aggregate_local(df_loc):
    # Only aggregate years where local ordinances actually exist to prevent misleading linear interpolation across multi-year historical gaps
    ann = df_loc.groupby("year").agg(
        count=("words", "count"),
        median=("words", "median"),
        q25=("words", lambda x: x.quantile(0.25)),
        q75=("words", lambda x: x.quantile(0.75)),
        mean=("words", "mean"),
        max=("words", "max")
    ).reset_index()
    
    # Full timeline for volume bars
    all_years = pd.DataFrame({"year": range(1950, 2026)})
    m = pd.merge(all_years, ann, on="year", how="left")
    m["count"] = m["count"].fillna(0)
    return ann, m

def generate_figure(df_nat, df_loc):
    print("Generating refined statutory_word_count_temporal_evolution.png...")
    nat_ann = aggregate_national(df_nat)
    loc_ann_pts, loc_full = aggregate_local(df_loc)

    fig = plt.figure(figsize=(15.8, 5.6), dpi=300)
    gs = GridSpec(1, 2, width_ratios=[1.0, 1.0], wspace=0.30, left=0.06, right=0.93, bottom=0.13, top=0.88)

    # -------------------------------------------------------------
    # Panel (a): National Statutory Corpus (1900-2025)
    # -------------------------------------------------------------
    ax1 = fig.add_subplot(gs[0])
    ax1_vol = ax1.twinx()

    # Background volume bars
    bars1 = ax1_vol.bar(nat_ann["year"], nat_ann["count"], width=0.85, color="#cfd8dc", alpha=0.45,
                        label="Annual Enactments (Volume)")
    ax1_vol.set_ylabel("Annual Enactments Passed", color="#546e7a", fontsize=9.5, fontweight="bold", labelpad=8)
    ax1_vol.tick_params(axis='y', labelcolor="#546e7a", labelsize=8.5)
    ax1_vol.set_ylim(0, 950)
    ax1_vol.grid(False)

    # Foreground lines and ribbon
    line_med = ax1.plot(nat_ann["year"], nat_ann["median"], color="#1565c0", linewidth=2.0,
                        label="Median Word Count")[0]
    line_mean = ax1.plot(nat_ann["year"], nat_ann["mean"], color="#0d47a1", linewidth=1.4,
                         linestyle="--", alpha=0.85, label="Mean Word Count (Omnibus Pull)")[0]
    band1 = ax1.fill_between(nat_ann["year"], nat_ann["q25"], nat_ann["q75"],
                             color="#42a5f5", alpha=0.22, label="Interquartile Range (IQR: P25–P75)")

    # Key historical annotations
    ax1.annotate("Revised Penal Code\n(Act 3815, 1930)", xy=(1930, 2560), xytext=(1938, 3200),
                 arrowprops=dict(facecolor="#263238", arrowstyle="->", lw=0.9),
                 fontsize=8.0, fontweight="bold", color="#263238", ha="center",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffffff", edgecolor="#90a4ae", alpha=0.95))

    ax1.annotate("Local Government Code\n(RA 7160, 1991)", xy=(1991, 2350), xytext=(1985, 2900),
                 arrowprops=dict(facecolor="#263238", arrowstyle="->", lw=0.9),
                 fontsize=8.0, fontweight="bold", color="#263238", ha="center",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffffff", edgecolor="#90a4ae", alpha=0.95))

    ax1.set_title("(a) National Statutory Corpus: Length Evolution (1900–2025, N = 25,432)",
                  fontsize=11.0, fontweight="bold", pad=12, color="#1a1a1a")
    ax1.set_xlabel("Enactment Year", fontsize=9.5, fontweight="bold", labelpad=7)
    ax1.set_ylabel("Raw Words per Statute", fontsize=9.5, fontweight="bold", labelpad=7, color="#1565c0")
    ax1.tick_params(axis='y', labelcolor="#1565c0", labelsize=8.5)
    ax1.tick_params(axis='x', labelsize=8.5)
    ax1.set_xlim(1898, 2027)
    ax1.set_ylim(0, 4600)
    ax1.grid(True, linestyle="--", alpha=0.55)

    # Combined legend
    lines1 = [line_med, line_mean, band1, bars1]
    labels1 = [l.get_label() for l in lines1]
    ax1.legend(lines1, labels1, loc="upper left", fontsize=7.8, framealpha=0.94, facecolor="#ffffff")

    # -------------------------------------------------------------
    # Panel (b): Davao City Local Legislative Corpus (1950-2025)
    # -------------------------------------------------------------
    ax2 = fig.add_subplot(gs[1])
    ax2_vol = ax2.twinx()

    # Background volume bars across the full timeline
    bars2 = ax2_vol.bar(loc_full["year"], loc_full["count"], width=0.85, color="#ffccbc", alpha=0.45,
                        label="Annual Ordinances (Volume)")
    ax2_vol.set_ylabel("Annual Ordinances Enacted", color="#d84315", fontsize=9.5, fontweight="bold", labelpad=8)
    ax2_vol.tick_params(axis='y', labelcolor="#d84315", labelsize=8.5)
    ax2_vol.set_ylim(0, 460)
    ax2_vol.grid(False)

    # For local enactments, connect years with active enactments using line + markers
    line_med2 = ax2.plot(loc_ann_pts["year"], loc_ann_pts["median"], color="#d84315", linewidth=1.9,
                         marker='o', markersize=3.2, label="Median Word Count")[0]
    line_mean2 = ax2.plot(loc_ann_pts["year"], loc_ann_pts["mean"], color="#bf360c", linewidth=1.4,
                          linestyle="--", marker='s', markersize=2.8, alpha=0.85, label="Mean Word Count (Omnibus Pull)")[0]
    band2 = ax2.fill_between(loc_ann_pts["year"], loc_ann_pts["q25"], loc_ann_pts["q75"],
                             color="#ff7043", alpha=0.20, label="Interquartile Range (IQR: P25–P75)")

    # Key local annotations
    ax2.annotate("Comprehensive Zoning &\nRevenue Landmark Codes", xy=(1998, 4800), xytext=(1970, 6800),
                 arrowprops=dict(facecolor="#263238", arrowstyle="->", lw=0.9),
                 fontsize=8.0, fontweight="bold", color="#263238", ha="center",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffffff", edgecolor="#ffab91", alpha=0.95))

    ax2.annotate("LISSP Electronic Census Era\n(250–365 Enactments/Yr;\nMedian ~850–930 Words)",
                 xy=(2022, 1100), xytext=(2004, 3800),
                 arrowprops=dict(facecolor="#263238", arrowstyle="->", lw=0.9),
                 fontsize=8.0, fontweight="bold", color="#263238", ha="center",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffffff", edgecolor="#ffab91", alpha=0.95))

    ax2.set_title("(b) Davao City Local Corpus: Length Evolution (1950–2025, N = 1,664)",
                  fontsize=11.0, fontweight="bold", pad=12, color="#1a1a1a")
    ax2.set_xlabel("Enactment Year", fontsize=9.5, fontweight="bold", labelpad=7)
    ax2.set_ylabel("Raw Words per Ordinance", fontsize=9.5, fontweight="bold", labelpad=7, color="#d84315")
    ax2.tick_params(axis='y', labelcolor="#d84315", labelsize=8.5)
    ax2.tick_params(axis='x', labelsize=8.5)
    ax2.set_xlim(1948, 2027)
    ax2.set_ylim(0, 8500)
    ax2.grid(True, linestyle="--", alpha=0.55)

    # Combined legend (placed in upper right where space is open)
    lines2 = [line_med2, line_mean2, band2, bars2]
    labels2 = [l.get_label() for l in lines2]
    ax2.legend(lines2, labels2, loc="upper right", fontsize=7.8, framealpha=0.94, facecolor="#ffffff")

    # Save outputs
    out_fig = TEMPLATE_FIGS_DIR / "statutory_word_count_temporal_evolution.png"
    out_viz = OUTPUT_VIZ_DIR / "statutory_word_count_temporal_evolution.png"
    plt.savefig(out_fig, dpi=300, bbox_inches="tight")
    plt.savefig(out_viz, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[DONE] Saved to {out_fig} and {out_viz}")

if __name__ == "__main__":
    df_nat, df_loc = load_data()
    generate_figure(df_nat, df_loc)
