"""
visualize_and_validate.py
=========================
Comprehensive Visualizations and Empirical Validation for Statutory Topic Modeling.

Features:
1. 80/20 Hold-out Train/Test Validation:
   - Evaluates out-of-sample cluster assignment confidence.
   - Measures Silhouette Score & Davies-Bouldin Index.
   - Trains a multi-class classifier on 80% train split and evaluates Out-of-Sample Accuracy,
     Macro F1, Precision, and Recall on the 20% hold-out test set.
   - Verifies explicit statutory pattern consistency.
2. Generates Interactive Plotly & Publication-Ready Matplotlib Visualizations:
   - 01: Macro-Domain Frequency & Corpus Percentage Distribution (Bar chart)
   - 02: Temporal & Historical Legislative Evolution across Eras (Stacked area / timeline)
   - 03: Interactive 2D Semantic Topic Landscape (2D PCA/SVD scatter plot with hover data)
   - 04: Top Salient c-TF-IDF Keywords per Legal Domain (Subplots)
   - 05: Statutory Category Composition (RA vs BP vs CA vs EO vs PD vs Acts breakdown)
"""

import os
import sys
import re
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, f1_score, silhouette_score, davies_bouldin_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

from src.topic_modeler import StatutoryTopicModeler
from src.preprocess import load_corpus


