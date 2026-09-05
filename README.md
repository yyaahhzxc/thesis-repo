# A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances

[![Institution: Ateneo de Davao University](https://img.shields.io/badge/Institution-Ateneo%20de%20Davao%20University-003366.svg)](https://www.addu.edu.ph/)
[![Department: Computer Science](https://img.shields.io/badge/Department-Computer%20Science-blue.svg)]()
[![Degree: BS Computer Science Thesis](https://img.shields.io/badge/Thesis-Undergraduate%20Research-green.svg)]()
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)]()
[![LaTeX: TeX Live / MiKTeX](https://img.shields.io/badge/LaTeX-97%20Pages%20%7C%200%20Errors-blue.svg)]()
[![Benchmark: 350 Pairs](https://img.shields.io/badge/Benchmark-350%20Pairs%20%7C%208%20Domains-orange.svg)]()

**Undergraduate Thesis Project (April 2026)**  
**Authors**: Ralph Paolo Dulce & Yahyah Odin  
**Adviser**: Mr. Adrian "Ogs" Ablazo  
**Institution**: School of Arts and Sciences, Ateneo de Davao University, Davao City, Philippines  

---

## ⚡ Quick Start: One-Click Automated Setup

If you are cloning this repository on a new machine, setting up for review, or testing in VS Code / Cursor:

### Step 1: Run the Automated Setup Script
Run the turnkey PowerShell setup script in the repository root:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_environment.ps1
```
This script automatically:
1. Detects your LaTeX compiler (`pdflatex`); if missing, initiates automated installation of **MiKTeX** via `winget`.
2. Creates and activates the Python virtual environment (`venv`).
3. Installs all required Python dependencies from [`requirements.txt`](file:///c:/Users/SHRIMP/Documents/thesis-repo/requirements.txt).
4. Verifies the end-to-end multi-pass LaTeX thesis build.

> [!IMPORTANT]
> **Manual VS Code Extension Requirement (`James-Yu.latex-workshop`)**:  
> The setup script attempts to install the LaTeX Workshop extension via `code --install-extension James-Yu.latex-workshop`. However, if the `code` CLI is not in your system `PATH` (common default Windows VS Code installs) or if you are using **Cursor** / **VSCodium**, the extension cannot be installed from the command line.  
> **You must install it manually:**
> 1. Open VS Code or Cursor and press **`Ctrl + Shift + X`** (Extensions Marketplace).
> 2. Search for **`LaTeX Workshop`** (by **James Yu** / ID: `James-Yu.latex-workshop`).
> 3. Click **Install**.
> 4. Restart VS Code/Cursor if prompted to ensure the `pdflatex` path is loaded.

---

## Overview

This repository houses the end-to-end research codebase, empirical evaluation suites, statutory datasets, and LaTeX manuscript for the thesis titled:  
**"A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference."**

The system operationalizes the **Magtajas v. Pryce Doctrine** by automatically auditing proposed municipal ordinances against the corpus of Philippine national laws before formal enactment (*ex-ante*). The architecture employs a two-stage paradigm:
1. **Stage 1 (Coarse Retrieval)**: Hybrid Sparse Lexical (BM25) + Dense Bi-Encoder (`all-mpnet-base-v2` / `BGE-M3`) retrieval over 25,432 national statutes.
2. **Stage 2 (Fine Natural Language Inference)**: Asymmetric Span-Level NLI Cross-Encoder (`ModernBERT` / `DeBERTa-v3`) with temperature-calibrated softmax classification and intrinsic self-attention Explainable AI (XAI).

```mermaid
flowchart LR
    A[Proposed Draft Ordinance] --> B[Stage 1: Coarse IR\nBM25 + Dense Bi-Encoder]
    B --> C[Top-k Candidate Statutes\nFiltered Search Space]
    C --> D[Stage 2: Fine NLI Cross-Encoder\nAsymmetric Span Pairing]
    D --> E[Calibrated Conflict Probabilities\nEntailment | Neutral | Contradiction]
    E --> F[Intrinsic Attention XAI Heatmap\nGranular Legal Explanations]
```

---

## Repository Layout

```
thesis-repo/
├── CS_Undergraduate_Thesis_Template/  <-- Full LaTeX Thesis Manuscript Source (97 pages)
│   ├── main.tex                       <-- Root LaTeX document
│   ├── references.bib                 <-- BibTeX literature database
│   ├── chapters/                      <-- Thesis chapters
│   │   ├── introduction.tex           <-- Chapter 1
│   │   ├── literature_review.tex      <-- Chapter 2
│   │   ├── theoretical-framework.tex  <-- Theoretical Framework
│   │   └── methodology.tex            <-- Chapter 3 (Refined, simplified headers)
│   ├── figs/                          <-- Publication diagrams, charts, and figures
│   │   ├── statute_type_composition.png
│   │   ├── historical_temporal_evolution.png
│   │   └── macro_domain_distribution.png
│   └── .vscode/settings.json          <-- Instant live-preview configuration
│
├── data/                              <-- Evaluation Benchmark & Partitioning
│   ├── ground_truth_350_review.xlsx   <-- Master 4-sheet evaluation & review workbook
│   ├── ground_truth_350.jsonl         <-- Complete 350-pair benchmark dataset (JSONL)
│   ├── ground_truth_350.csv           <-- Complete 350-pair benchmark dataset (CSV)
│   ├── blocks/                        <-- Pre-split blocks for annotator panels
│   │   ├── block_1.csv                <-- Set A (70 pairs)
│   │   ├── block_2.csv                <-- Set B (70 pairs)
│   │   ├── block_3.csv                <-- Set C (70 pairs)
│   │   ├── block_4.csv                <-- Set D (70 pairs)
│   │   └── block_5.csv                <-- Set E (70 pairs)
│   ├── verbatim_statutory_sections.json <-- Extracted Lawphil statute texts
│   └── corpus_statute_premises.json   <-- Exact statutory premises from corpus
│
├── docs/                              <-- Institutional Documentation & Instruments
│   └── annotation/
│       ├── sp_annotation_cheat_sheet.md           <-- Quick-reference rubric for SP evaluators
│       └── adviser_endorsement_letter_template.md <-- Formal endorsement request letter
│
├── corpus/                            <-- Statutory Data (Git-Ignored / Local Storage)
│   ├── categorized_national_laws.jsonl <-- Master 25,432 cleaned national laws (194 MB)
│   ├── national_laws/                 <-- Raw JSONL files (RA, BP, CA, EO, PD, Acts)
│   └── city_ordinances/               <-- Scanned municipal PDF ordinances (2021-2025)
│
├── src/                               <-- Core Python Engine
│   ├── preprocess.py                  <-- Text normalization, HTML unescaping & parsing
│   ├── topic_modeler.py               <-- Unsupervised SVD + KMeans topic discovery engine
│   ├── categorize_query.py            <-- Interactive CLI statute & draft query tool
│   ├── visualize_and_validate.py      <-- 80/20 train/test holdout validation & plotting
│   └── scraper/                       <-- Lawphil statutory scraper suite
│       ├── lawphil_scraper.py         <-- Resilient scraper with rate-limiting
│       └── file_map_config.json       <-- Statute URL index mappings
│
├── scripts/                           <-- Automated Helper & Benchmark Scripts
│   ├── setup_environment.ps1          <-- One-click automated setup for Windows
│   ├── build_paper.py                 <-- LaTeX PDF compiler (supports --fast flag)
│   ├── export_ground_truth_excel.py   <-- Builds the master 4-sheet review workbook
│   ├── generate_ground_truth_dataset.py <-- Compiles the 350-pair stratified benchmark
│   ├── validate_ground_truth.py       <-- Validates citation integrity and balance
│   └── compare_ocr_experiments.py     <-- Empirical OCR vs. VLM benchmark suite
│
├── output/                            <-- Generated Summaries & Evaluation Artifacts
│   ├── topic_summary.csv              <-- 11 Macro Legal Domains summary
│   ├── validation_report.json         <-- Empirical 80/20 holdout metrics
│   ├── ocr_experiment_report.json     <-- OCR vs. VLM benchmark metrics
│   └── visualizations/                <-- 12 publication PNGs and interactive HTML charts
│
├── OCR_EXPERIMENT_DRAFT.md            <-- Research draft on OCR vs VLM municipal parsing
├── requirements.txt                   <-- Python dependency specifications
└── .gitignore                         <-- Excludes heavy corpus and LaTeX cache files
```

---

## 📊 Ground Truth Benchmark Dataset (350 Pairs)

To evaluate the coarse-to-fine pipeline, we constructed a representative, stratified ground truth benchmark of **350 premise-hypothesis pairs** based on actual Philippine national statutes and realistic Davao City legislative draft ordinances.

### 1. Difficulty Tier Stratification
The benchmark exercises Stage 1 and Stage 2 across three distinct operational challenges:
* **Tier 1: Lexical-Syntactic Surface Direct (30%)**: Direct lexical overlap and explicit statutory thresholds (e.g., penalty ceilings under RA 7160 Section 458, verbatim mandatory structural elements).
* **Tier 2: Definitional & Structural Operational (40%)**: Conflicting administrative jurisdictions, operational standards, definitions, and zoning/franchising criteria without direct word-for-word phrasing.
* **Tier 3: Asymmetric Domain Nuance & Qualitative Overreach (30%)**: Substantive legal conflicts involving *ultra vires* regulatory overreach, constitutional preemption doctrines, field preemption (e.g., national energy/telecom regulation), and implicit statutory exemptions.

### 2. Macro Domain Coverage
The 350 pairs are balanced across 8 core local government functional domains:
1. **Public Order, Safety, & Police Powers** (e.g., curfew, traffic penalties, surveillance)
2. **Local Taxation, Revenue, & Fiscal Measures** (e.g., local business taxes, franchise fees)
3. **Zoning, Land Use, & Real Property** (e.g., comprehensive land use, building heights, easements)
4. **Environmental Management & Sanitation** (e.g., solid waste management, single-use plastics)
5. **Trade, Commerce, & Economic Enterprises** (e.g., market stall leasing, price freeze compliance)
6. **Public Health, Sanitation, & Regulated Substances** (e.g., anti-smoking, vaping, health permits)
7. **Social Welfare & Protected Demographics** (e.g., senior citizen discounts, PWD accessibility)
8. **Administrative & Civil Service** (e.g., LGU personnel discipline, local appointments)

### 3. Master Review Workbook (`data/ground_truth_350_review.xlsx`)
A master Excel workbook formatted with professional headers, auto-filter, and column widths is available for adviser review:
* **Sheet 1 (`Codebook & Instructions`)**: Complete NLI classification rubric (Entailment, Contradiction, Neutral) and evaluator guidelines.
* **Sheet 2 (`All 350 Benchmark Pairs`)**: Full benchmark dataset featuring verbatim national law premises extracted directly from corpus text, realistic Davao City ordinance hypotheses, verified citations, and consolidated evaluation set designations (`Set A` to `Set E`).
* **Sheet 3 (`Domain Summaries`)**: High-level statistical summaries across all 8 domains and 3 difficulty tiers.
* **Sheet 4 (`Panel & Annotator Assignments`)**:
  * **Table 1: Evaluation Set & Sub-Panel Allocation**: Clean 5-set division (`Set A` to `Set E`, 70 pairs each).
  * **Table 2: Annotator Directory**: 15 Sangguniang Panlungsod legal researchers divided into 5 independent trios (Panels A–E). Each panel contains **1 Senior Lead Annotator ($\ge 5$ years legislative tenure)** and **2 Associate Annotators**, selected via purposive availability sampling across the 48-member pool (no artificial district quotas, reflecting city-wide ordinance scope).
  * **Table 3: Google Forms Conditional Branching Blueprint**: Step-by-step implementation guide for deploying a single master Google Form using Section 1 dropdown branching (`Go to section based on answer`) with direct form submissions, collecting 1,050 total judgment data points across 15 submissions.

---

## 📝 Thesis Paper Drafting (Overleaf-Style Local Setup)

The LaTeX source code for the 97-page thesis manuscript is located in `CS_Undergraduate_Thesis_Template/`. The setup runs completely offline in VS Code / Cursor with identical live-preview ergonomics.

### How We Replicate the Overleaf Experience Locally

| Action | Shortcut / Command | What Happens |
| :--- | :--- | :--- |
| **Open Side-by-Side PDF** | **`Ctrl + Alt + V`** | Opens the compiled PDF directly in an editor tab. Snap it to the right half for split-screen view. |
| **Instant Recompile** | **`Ctrl + S`** (Save) | Triggers the fast 1-second single-pass `pdflatex` build and reloads the preview tab automatically. |
| **Jump Code $\rightarrow$ PDF** | **`Ctrl + Alt + J`** <br>*(or `Ctrl + Alt + Click`)* | Jumps the PDF preview directly to the paragraph your cursor is currently on. |
| **Jump PDF $\rightarrow$ Code** | **`Ctrl + Left Click`** on PDF | Clicks any text in the PDF tab to jump straight to that line in your `.tex` source code. |
| **Fast CLI Build** | `python scripts/build_paper.py --fast` | Fast single-pass build for quick proofreading. |
| **Full 4-Pass Build** | `python scripts/build_paper.py` | Complete build (`pdflatex -> bibtex -> pdflatex*2`) to refresh citations, TOC, and references. |

### Chapter 3 Methodology Updates
The methodology chapter ([`CS_Undergraduate_Thesis_Template/chapters/methodology.tex`](file:///c:/Users/SHRIMP/Documents/thesis-repo/CS_Undergraduate_Thesis_Template/chapters/methodology.tex)) has been extensively updated:
1. **Simplified Section Headers**: Replaced verbose headings with concise 2–3 word titles matching the style of Chapters 1 and 2 (e.g., *Benchmark Construction*, *Workload Allocation*, *Annotator Selection*, *Inter-Rater Reliability*).
2. **Workload Mathematics**: Formalized the evaluation partition ($N=350$ pairs, $K=3$ independent raters per item, $R=70$ items per annotator, $A=15$ total legal annotators, yielding 1,050 total judgment data points).
3. **Statistical Power Analysis**: Added Cohen's statistical power analysis ($w=0.30$, $\alpha=0.05$, $df=28$, $N=1,050$, power $> 0.999$) establishing statistical rigor.
4. **Annotator Qualifications & Purposive Sampling**: Formalized the Senior Lead Annotator qualification metric ($\ge 5$ years legislative tenure) and purposive availability sampling across the 48-member pool without artificial district quotas.
5. **Compilation Status**: **97 pages, 0 LaTeX errors**, compiled directly to [`CS_Undergraduate_Thesis_Template/main.pdf`](file:///c:/Users/SHRIMP/Documents/thesis-repo/CS_Undergraduate_Thesis_Template/main.pdf).

---

## 🛠️ Core Pipelines & Execution Guide

### 1. Statutory Topic Modeling & Corpus Consolidation
Processes the 25,432 national laws, normalizes legislative templates, and categorizes them into **11 Consolidated Macro Legal Domains** ($\ge 1.0\%$ corpus threshold):
```powershell
python src/topic_modeler.py
```
*Outputs:* `output/statutory_topic_model.pkl`, `output/topic_summary.csv`, and `corpus/categorized_national_laws.jsonl`.

### 2. Empirical Holdout Validation (80/20 Train/Test Split) & Visualizations
Runs out-of-sample topic projection, measures cosine confidence, computes the supervised classification benchmark, and exports 12 interactive HTML and 300 DPI publication PNGs:
```powershell
python src/visualize_and_validate.py
```
*Key Validation Results:*
* **Out-of-Sample Classification Accuracy**: **97.50%**
* **Macro F1-Score**: **96.44%**
* **Explicit Statutory Pattern Precision**: Telecom Franchises (97.8%), Health/Bed Capacity (97.0%), Education (91.8%).

### 3. Interactive Category Query & Traceability Engine
Query any national statute by ID or predict the macro-domain for a newly drafted local ordinance:
```powershell
# Query an existing statute by ID:
python src/categorize_query.py --id ra_7160_1991

# Categorize custom draft ordinance text:
python src/categorize_query.py --text "AN ORDINANCE BANNING ELECTRONIC CIGARETTES AND VAPING IN ALL ENCLOSED PUBLIC SPACES IN DAVAO CITY."
```

### 4. Ground Truth Dataset & Excel Generation
To re-generate the ground truth benchmark or re-export the master review Excel workbook:
```powershell
# Generate the stratified 350-pair benchmark:
python scripts/generate_ground_truth_dataset.py

# Export the master 4-sheet review Excel workbook:
python scripts/export_ground_truth_excel.py

# Validate benchmark balance and citations:
python scripts/validate_ground_truth.py
```

---

## 📑 Municipal Ordinance Ingestion: OCR vs. Vision-Language Models

Local government archives (such as the Davao City Sangguniang Panlungsod records in `corpus/city_ordinances/`) consist of physical paper scans with stamps, councilor attendance rosters, and low-contrast signatures.

### Benchmark Summary (Ordinance No. 0667-21)
Our empirical evaluation ([`OCR_EXPERIMENT_DRAFT.md`](file:///c:/Users/SHRIMP/Documents/thesis-repo/OCR_EXPERIMENT_DRAFT.md)) reveals why traditional OCR must not be used:

| Ingestion Model | Word Error Rate (WER) $\downarrow$ | Character Error Rate (CER) $\downarrow$ | Citation / Header Precision $\uparrow$ | Vector Fidelity $\uparrow$ | Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Traditional Scanner OCR** | **27.44%** | **25.05%** | **36.36%** | **84.36%** | ❌ High Noise (Breaks Section Regex) |
| **Llama-3.2-11B-Vision** | **1.27%** | **0.29%** | **100.00%** | **97.97%** | ✅ Strong Open VLM |
| **Qwen2.5-VL-7B-Instruct** | **0.00%** | **0.02%** | **100.00%** | **100.00%** | 🏆 **Top Open-Source Local Model** |
| **Gemini 1.5 Flash Vision** | **0.00%** | **0.00%** | **100.00%** | **100.00%** | 🏆 **Top Cloud API (Free Tier)** |

To re-run this comparative benchmark:
```powershell
python scripts/compare_ocr_experiments.py
```

---

## 🌐 Google Colab Workflows

For GPU-accelerated training, dense vector index construction, and transformer cross-encoding:
1. Open [`notebooks/01_corpus_preparation_and_topic_modeling.ipynb`](file:///c:/Users/SHRIMP/Documents/thesis-repo/notebooks/01_corpus_preparation_and_topic_modeling.ipynb) in Google Colab.
2. Select a **T4 GPU** runtime (`Runtime` $\rightarrow$ `Change runtime type` $\rightarrow$ `T4 GPU`).
3. Execute the cells sequentially to run **BERTopic**, generate interactive 2D topic maps, and test zero-shot ordinance classification.

---

## 🔒 Git & Large File Management

To comply with GitHub repository size limits ($<100\text{ MB}$ per file), the [`.gitignore`](file:///c:/Users/SHRIMP/Documents/thesis-repo/.gitignore) is pre-configured to exclude:
* `corpus/` (Raw JSONLs and heavy scanned PDF folders).
* `output/*.jsonl` and `output/*.pkl` (Generated dataset binaries).
* LaTeX auxiliary compilation caches (`*.aux`, `*.log`, `*.toc`, `*.bbl`, etc.).

*All dataset binaries and serialized vector models are reproduced automatically by running the setup scripts.*
