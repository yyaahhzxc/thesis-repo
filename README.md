# A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances

[![Institution: Ateneo de Davao University](https://img.shields.io/badge/Institution-Ateneo%20de%20Davao%20University-003366.svg)](https://www.addu.edu.ph/)
[![Department: Computer Science](https://img.shields.io/badge/Department-Computer%20Science-blue.svg)]()
[![Degree: BS Computer Science Thesis](https://img.shields.io/badge/Thesis-Undergraduate%20Research-green.svg)]()
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)]()
[![LaTeX: TeX Live / MiKTeX](https://img.shields.io/badge/LaTeX-97%20Pages%20%7C%200%20Errors-blue.svg)]()
[![Benchmark: 350 Pairs](https://img.shields.io/badge/Benchmark-350%20Pairs%20%7C%208%20Domains-orange.svg)]()

**Undergraduate Thesis Project (Academic Year 2025–2026)**  
**Authors**: Ralph Paolo Dulce and Yahyah Odin  
**Adviser**: Mr. Adrian "Ogs" Ablazo  
**Institution**: Department of Computer Science, School of Arts and Sciences, Ateneo de Davao University, Davao City, Philippines  

---

## Executive Summary

This repository contains the official research codebase, empirical benchmark datasets, statutory processing pipelines, and LaTeX source manuscript for the undergraduate computer science thesis:

> **"A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference."**

The system operationalizes the legal doctrine articulated in *Magtajas v. Pryce Properties, Inc.* (G.R. No. 111097, July 20, 1994, 234 SCRA 78), which mandates that municipal ordinances enacted by local government units (LGUs) must conform to national statutes and public policy. The architecture implements an automated *ex-ante* audit pipeline that scrutinizes proposed draft ordinances prior to enactment using a two-stage retrieve-then-entail paradigm:

1. **Stage 1 (Coarse Retrieval)**: Hybrid sparse lexical (BM25) and dense bi-encoder semantic indexing over 25,432 cleaned Philippine national statutes, filtering the vast legal search space to top-$k$ relevant statutory candidates.
2. **Stage 2 (Fine Natural Language Inference)**: Asymmetric span-level cross-encoder classification with temperature-calibrated softmax outputs across three formal NLI classes (*Entailment*, *Contradiction*, and *Neutral*), coupled with self-attention feature attribution for granular legal interpretability.

```mermaid
flowchart LR
    A[Proposed Draft Ordinance] --> B[Stage 1: Coarse IR\nBM25 + Dense Bi-Encoder]
    B --> C[Top-k Candidate Statutes\nFiltered Statutory Space]
    C --> D[Stage 2: Fine NLI Cross-Encoder\nAsymmetric Span Pairing]
    D --> E[Calibrated Conflict Probabilities\nEntailment | Neutral | Contradiction]
    E --> F[Self-Attention XAI Attribution\nSpan-Level Interpretability]
```

---

## Quick Start: Environment Initialization

This section outlines the setup process for collaborators, thesis committee members, and researchers deploying this repository on a new workstation.

### Step 1: Automated Configuration Script

On Windows systems, execute the automated setup script from PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_environment.ps1
```

The script performs the following tasks:
1. Verifies the presence of a local LaTeX compiler (`pdflatex`). If none is detected, it invokes the Windows Package Manager (`winget`) to install MiKTeX.
2. Initializes an isolated Python virtual environment (`venv/`) if one does not already exist.
3. Installs all required Python dependencies specified in `requirements.txt`.
4. Executes a verification compilation of the LaTeX thesis manuscript.

### Step 2: VS Code / Cursor Extension Configuration

> [!IMPORTANT]
> **Manual Installation of LaTeX Workshop (`James-Yu.latex-workshop`)**  
> While `setup_environment.ps1` attempts to install the extension via the command line, the execution will fail silently if the `code` executable is not registered in the system environment `PATH` variable, or if you are working within **Cursor**, **VSCodium**, or an alternative editor.  
> **Please ensure the extension is installed manually:**
> 1. Open the editor and open the Extensions view (**`Ctrl + Shift + X`**).
> 2. Search for **`LaTeX Workshop`** authored by **James Yu** (`James-Yu.latex-workshop`).
> 3. Click **Install**.
> 4. If prompted, restart the editor to ensure all environment paths are refreshed.

### Step 3: Compiling the Thesis Manuscript

The repository provides automated Python compilation utilities configured to build without external Perl dependencies:

```powershell
# Full four-pass compilation (pdflatex -> bibtex -> pdflatex -> pdflatex)
python scripts/build_paper.py

# Fast single-pass preview compilation (approximately 1 second)
python scripts/build_paper.py --fast
```

*Target output:* `CS_Undergraduate_Thesis_Template/main.pdf` (97 pages, 0 compilation errors).

---

## Repository Structure

The repository is structured logically into dedicated directories for the LaTeX manuscript, evaluation data, documentation, experimental scripts, and core system modules:

```
thesis-repo/
├── CS_Undergraduate_Thesis_Template/  <-- Complete LaTeX Thesis Manuscript Source
│   ├── main.tex                       <-- Root document
│   ├── references.bib                 <-- BibTeX bibliographic database
│   ├── chapters/                      <-- Chapter source files
│   │   ├── introduction.tex           <-- Chapter 1: Introduction
│   │   ├── literature_review.tex      <-- Chapter 2: Literature Review
│   │   ├── theoretical-framework.tex  <-- Theoretical and Conceptual Framework
│   │   └── methodology.tex            <-- Chapter 3: Methodology (Standardized titles)
│   ├── figs/                          <-- Publication figures and architectural schematics
│   │   ├── statute_type_composition.png
│   │   ├── historical_temporal_evolution.png
│   │   └── macro_domain_distribution.png
│   └── .vscode/settings.json          <-- Editor-specific build and SyncTeX settings
│
├── data/                              <-- Evaluation Datasets and Benchmarks
│   ├── ground_truth_350_review.xlsx   <-- Master 4-sheet evaluation and review workbook
│   ├── ground_truth_350.jsonl         <-- Master 350-pair benchmark dataset (JSONL)
│   ├── ground_truth_350.csv           <-- Master 350-pair benchmark dataset (CSV)
│   ├── blocks/                        <-- Partitioned evaluation sets for raters
│   │   ├── block_1.csv                <-- Evaluation Set A (70 pairs)
│   │   ├── block_2.csv                <-- Evaluation Set B (70 pairs)
│   │   ├── block_3.csv                <-- Evaluation Set C (70 pairs)
│   │   ├── block_4.csv                <-- Evaluation Set D (70 pairs)
│   │   └── block_5.csv                <-- Evaluation Set E (70 pairs)
│   ├── verbatim_statutory_sections.json <-- Verified statutory provisions
│   ├── corpus_statute_premises.json   <-- Corpus premise extractions
│   └── ordinance_000667_ground_truth.txt <-- Transcription baseline for OCR evaluation
│
├── docs/                              <-- Documentation, Instrument Drafts, and Notes
│   ├── annotation/                    <-- Human evaluation instruments and guidelines
│   │   ├── sp_annotation_cheat_sheet.md           <-- Quick-reference rubric for evaluators
│   │   └── adviser_endorsement_letter_template.md <-- Official institutional request letter
│   ├── drafts/                        <-- Archive of manuscript drafts
│   │   └── Dulce_Odin_CS_Thesis_Draft.pdf         <-- Initial thesis manuscript draft
│   └── experiments/                   <-- Empirical research reports and benchmark notes
│       └── ocr_vs_vlm_experiment.md   <-- Evaluation of OCR vs. VLMs on scanned ordinances
│
├── corpus/                            <-- Statutory Data (Excluded from Git tracking)
│   ├── categorized_national_laws.jsonl <-- Consolidated cleaned national laws (194 MB)
│   ├── national_laws/                 <-- Granular statutory collections (RA, BP, CA, EO, PD)
│   └── city_ordinances/               <-- Scanned municipal PDF ordinances (2021–2025)
│
├── src/                               <-- Core Python Engine
│   ├── preprocess.py                  <-- Statutory text normalization and segmentation
│   ├── topic_modeler.py               <-- Unsupervised SVD and KMeans domain discovery
│   ├── categorize_query.py            <-- Interactive CLI classification tool
│   ├── visualize_and_validate.py      <-- Holdout validation and publication plotting
│   └── scraper/                       <-- Statutory Web Scraper Suite
│       ├── lawphil_scraper.py         <-- Scraper with rate-limiting and resume support
│       └── file_map_config.json       <-- Statute URL index mappings
│
├── scripts/                           <-- Automated Utilities and Build Tools
│   ├── setup_environment.ps1          <-- One-click environment setup script
│   ├── build_paper.py                 <-- LaTeX PDF compiler with --fast option
│   ├── export_ground_truth_excel.py   <-- Master 4-sheet evaluation workbook generator
│   ├── generate_ground_truth_dataset.py <-- Stratified benchmark generation pipeline
│   ├── validate_ground_truth.py       <-- Verification script for citation integrity
│   └── compare_ocr_experiments.py     <-- Comparative OCR and VLM evaluation script
│
├── output/                            <-- Generated Summaries and Evaluation Artifacts
│   ├── topic_summary.csv              <-- Macro legal domain breakdown
│   ├── validation_report.json         <-- Empirical 80/20 holdout metrics
│   ├── ocr_experiment_report.json     <-- OCR vs. VLM benchmark metrics
│   └── visualizations/                <-- 12 publication-ready PNG and HTML figures
│
├── requirements.txt                   <-- Python package specifications
└── .gitignore                         <-- Exclusion rules for heavy corpora and build caches
```

---

## Ground Truth Evaluation Benchmark (350 Pairs)

To establish an empirical evaluation standard for the coarse-to-fine system, a stratified ground truth benchmark of **350 premise-hypothesis pairs** was constructed. The dataset pairs verified statutory provisions from the Philippine national corpus with synthetic and authentic Davao City draft ordinance provisions.

### 1. Difficulty Tier Stratification
The benchmark evaluates model performance across three operational tiers:

* **Tier 1: Lexical-Syntactic Surface Direct (30%, $n=105$)**:  
  Direct textual overlap, explicit numerical penalty ceilings, and verbatim statutory thresholds (e.g., Section 458 of RA 7160 limiting municipal fines to P5,000.00 and imprisonment to one year).
* **Tier 2: Definitional and Structural Operational (40%, $n=140$)**:  
  Structural, administrative, and jurisdictional inconsistencies where vocabulary differs but operational definitions or mandatory procedures conflict (e.g., zoning deviations, administrative authority boundaries, permit requirements).
* **Tier 3: Asymmetric Domain Nuance and Qualitative Overreach (30%, $n=105$)**:  
  Substantive legal conflicts involving *ultra vires* regulatory overreach, preemption doctrines, national field occupation (e.g., national energy transmission, civil aviation, telecommunications), and unstated statutory exemptions.

### 2. Macro Legal Domain Distribution
The 350 pairs are balanced across eight core local governance domains:
1. Public Order, Safety, and Police Powers
2. Local Taxation, Revenue, and Fiscal Measures
3. Zoning, Land Use, and Real Property Administration
4. Environmental Protection, Sanitation, and Waste Management
5. Trade, Commerce, and Local Economic Enterprises
6. Public Health, Sanitation, and Regulated Substances
7. Social Welfare and Protected Demographics
8. Administrative Governance and Local Civil Service

### 3. Master Review Workbook (`data/ground_truth_350_review.xlsx`)

The evaluation suite includes a standardized Microsoft Excel workbook structured into four dedicated sheets for external review and human annotation deployment:

* **Sheet 1 (`Codebook & Instructions`)**: Formal operational definitions for the three target classes (*Entailment*, *Contradiction*, *Neutral*) alongside step-by-step annotation guidelines.
* **Sheet 2 (`All 350 Benchmark Pairs`)**: Complete benchmark dataset featuring verbatim national law premises, ordinance hypotheses, exact statutory citations, and assigned evaluation sets (`Set A` through `Set E`).
* **Sheet 3 (`Domain Summaries`)**: Stratification summary cross-tabulating domain distribution against difficulty tiers.
* **Sheet 4 (`Panel & Annotator Assignments`)**:
  * **Table 1: Evaluation Set Partitioning**: Partitions the 350 benchmark pairs into five distinct evaluation sets (`Set A` to `Set E`), each containing exactly 70 questions.
  * **Table 2: Annotator Directory**: Designates 15 legal researchers from the Sangguniang Panlungsod into five 3-person evaluation trios (Panels A–E). Each panel is anchored by **one Senior Lead Annotator ($\ge 5$ years legislative tenure)** and two Associate Annotators. Recruitment follows purposive availability sampling from the 48-member institutional pool without artificial district quotas, reflecting the city-wide scope of municipal ordinances.
  * **Table 3: Google Forms Branching Blueprint**: Complete technical blueprint for deploying a single master Google Form using Section 1 identifier branching (`Go to section based on answer`) with direct form submissions, collecting 1,050 total judgment data points across 15 individual responses.

---

## Thesis Manuscript (Chapter 3 Methodology Revisions)

The LaTeX thesis manuscript is located in `CS_Undergraduate_Thesis_Template/`. Chapter 3 (`chapters/methodology.tex`) has been refined to align with rigorous computer science thesis standards:

1. **Standardized Section Titles**: Verbose headings were replaced with concise two- to three-word titles consistent with Chapters 1 and 2 (e.g., *Benchmark Construction*, *Workload Allocation*, *Annotator Selection*, *Inter-Rater Reliability*).
2. **Mathematical Workload Allocation**:
   $$\text{Total Judgment Points} = N \times K = 350 \times 3 = 1,050$$
   $$\text{Annotator Burden} = R = \frac{N \times K}{A} = \frac{1,050}{15} = 70 \text{ items/annotator}$$
3. **Statistical Power Analysis**:
   Incorporated Cohen's chi-square goodness-of-fit power calculations ($w = 0.30$, $\alpha = 0.05$, $df = 28$, $N = 1,050$), establishing that the evaluation framework achieves statistical power $> 0.999$, ensuring that inter-rater agreement measures (Fleiss' $\kappa$ and Krippendorff's $\alpha$) are adequately powered.
4. **Purposive Availability Sampling Protocol**:
   Formalized the selection of 15 legal researchers from the Davao City Sangguniang Panlungsod without artificial geographic district quotas, grounded in plenary municipal police powers that apply uniformly across all city districts.
5. **Compilation Status**:
   Verified complete compilation to `CS_Undergraduate_Thesis_Template/main.pdf` (**97 pages, 0 LaTeX errors, 0 overfull hbox warnings in table of contents**).

---

## Municipal Ordinance Ingestion: OCR versus Vision-Language Models

Historical municipal archives from the Davao City Sangguniang Panlungsod (`corpus/city_ordinances/`) consist primarily of physical paper scans with official seals, council attendance rosters, and variable scan contrast.

### Empirical Benchmark Summary (*Ordinance No. 0667-21*)

An empirical study was conducted to evaluate traditional optical character recognition against multimodal vision-language models for document ingestion prior to semantic retrieval (detailed in [`docs/experiments/ocr_vs_vlm_experiment.md`](file:///c:/Users/SHRIMP/Documents/thesis-repo/docs/experiments/ocr_vs_vlm_experiment.md)):

| Ingestion Architecture | Model Classification | Word Error Rate (WER) | Character Error Rate (CER) | Citation & Header Precision | Semantic Cosine Fidelity | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Traditional Scanner OCR** | Optical Character | 27.44% | 25.05% | 36.36% | 84.36% | Deprecated (Tokenization failure) |
| **Llama-3.2-11B-Vision** | Open-Weight VLM | 1.27% | 0.29% | 100.00% | 97.97% | Viable Open-Weight VLM |
| **Qwen2.5-VL-7B-Instruct** | Open-Weight VLM | 0.00% | 0.02% | 100.00% | 100.00% | Primary Local Offline Model |
| **Gemini 1.5 Flash Vision** | Cloud API VLM | 0.00% | 0.00% | 100.00% | 100.00% | Primary Cloud API Baseline |

To re-run the comparative evaluation script:
```powershell
python scripts/compare_ocr_experiments.py
```

---

## Core System Pipelines and Execution Guide

### 1. Statutory Topic Modeling & Corpus Consolidation
Processes the 25,432 national statutes, normalizes legislative formulas, and categorizes provisions into 11 consolidated macro legal domains:
```powershell
python src/topic_modeler.py
```
*Generated outputs:* `output/statutory_topic_model.pkl`, `output/topic_summary.csv`, and `corpus/categorized_national_laws.jsonl`.

### 2. Empirical Holdout Validation (80/20 Train/Test Split)
Evaluates out-of-sample topic projection, measures cosine classification confidence, and exports publication figures:
```powershell
python src/visualize_and_validate.py
```
*Validation Metrics:* Out-of-sample classification accuracy of 97.50% and macro F1-score of 96.44%.

### 3. Interactive Category Query & Traceability Engine
Classifies existing statutes by identifier or predicts the primary legal domain for draft ordinance text:
```powershell
# Query an existing statute:
python src/categorize_query.py --id ra_7160_1991

# Categorize draft ordinance text:
python src/categorize_query.py --text "AN ORDINANCE BANNING ELECTRONIC CIGARETTES AND VAPING IN ALL ENCLOSED PUBLIC SPACES IN DAVAO CITY."
```

### 4. Benchmark Generation and Review Export
Re-generates the benchmark dataset and exports the master evaluation workbook:
```powershell
# Compile the stratified 350-pair dataset:
python scripts/generate_ground_truth_dataset.py

# Export the master 4-sheet review Excel workbook:
python scripts/export_ground_truth_excel.py

# Verify citation validity and domain balance:
python scripts/validate_ground_truth.py
```

---

## Offline Editing Workflow in VS Code / Cursor

The workspace configuration (`.vscode/settings.json`) provides an interactive local editing environment:

| Workflow Action | Keybinding / Command | Description |
| :--- | :--- | :--- |
| **Open Split PDF Preview** | **`Ctrl + Alt + V`** | Opens the compiled PDF directly in an editor tab for side-by-side editing. |
| **Instant Save Compilation** | **`Ctrl + S`** | Executes an immediate single-pass `pdflatex` build (~1 second) and refreshes the view. |
| **Direct Synctex Navigation** | **`Ctrl + Alt + J`** | Jumps the PDF preview directly to the paragraph at the active cursor position. |
| **Inverse SyncTeX Navigation** | **`Ctrl + Click`** on PDF | Clicks on any text within the PDF viewer to locate the corresponding source line in `.tex`. |
| **Full Citation Compilation** | `python scripts/build_paper.py` | Executes all four compilation passes to rebuild bibliographies and structural numbering. |

---

## Data Governance and Repository Scope

To comply with version control best practices and repository size limitations:
* The `corpus/` directory (containing raw statutory corpora and high-resolution scanned PDFs) is excluded from version control via `.gitignore`.
* Serialized machine learning models (`output/*.pkl`) and large intermediate outputs are generated locally by executing the documented setup scripts.
* All evaluation datasets, codebooks, benchmark partitions, and LaTeX manuscript files are fully versioned and tracked.