def run_holdout_validation(records: List[Dict[str, Any]], test_size: float = 0.20) -> Dict[str, Any]:
    """
    Executes a rigorous 80/20 train/test hold-out validation to test cluster stability and out-of-sample generalizability.
    """
    print(f"\n========================================================")
    print(f"[*] EXECUTING 80/20 HOLD-OUT EMPIRICAL VALIDATION")
    print(f"========================================================")
    
    docs = [r["searchable_doc"] for r in records]
    
    # 80/20 Train/Test Split
    train_docs, test_docs, train_idx, test_idx = train_test_split(
        docs, np.arange(len(docs)), test_size=test_size, random_state=42
    )
    print(f"Training split: {len(train_docs)} statutes (80%)")
    print(f"Hold-out Test split: {len(test_docs)} statutes (20%)")
    
    # 1. Fit topic model exclusively on Training set
    print(f"\n[Validation Step 1] Fitting topic modeler on Training split...")
    modeler = StatutoryTopicModeler(n_initial_clusters=28, min_corpus_pct=1.0)
    train_topic_ids, train_confidences = modeler.fit_transform(train_docs)
    
    # Extract training embeddings
    train_tfidf = modeler.vectorizer.transform(train_docs)
    train_svd = normalize(modeler.dim_reducer.transform(train_tfidf))
    
    # 2. Project Hold-out Test split into discovered semantic space
    print(f"[Validation Step 2] Projecting Hold-out Test split into discovered space...")
    test_tfidf = modeler.vectorizer.transform(test_docs)
    test_svd = normalize(modeler.dim_reducer.transform(test_tfidf))
    
    test_sims = cosine_similarity(test_svd, modeler.macro_centroids)
    test_topic_ids = np.argmax(test_sims, axis=1)
    
    scaled_test_sims = np.exp(test_sims * 6.0)
    test_confidences = scaled_test_sims[np.arange(len(scaled_test_sims)), test_topic_ids] / np.maximum(scaled_test_sims.sum(axis=1), 1e-9)
    
    mean_test_conf = float(np.mean(test_confidences))
    median_test_conf = float(np.median(test_confidences))
    high_conf_pct = float((test_confidences >= 0.50).mean() * 100.0)
    
    print(f"  -> Out-of-Sample Mean Cosine Confidence: {mean_test_conf * 100:.2f}%")
    print(f"  -> Out-of-Sample Median Confidence: {median_test_conf * 100:.2f}%")
    print(f"  -> Test statutes assigned with >=50% confidence: {high_conf_pct:.1f}%")
    
    # 3. Compute Separation & Compactness Metrics on sample
    sample_size = min(5000, len(test_svd))
    sample_idx = np.random.RandomState(42).choice(len(test_svd), sample_size, replace=False)
    sil_score = float(silhouette_score(test_svd[sample_idx], test_topic_ids[sample_idx], metric="cosine"))
    db_score = float(davies_bouldin_score(test_svd[sample_idx], test_topic_ids[sample_idx]))
    
    print(f"  -> Hold-out Silhouette Score (Cosine): {sil_score:.4f}")
    print(f"  -> Hold-out Davies-Bouldin Index: {db_score:.4f}")
    
    # 4. Supervised Generalization Benchmark
    # Train Logistic Regression on Train SVD representations to evaluate if the clusters are mathematically separable
    print(f"\n[Validation Step 3] Training Supervised Benchmark on discovered cluster labels...")
    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(train_svd, train_topic_ids)
    
    pred_test_ids = clf.predict(test_svd)
    clf_acc = float(accuracy_score(test_topic_ids, pred_test_ids))
    clf_f1 = float(f1_score(test_topic_ids, pred_test_ids, average="macro"))
    
    print(f"  -> Hold-out Classification Consistency Accuracy: {clf_acc * 100:.2f}%")
    print(f"  -> Hold-out Macro F1-Score: {clf_f1 * 100:.2f}%")
    
    # 5. Explicit Statutory Header Consistency Test
    # Test accuracy on laws whose titles have unambiguous statutory indicators
    test_records = [records[i] for i in test_idx]
    pattern_results = []
    
    indicator_tests = [
        ("School / Education", r'\b(?:ELEMENTARY SCHOOL|HIGH SCHOOL|UNIVERSITY|COLLEGE)\b', "Education & Academic Institutions"),
        ("Franchise / Telecom", r'\b(?:FRANCHISE|BROADCASTING|RADIO STATION)\b', "Public Utilities & Telecommunications Franchises"),
        ("Hospital / Bed Capacity", r'\b(?:BED CAPACITY|HOSPITAL|INFIRMARY)\b', "Public Health, Hospitals & Medical Services"),
        ("Barangay / Municipality", r'\b(?:BARANGAY|MUNICIPALITY|BARRIO)\b', "Local Government & Territorial Boundaries"),
        ("Court / Trial", r'\b(?:REGIONAL TRIAL COURT|JUDICIAL|COURT OF FIRST INSTANCE)\b', "Judiciary, Courts & Administration of Justice"),
        ("Tax / Customs", r'\b(?:TARIFF|CUSTOMS CODE|INTERNAL REVENUE|TAX)\b', "Taxation, Tariffs & Revenue Administration")
    ]
    
    print(f"\n[Validation Step 4] Testing Explicit Statutory Pattern Precision:")
    for label_name, regex_pattern, expected_domain in indicator_tests:
        matching_indices = [i for i, r in enumerate(test_records) if re.search(regex_pattern, r["long_title"], re.IGNORECASE)]
        if matching_indices:
            expected_tid = modeler.domain_to_id.get(expected_domain, -1)
            predicted_tids = [test_topic_ids[i] for i in matching_indices]
            correct_count = sum(1 for pid in predicted_tids if pid == expected_tid)
            precision = (correct_count / len(matching_indices)) * 100.0
            pattern_results.append({
                "Pattern": label_name,
                "Sample_Count": len(matching_indices),
                "Expected_Domain": expected_domain,
                "Precision": f"{precision:.1f}%"
            })
            print(f"  - {label_name:24s}: {precision:5.1f}% precision ({correct_count}/{len(matching_indices)} test laws)")

    validation_report = {
        "train_samples": len(train_docs),
        "test_samples": len(test_docs),
        "discovered_macro_domains": len(modeler.macro_metadata),
        "mean_test_cosine_confidence": round(mean_test_conf, 4),
        "median_test_confidence": round(median_test_conf, 4),
        "high_confidence_pct": round(high_conf_pct, 2),
        "holdout_silhouette_score": round(sil_score, 4),
        "holdout_davies_bouldin_score": round(db_score, 4),
        "supervised_benchmark_accuracy": round(clf_acc, 4),
        "supervised_benchmark_macro_f1": round(clf_f1, 4),
        "explicit_pattern_precision": pattern_results
    }
    
    return validation_report


