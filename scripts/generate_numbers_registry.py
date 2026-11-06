"""
scripts/generate_numbers_registry.py
====================================
Canonical Single Source of Truth Numbers Registry for BS CS Thesis.

Institution: Ateneo de Davao University, Department of Computer Science
Authors: Ralph Paolo Dulce & Yahyah Odin
Adviser: Mr. Adrian "Ogs" Ablazo | Professor: Ma'am Grace Tacadao

Generates:
1. output/numbers_registry.json (structured JSON data)
2. CS_Undergraduate_Thesis_Template/thesis_numbers.sty (LaTeX macro constants)
"""

import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TEX_DIR = BASE_DIR / "CS_Undergraduate_Thesis_Template"

REGISTRY = {
    "corpus": {
        "total_enactments": 27357,
        "national_statutes": 25432,
        "davao_local_ordinances": 1925,
        "total_searchable_provisions": 178494,
        "operative_provisions": 174107,
        "ordinance_512_token_compliance_pct": 94.75,
    },
    "benchmark": {
        "total_annotation_instances": 350,
        "unique_proposition_pairs": 198,
        "unique_statutory_premises": 22,
        "pairs_per_statutory_premise": 9,
        "class_balance_198": {
            "contradiction": 66,
            "entailment": 66,
            "neutral": 66
        },
        "panel_distribution": {
            "num_panels": 5,
            "pairs_per_panel": 70,
            "overlap_1_panel": 56,
            "overlap_2_panels": 132,
            "overlap_3_panels": 10
        },
        "train_val_test_split": {
            "train": 245,
            "val": 52,
            "test": 53
        }
    },
    "stage1_retrieval": {
        "controlled_candidate_pool": {
            "bm25_recall_at_50": 99.71,
            "hybrid_rrf_recall_at_50": 100.0,
            "hybrid_rrf_recall_at_5": 88.57,
            "hybrid_rrf_recall_at_10": 95.43,
            "hybrid_rrf_recall_at_20": 98.86
        },
        "open_corpus_full_scale": {
            "bm25_recall_at_50": 43.14,
            "dual_stream_recall_at_50": 65.14,
            "dual_stream_mrr": 0.3462,
            "open_corpus_latency_sec": 5.8
        }
    },
    "stage2_cross_encoder_5fold_stratified": {
        "deberta_v3_base_nli": {
            "val_acc": 86.54,
            "test_acc": 86.79,
            "cv_acc_mean": 88.30,
            "cv_acc_sd": 3.44,
            "cv_macro_f1_mean": 0.8800,
            "cv_macro_f1_sd": 0.0371,
            "cv_conflict_f1_mean": 0.9008,
            "cv_conflict_f1_sd": 0.0421
        },
        "pol_bert_large": {
            "val_acc": 84.62,
            "test_acc": 84.91,
            "cv_acc_mean": 86.58,
            "cv_acc_sd": 3.65,
            "cv_macro_f1_mean": 0.8633,
            "cv_macro_f1_sd": 0.0383,
            "cv_conflict_f1_mean": 0.8929,
            "cv_conflict_f1_sd": 0.0538
        },
        "modernbert_base": {
            "val_acc": 82.69,
            "test_acc": 83.02,
            "cv_acc_mean": 84.59,
            "cv_acc_sd": 3.45,
            "cv_macro_f1_mean": 0.8447,
            "cv_macro_f1_sd": 0.0366,
            "cv_conflict_f1_mean": 0.8697,
            "cv_conflict_f1_sd": 0.0439
        },
        "legal_bert_base": {
            "val_acc": 82.69,
            "test_acc": 83.02,
            "cv_acc_mean": 84.30,
            "cv_acc_sd": 3.16,
            "cv_macro_f1_mean": 0.8420,
            "cv_macro_f1_sd": 0.0338,
            "cv_conflict_f1_mean": 0.8658,
            "cv_conflict_f1_sd": 0.0429
        },
        "bert_base_uncased": {
            "val_acc": 82.69,
            "test_acc": 83.02,
            "cv_acc_mean": 84.02,
            "cv_acc_sd": 3.21,
            "cv_macro_f1_mean": 0.8393,
            "cv_macro_f1_sd": 0.0342,
            "cv_conflict_f1_mean": 0.8559,
            "cv_conflict_f1_sd": 0.0299
        },
        "all_minilm_l6_v2": {
            "val_acc": 80.77,
            "test_acc": 81.13,
            "cv_acc_mean": 81.14,
            "cv_acc_sd": 3.99,
            "cv_macro_f1_mean": 0.8099,
            "cv_macro_f1_sd": 0.0420,
            "cv_conflict_f1_mean": 0.8341,
            "cv_conflict_f1_sd": 0.0352
        },
        "zero_shot_baseline": {
            "val_acc": 55.77,
            "test_acc": 56.60,
            "cv_acc_mean": 55.15,
            "cv_acc_sd": 3.52,
            "cv_macro_f1_mean": 0.5435,
            "cv_macro_f1_sd": 0.0385,
            "cv_conflict_f1_mean": 0.4833,
            "cv_conflict_f1_sd": 0.1206
        }
    },
    "stage2_premise_grouped_cv": {
        "deberta_v3_base_nli": {
            "grouped_acc_mean": 86.44,
            "grouped_acc_sd": 6.05,
            "grouped_macro_f1_mean": 0.8617,
            "grouped_macro_f1_sd": 0.0631,
            "grouped_conflict_f1_mean": 0.8945,
            "grouped_conflict_f1_sd": 0.0683
        },
        "pol_bert_large": {
            "grouped_acc_mean": 85.33,
            "grouped_acc_sd": 5.18,
            "grouped_macro_f1_mean": 0.8505,
            "grouped_macro_f1_sd": 0.0546,
            "grouped_conflict_f1_mean": 0.8859,
            "grouped_conflict_f1_sd": 0.0668
        },
        "modernbert_base": {
            "grouped_acc_mean": 84.22,
            "grouped_acc_sd": 4.56,
            "grouped_macro_f1_mean": 0.8400,
            "grouped_macro_f1_sd": 0.0488,
            "grouped_conflict_f1_mean": 0.8703,
            "grouped_conflict_f1_sd": 0.0739
        },
        "legal_bert_base": {
            "grouped_acc_mean": 83.33,
            "grouped_acc_sd": 4.38,
            "grouped_macro_f1_mean": 0.8315,
            "grouped_macro_f1_sd": 0.0462,
            "grouped_conflict_f1_mean": 0.8582,
            "grouped_conflict_f1_sd": 0.0754
        },
        "bert_base_uncased": {
            "grouped_acc_mean": 82.67,
            "grouped_acc_sd": 4.25,
            "grouped_macro_f1_mean": 0.8249,
            "grouped_macro_f1_sd": 0.0453,
            "grouped_conflict_f1_mean": 0.8505,
            "grouped_conflict_f1_sd": 0.0799
        },
        "zero_shot_baseline": {
            "grouped_acc_mean": 54.89,
            "grouped_acc_sd": 7.47,
            "grouped_macro_f1_mean": 0.5434,
            "grouped_macro_f1_sd": 0.0784,
            "grouped_conflict_f1_mean": 0.4644,
            "grouped_conflict_f1_sd": 0.1833
        }
    },
    "statistical_hypothesis_testing": {
        "friedman_test": {
            "chi2_f": 40.0000,
            "df": 5,
            "p_val": 1.49e-7,
            "num_domains": 8
        },
        "mcnemar_tests": {
            "deberta_vs_zero_shot": {
                "cell_b": 18,
                "cell_c": 2,
                "chi2": 11.2500,
                "p_val": 0.0008
            },
            "deberta_vs_bert": {
                "cell_b": 3,
                "cell_c": 1,
                "chi2": 0.2500,
                "p_val": 0.6171,
                "bonferroni_adjusted_alpha": 0.0167
            },
            "deberta_vs_legal_bert": {
                "cell_b": 3,
                "cell_c": 1,
                "chi2": 0.2500,
                "p_val": 0.6171
            }
        },
        "wilcoxon_tests": {
            "deberta_vs_bert": {
                "w_stat": 0.0,
                "p_val": 0.0078,
                "mean_macro_f1_gain": 0.0720,
                "ci_95_lower": 0.0626,
                "ci_95_upper": 0.0815,
                "ci_method": "Students t-interval (df=7)",
                "bonferroni_adjusted_alpha": 0.0167
            },
            "deberta_vs_legal_bert": {
                "w_stat": 0.0,
                "p_val": 0.0078,
                "mean_macro_f1_gain": 0.0540,
                "ci_95_lower": 0.0449,
                "ci_95_upper": 0.0632,
                "ci_method": "Students t-interval (df=7)",
                "bonferroni_adjusted_alpha": 0.0167
            }
        }
    },
    "full_document_audit_latency": {
        "draft_sections": 14,
        "candidate_shortlist_pairs": 105,
        "static_padding_latency_sec": 28.15,
        "static_padding_sd": 0.83,
        "dynamic_padding_latency_sec": 12.69,
        "dynamic_padding_sd": 0.37,
        "speedup_factor": 2.22,
        "latency_reduction_pct": 55.4,
        "per_pair_latency_ms": 120.9,
        "peak_ram_mb": 1416.4,
        "lgu_hardware_ram_cap_mb": 8000
    }
}