def generate_all_visualizations(
    records: List[Dict[str, Any]],
    modeler: StatutoryTopicModeler,
    output_dir: str = "output/visualizations"
) -> None:
    """Generates all interactive Plotly charts and static PNG figures."""
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n========================================================")
    print(f"[*] GENERATING VISUALIZATIONS IN {output_dir}")
    print(f"========================================================")
    
    # 1. Macro-Domain Distribution Bar Chart
    print(f"[Chart 1/5] Generating Macro-Domain Distribution Bar Chart...")
    topic_counts = []
    for mid in range(len(modeler.macro_metadata)):
        meta = modeler.macro_metadata[mid]
        topic_counts.append({
            "Topic_ID": f"[{mid:02d}] {meta['domain_name']}",
            "Count": meta["doc_count"],
            "Percentage": meta["corpus_percentage"]
        })
    df_dist = pd.DataFrame(topic_counts).sort_values(by="Count", ascending=True)
    
    # Plotly
    fig1 = px.bar(
        df_dist,
        x="Count",
        y="Topic_ID",
        orientation="h",
        text=df_dist["Percentage"].apply(lambda p: f"{p:.1f}%"),
        title="Distribution of Philippine Statutes Across Discovered Legal Domains (N=25,432)",
        labels={"Count": "Number of Enacted Statutes", "Topic_ID": "Legal Domain"},
        color="Count",
        color_continuous_scale="Blues"
    )
    fig1.update_layout(height=600, width=900, template="plotly_white")
    fig1.write_html(os.path.join(output_dir, "01_macro_domain_distribution.html"))
    
    # Matplotlib static
    plt.figure(figsize=(10, 6))
    bars = plt.barh(df_dist["Topic_ID"], df_dist["Count"], color="#1f77b4", edgecolor="black", alpha=0.85)
    for bar, pct in zip(bars, df_dist["Percentage"]):
        plt.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2, f"{pct:.1f}%", va="center", fontsize=9)
    plt.title("Philippine Statutory Corpus: Discovered Legal Domains (>= 1% Threshold)", fontsize=12, fontweight="bold")
    plt.xlabel("Number of Statutes", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "01_macro_domain_distribution.png"), dpi=300)
    plt.close()

    # 2. Historical Temporal Evolution (Era by Era)
    print(f"[Chart 2/5] Generating Historical Temporal Evolution Timeline...")
    era_data = []
    for r in records:
        yr = r.get("year")
        if yr is None or yr < 1900 or yr > 2026:
            continue
        # Bin into historical eras
        if yr < 1935:
            era = "1900-1934: Insular / Early Acts"
        elif yr < 1946:
            era = "1935-1945: Commonwealth Era"
        elif yr < 1972:
            era = "1946-1971: Post-War Republic"
        elif yr < 1986:
            era = "1972-1985: Martial Law / Marcos PDs"
        elif yr < 1991:
            era = "1986-1990: Post-EDSA Transition"
        else:
            era = "1991-2026: Modern / LGC Era"
            
        era_data.append({
            "Era": era,
            "Year": yr,
            "Domain": r.get("topic_label", "Unknown")
        })
    df_era = pd.DataFrame(era_data)
    era_counts = df_era.groupby(["Era", "Domain"]).size().reset_index(name="Statute_Count")
    
    fig2 = px.bar(
        era_counts,
        x="Era",
        y="Statute_Count",
        color="Domain",
        title="Historical Evolution of Philippine Legislation by Era and Legal Domain",
        labels={"Statute_Count": "Statutes Passed", "Era": "Historical Era"},
        barmode="stack",
        template="plotly_white"
    )
    fig2.update_layout(height=650, width=1050)
    fig2.write_html(os.path.join(output_dir, "02_historical_temporal_evolution.html"))
    
    # Matplotlib static version for Chart 2
    pivot_era = df_era.pivot_table(index="Era", columns="Domain", aggfunc="size", fill_value=0)
    pivot_era.plot(kind="bar", stacked=True, figsize=(12, 6), colormap="tab20", edgecolor="black", alpha=0.9)
    plt.title("Historical Evolution of Philippine Legislation Across Eras", fontsize=12, fontweight="bold")
    plt.xlabel("Historical Era", fontsize=10)
    plt.ylabel("Number of Enacted Statutes", fontsize=10)
    plt.xticks(rotation=20, ha="right", fontsize=9)
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "02_historical_temporal_evolution.png"), dpi=300)
    plt.close()

    # 3. 2D Semantic Topic Landscape
    print(f"[Chart 3/5] Generating Interactive 2D Semantic Topic Landscape...")
    docs_sample = [r["searchable_doc"] for r in records]
    tfidf_mat = modeler.vectorizer.transform(docs_sample)
    svd_2d = modeler.dim_reducer.transform(tfidf_mat)[:, :2]  # First 2 components
    
    # Sample 3,500 documents for responsive interactive rendering
    sample_n = min(3500, len(records))
    idx_sample = np.random.RandomState(42).choice(len(records), sample_n, replace=False)
    
    df_scatter = pd.DataFrame({
        "SVD_Dim_1": svd_2d[idx_sample, 0],
        "SVD_Dim_2": svd_2d[idx_sample, 1],
        "Domain": [records[i]["topic_label"] for i in idx_sample],
        "Law_ID": [records[i]["law_id"] for i in idx_sample],
        "Year": [records[i].get("year", "N/A") for i in idx_sample],
        "Title": [records[i]["long_title"][:80] + "..." for i in idx_sample]
    })
    
    fig3 = px.scatter(
        df_scatter,
        x="SVD_Dim_1",
        y="SVD_Dim_2",
        color="Domain",
        hover_data=["Law_ID", "Year", "Title"],
        title="2D Latent Semantic Landscape of Philippine National Statutes (Sample N=3,500)",
        template="plotly_white",
        opacity=0.75
    )
    fig3.update_layout(height=700, width=1050)
    fig3.write_html(os.path.join(output_dir, "03_semantic_topic_landscape_2d.html"))
    
    # Matplotlib static version for Chart 3
    plt.figure(figsize=(11, 7))
    for dom in df_scatter["Domain"].unique():
        sub = df_scatter[df_scatter["Domain"] == dom]
        plt.scatter(sub["SVD_Dim_1"], sub["SVD_Dim_2"], label=dom, alpha=0.6, s=16)
    plt.title("2D Latent Semantic Topic Space (Philippine Statutes)", fontsize=12, fontweight="bold")
    plt.xlabel("Latent Semantic Dimension 1", fontsize=10)
    plt.ylabel("Latent Semantic Dimension 2", fontsize=10)
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "03_semantic_topic_landscape_2d.png"), dpi=300)
    plt.close()
    
    # 4. Top Salient Keywords per Domain
    print(f"[Chart 4/5] Generating c-TF-IDF Top Keywords Subplots...")
    n_domains = len(modeler.macro_metadata)
    cols = 2
    rows = (n_domains + 1) // 2
    
    fig, axes = plt.subplots(rows, cols, figsize=(14, rows * 2.8), sharex=False)
    axes = axes.flatten()
    
    for mid in range(n_domains):
        meta = modeler.macro_metadata[mid]
        kws = meta["keyword_weights"][:6][::-1]
        words = [k[0] for k in kws]
        weights = [k[1] for k in kws]
        
        ax = axes[mid]
        ax.barh(words, weights, color="#2ca02c", alpha=0.85, edgecolor="black")
        ax.set_title(f"[{mid:02d}] {meta['domain_name'][:38]}", fontsize=9, fontweight="bold")
        ax.tick_params(axis='both', which='major', labelsize=8)
        
    for j in range(n_domains, len(axes)):
        fig.delaxes(axes[j])
        
    plt.suptitle("Top c-TF-IDF Salient Keywords by Discovered Legal Domain", fontsize=13, fontweight="bold", y=0.995)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "04_top_keywords_per_domain.png"), dpi=300)
    plt.close()

    # 5. Statute Type Composition (RA, BP, CA, EO, PD, Acts)
    print(f"[Chart 5/5] Generating Statute Type Composition Breakdown...")
    type_data = []
    for r in records:
        type_data.append({
            "Statute_Type": r.get("category", "Other"),
            "Domain": r.get("topic_label", "Unknown")
        })
    df_type = pd.DataFrame(type_data)
    type_counts = df_type.groupby(["Domain", "Statute_Type"]).size().reset_index(name="Count")
    
    fig5 = px.bar(
        type_counts,
        x="Domain",
        y="Count",
        color="Statute_Type",
        title="Statutory Origin Composition per Discovered Legal Domain",
        labels={"Count": "Number of Laws", "Domain": "Discovered Legal Domain"},
        barmode="stack",
        template="plotly_white"
    )
    fig5.update_layout(height=650, width=1100, xaxis_tickangle=-30)
    fig5.write_html(os.path.join(output_dir, "05_statute_type_composition.html"))
    
    # Matplotlib static version for Chart 5
    pivot_type = df_type.pivot_table(index="Domain", columns="Statute_Type", aggfunc="size", fill_value=0)
    pivot_type.plot(kind="bar", stacked=True, figsize=(12, 6), colormap="Set2", edgecolor="black", alpha=0.9)
    plt.title("Statutory Origin Composition per Discovered Legal Domain", fontsize=12, fontweight="bold")
    plt.xlabel("Discovered Legal Domain", fontsize=10)
    plt.ylabel("Number of Laws", fontsize=10)
    plt.xticks(rotation=25, ha="right", fontsize=9)
    plt.legend(title="Statute Type", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "05_statute_type_composition.png"), dpi=300)
    plt.close()
    
    print(f"All 5 interactive HTML and static PNG visualization artifacts successfully saved to {output_dir}!")


if __name__ == "__main__":
    print("=== Running Topic Modeling, Validation, and Visualization Pipeline ===")
    
    # 1. Load Corpus & Fit Consolidated Model
    corpus_records = load_corpus(base_dir=".", include_executive=True)
    docs_all = [r["searchable_doc"] for r in corpus_records]
    
    modeler = StatutoryTopicModeler(n_initial_clusters=28, min_corpus_pct=1.0)
    topic_ids, confidences = modeler.fit_transform(docs_all)
    
    # Assign labels to records
    for idx, r in enumerate(corpus_records):
        t_id = int(topic_ids[idx])
        meta = modeler.macro_metadata[t_id]
        r["topic_id"] = t_id
        r["topic_label"] = meta["domain_name"]
        r["topic_confidence"] = float(round(confidences[idx], 4))
        r["topic_keywords"] = meta["keywords"][:6]
        
    # Save Model & Updated Categorized Corpus
    os.makedirs("output", exist_ok=True)
    modeler.save("output/statutory_topic_model.pkl")
    
    with open("output/categorized_corpus.jsonl", "w", encoding="utf-8") as f:
        for r in corpus_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            
    # Export Summary CSV
    summary_rows = []
    for mid in range(len(modeler.macro_metadata)):
        meta = modeler.macro_metadata[mid]
        summary_rows.append({
            "Topic_ID": mid,
            "Macro_Legal_Domain": meta["domain_name"],
            "Document_Count": meta["doc_count"],
            "Corpus_Pct": f"{meta['corpus_percentage']}%",
            "Top_Salient_Keywords": ", ".join(meta["keywords"][:8])
        })
    pd.DataFrame(summary_rows).to_csv("output/topic_summary.csv", index=False)
    
    # 2. Run 80/20 Hold-out Validation
    val_report = run_holdout_validation(corpus_records, test_size=0.20)
    with open("output/validation_report.json", "w", encoding="utf-8") as f:
        json.dump(val_report, f, indent=2)
    print(f"\n[Export] Validation report saved to output/validation_report.json")
    
    # 3. Generate Visualizations
    generate_all_visualizations(corpus_records, modeler, output_dir="output/visualizations")