def main():
    json_path = OUT_DIR / "numbers_registry.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(REGISTRY, f, indent=2, ensure_ascii=False)
    print(f"[+] Numbers registry JSON written to: {json_path}")

    # Generate LaTeX style definitions
    sty_path = TEX_DIR / "thesis_numbers.sty"
    tex_macros = [
        "% Single Source of Truth Numbers Registry for BS CS Thesis",
        "% Generated automatically by scripts/generate_numbers_registry.py",
        "\\ProvidesPackage{thesis_numbers}",
        "",
        "% Corpus Census",
        f"\\newcommand{{\\CorpusTotalEnactments}}{{{REGISTRY['corpus']['total_enactments']:,}}}",
        f"\\newcommand{{\\CorpusNationalStatutes}}{{{REGISTRY['corpus']['national_statutes']:,}}}",
        f"\\newcommand{{\\CorpusDavaoOrdinances}}{{{REGISTRY['corpus']['davao_local_ordinances']:,}}}",
        f"\\newcommand{{\\CorpusTotalProvisions}}{{{REGISTRY['corpus']['total_searchable_provisions']:,}}}",
        f"\\newcommand{{\\CorpusOperativeProvisions}}{{{REGISTRY['corpus']['operative_provisions']:,}}}",
        "",
        "% Benchmark Sizes",
        f"\\newcommand{{\\BenchmarkTotalPairs}}{{{REGISTRY['benchmark']['total_annotation_instances']}}}",
        f"\\newcommand{{\\BenchmarkUniquePairs}}{{{REGISTRY['benchmark']['unique_proposition_pairs']}}}",
        f"\\newcommand{{\\BenchmarkUniquePremises}}{{{REGISTRY['benchmark']['unique_statutory_premises']}}}",
        "",
        "% Stage 2 Primary Model (DeBERTa-v3-base-NLI)",
        f"\\newcommand{{\\DebertaValAcc}}{{{REGISTRY['stage2_cross_encoder_5fold_stratified']['deberta_v3_base_nli']['val_acc']:.2f}\\%}}",
        f"\\newcommand{{\\DebertaTestAcc}}{{{REGISTRY['stage2_cross_encoder_5fold_stratified']['deberta_v3_base_nli']['test_acc']:.2f}\\%}}",
        f"\\newcommand{{\\DebertaFiveFoldAcc}}{{{REGISTRY['stage2_cross_encoder_5fold_stratified']['deberta_v3_base_nli']['cv_acc_mean']:.2f}\\%}}",
        f"\\newcommand{{\\DebertaFiveFoldMacroFOne}}{{{REGISTRY['stage2_cross_encoder_5fold_stratified']['deberta_v3_base_nli']['cv_macro_f1_mean']:.4f}}}",
        f"\\newcommand{{\\DebertaFiveFoldConflictFOne}}{{{REGISTRY['stage2_cross_encoder_5fold_stratified']['deberta_v3_base_nli']['cv_conflict_f1_mean']:.4f}}}",
        "",
        "% Premise-Grouped CV (Robustness Shield)",
        f"\\newcommand{{\\DebertaGroupedAcc}}{{{REGISTRY['stage2_premise_grouped_cv']['deberta_v3_base_nli']['grouped_acc_mean']:.2f}\\%}}",
        f"\\newcommand{{\\DebertaGroupedMacroFOne}}{{{REGISTRY['stage2_premise_grouped_cv']['deberta_v3_base_nli']['grouped_macro_f1_mean']:.4f}}}",
        f"\\newcommand{{\\DebertaGroupedConflictFOne}}{{{REGISTRY['stage2_premise_grouped_cv']['deberta_v3_base_nli']['grouped_conflict_f1_mean']:.4f}}}",
        "",
        "% Latency & Speedup",
        f"\\newcommand{{\\LatencyStaticPad}}{{{REGISTRY['full_document_audit_latency']['static_padding_latency_sec']:.2f}\\,s}}",
        f"\\newcommand{{\\LatencyDynamicPad}}{{{REGISTRY['full_document_audit_latency']['dynamic_padding_latency_sec']:.2f}\\,s}}",
        f"\\newcommand{{\\SpeedupFactor}}{{{REGISTRY['full_document_audit_latency']['speedup_factor']:.2f}\\times}}",
        f"\\newcommand{{\\LatencyReductionPct}}{{{REGISTRY['full_document_audit_latency']['latency_reduction_pct']:.1f}\\%}}",
        "",
        "% Statistical Significance",
        f"\\newcommand{{\\FriedmanChiSquare}}{{{REGISTRY['statistical_hypothesis_testing']['friedman_test']['chi2_f']:.4f}}}",
        f"\\newcommand{{\\McNemarZeroShotChiSquare}}{{{REGISTRY['statistical_hypothesis_testing']['mcnemar_tests']['deberta_vs_zero_shot']['chi2']:.4f}}}",
        f"\\newcommand{{\\McNemarBertChiSquare}}{{{REGISTRY['statistical_hypothesis_testing']['mcnemar_tests']['deberta_vs_bert']['chi2']:.4f}}}",
    ]

    with open(sty_path, "w", encoding="utf-8") as f:
        f.write("\n".join(tex_macros) + "\n")
    print(f"[+] LaTeX macro definitions written to: {sty_path}")


if __name__ == "__main__":
    main()

