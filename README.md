# A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances

[![Institution: Ateneo de Davao University](https://img.shields.io/badge/Institution-Ateneo%20de%20Davao%20University-003366.svg)](https://www.addu.edu.ph/)
[![Department: Computer Science](https://img.shields.io/badge/Department-Computer%20Science-blue.svg)]()
[![Degree: BS Computer Science Thesis](https://img.shields.io/badge/Thesis-Undergraduate%20Research-green.svg)]()
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)]()
[![LaTeX: TeX Live 2026](https://img.shields.io/badge/LaTeX-TeX%20Live%202026-blue.svg)]()

**Undergraduate Thesis Project (April 2026)**  
**Authors**: Ralph Paolo Dulce & Yahyah Odin  
**Adviser**: Mr. Adrian "Ogs" Ablazo  
**Institution**: School of Arts and Sciences, Ateneo de Davao University, Davao City, Philippines  

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
├── CS_Undergraduate_Thesis_Template/  <-- Full LaTeX Thesis Manuscript Source
│   ├── main.tex                       <-- Root LaTeX document
│   ├── references.bib                 <-- BibTeX literature database
│   ├── chapters/                      <-- Individual thesis chapters
│   │   ├── introduction.tex           <-- Chapter 1
│   │   ├── literature_review.tex      <-- Chapter 2
│   │   ├── theoretical-framework.tex  <-- Theoretical Framework
│   │   └── methodology.tex            <-- Chapter 3
│   ├── figs/                          <-- Publication diagrams and architectural figures
│   └── .vscode/settings.json          <-- Instant live-preview configuration
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
│   └── visualize_and_validate.py      <-- 80/20 train/test holdout validation & plotting
│
├── scripts/                           <-- Automated Helper & Execution Scripts
│   ├── build_paper.py                 <-- One-click LaTeX PDF compiler (TeX Live / pdflatex)
│   ├── compare_ocr_experiments.py     <-- Empirical OCR vs. VLM benchmark suite
│   └── build_notebook.py              <-- Colab notebook generator
│
├── notebooks/                         <-- GPU-Accelerated Google Colab Notebooks
│   └── 01_corpus_preparation_and_topic_modeling.ipynb
│
├── output/                            <-- Generated Summaries & Evaluation Artifacts
│   ├── topic_summary.csv              <-- 11 Macro Legal Domains summary
│   ├── validation_report.json         <-- Empirical 80/20 holdout metrics
│   ├── ocr_experiment_report.json     <-- OCR vs. VLM benchmark metrics
│   └── visualizations/                <-- 12 publication PNGs and interactive HTML charts
│
├── OCR_EXPERIMENT_DRAFT.md            <-- Research draft on OCR vs VLM municipal parsing
├── requirements.txt                   <-- Python dependency specifications
└── .gitignore                         <-- Ignores heavy corpus and LaTeX cache files
```

---

## Environment Setup & Installation

### 1. Prerequisites (Matching Local Machine Setup)
* **Python**: Version `3.10` or higher (tested on Python 3.10 – 3.14).
* **LaTeX Distribution**: [TeX Live 2026](https://www.tug.org/texlive/) (Windows default install at `C:\texlive\2026\bin\windows`).
  * Verify in terminal: `pdflatex --version` (Ensure `pdflatex` is added to system `PATH`).
  * *Note*: We specifically avoid default `latexmk` on Windows because it requires a separate Perl interpreter; our configuration directly calls native `pdflatex` and `bibtex`.
* **VS Code Extensions**:
  * `LaTeX Workshop` (`James-Yu.latex-workshop`) — Configured for side-by-side Overleaf-like live compilation.
  * `Python` (`ms-python.python`) — For script execution and virtual environments.

### 2. Python Virtual Environment Setup

Clone the repository and initialize a virtual environment:

```powershell
# 1. Clone the repository
git clone https://github.com/<your-username>/thesis-repo.git
cd thesis-repo

# 2. Create an isolated Python virtual environment
python -m venv venv

# 3. Activate the virtual environment
# On Windows (PowerShell):
.\venv\Scripts\activate
# On Linux / macOS:
source venv/bin/activate

# 4. Install all required dependencies
pip install -r requirements.txt
```

---

## Thesis Paper Drafting (Overleaf-Style Local Setup)

The LaTeX source code for the 82-page thesis manuscript is located in `CS_Undergraduate_Thesis_Template/`. The setup was migrated from Overleaf to run completely offline in VS Code with identical live-preview ergonomics.

### How We Replicate the Overleaf Experience Locally

| Action | Shortcut / Command | What Happens |
| :--- | :--- | :--- |
| **Open Side-by-Side PDF** | **`Ctrl + Alt + V`** | Opens the compiled PDF directly in a tab. Drag it to the right half of your screen for the classic Overleaf split-screen view. |
| **Instant Recompile** | **`Ctrl + S`** (Save) | Triggers the fast 1-second single-pass `pdflatex` build and reloads the preview tab automatically. |
| **Jump from Code $\rightarrow$ PDF** | **`Ctrl + Alt + J`** <br>*(or `Ctrl + Alt + Click`)* | Jumps the PDF preview directly to the paragraph your cursor is on and highlights it. |
| **Jump from PDF $\rightarrow$ Code** | **`Ctrl + Left Click`** on PDF | Clicks any text in the PDF tab to jump straight to that line in your `.tex` source code. |
| **Full Reference / Citation Build** | `python scripts/build_paper.py` | Runs all 4 passes (`pdflatex -> bibtex -> pdflatex*2`) to resolve bibliography and TOC changes. |

1. **Multi-File Root Document Linking**:
   * All subfiles inside `chapters/` have `% !TeX root = ../main.tex` at line 1. You never need to switch back to `main.tex` to compile; editing and saving inside any chapter automatically updates the master document.
2. **Formatter Bypass (`editor.formatOnSave: false`)**:
   * To prevent the common VS Code warning (*"Please set your LaTeX formatter in latex-workshop.formatting.latex"*), formatting on save is explicitly disabled for LaTeX so only the fast compilation runs on `Ctrl + S`.

### The Live Configuration (`.vscode/settings.json`)
The pre-tuned live-preview settings are tracked in `.vscode/settings.json` (and `CS_Undergraduate_Thesis_Template/.vscode/settings.json`):

```json
{
    "latex-workshop.latex.tools": [
        {
            "name": "pdflatex-fast",
            "command": "pdflatex",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "%DOC%"
            ]
        },
        {
            "name": "bibtex",
            "command": "bibtex",
            "args": [
                "%DOCFILE%"
            ]
        }
    ],
    "latex-workshop.latex.recipes": [
        {
            "name": "fast-pdflatex (instant preview)",
            "tools": [
                "pdflatex-fast"
            ]
        },
        {
            "name": "full-build (pdflatex -> bibtex -> pdflatex*2)",
            "tools": [
                "pdflatex-fast",
                "bibtex",
                "pdflatex-fast",
                "pdflatex-fast"
            ]
        }
    ],
    "latex-workshop.latex.recipe.default": "first",
    "latex-workshop.latex.autoBuild.run": "onSave",
    "latex-workshop.latex.autoBuild.interval": 500,
    "latex-workshop.view.pdf.viewer": "tab",
    "latex-workshop.view.pdf.refreshes": "onBuild",
    "latex-workshop.synctex.afterBuild.enabled": true,
    "latex-workshop.latex.rootFile.useWorkspace": true,
    "[latex]": {
        "editor.formatOnSave": false
    },
    "[tex]": {
        "editor.formatOnSave": false
    }
}
```

### Full Multi-Pass Compilation (Citations & TOC Refresh)
When you add new citations in `references.bib` or add new sections:
* **Option A (VS Code Recipe)**: Click the **TeX** sidebar icon $\rightarrow$ **"Build LaTeX project"** $\rightarrow$ select **`full-build (pdflatex -> bibtex -> pdflatex*2)`**.
* **Option B (One-Click Python Script)**:
  ```powershell
  python scripts/build_paper.py
  ```
  *Output PDF is compiled to:* `CS_Undergraduate_Thesis_Template/main.pdf`.

---

## Replication Instructions for Another Device / AI Agent

If setting up this repo on another machine or asking an AI assistant (such as Gemini or Antigravity) on another device to replicate this exact environment:

### 1. Prerequisites (LaTeX & Python)
* **Install TeX Live 2026** (Windows installer: `install-tl-windows.exe`). Ensure `pdflatex` is available in your PATH (`pdflatex --version`).
* **Install VS Code Extension**: `LaTeX Workshop` (`James-Yu.latex-workshop`).
* **Python Environment**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  pip install -r requirements.txt
  ```

### 2. Turnkey Setup (Included Out-of-the-Box)
* **Pre-configured `.vscode/settings.json`**:
  * The repository includes tuned settings for root document auto-linking, instant 1-second single-pass `pdflatex-fast` builds on save, SyncTeX forward/inverse search, and format-on-save overrides.
  * No Perl / `latexmk` setup is needed.
* **Paper Writing & Agent Rules (`.agents/rules/paper-writing-instructions.md`)**:
  * Contains the full domain context (Magtajas v. Pryce doctrine, Philippine statutory hierarchy, Stage 1/Stage 2 pipeline), strict anti-AI tone rules, paragraph anatomy requirements, and peer-reviewed DOI citation verification protocols.
  * Any agent (Gemini, Antigravity, etc.) operating in this workspace automatically adheres to these rules when drafting, citing, or revising chapters.

### 3. Immediate Writing & Live Preview Workflow
1. Open any chapter file (e.g., `CS_Undergraduate_Thesis_Template/chapters/methodology.tex`).
2. Press **`Ctrl + Alt + V`** to open the live PDF viewer tab. Snap it to the right half of your screen.
3. Edit anywhere and press **`Ctrl + S`** — the PDF updates in ~1 second.
4. When adding new citations to `references.bib` or modifying section hierarchies, run the turnkey compiler:
   ```powershell
   python scripts/build_paper.py
   ```
   This compiles all 4 passes (`pdflatex -> bibtex -> pdflatex -> pdflatex`) cleanly to `CS_Undergraduate_Thesis_Template/main.pdf`.

---

## Core Pipelines & Execution Guide

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

---

## Municipal Ordinance Ingestion: OCR vs. Vision-Language Models

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

### Running Batch Ordinance Transcription Locally (Unattended / Overnight)
To parse 1,000+ scanned PDFs offline with **zero API costs and zero token limits**:
1. Install **Ollama** or **vLLM** and pull the vision model:
   ```bash
   ollama run qwen2.5-vl:7b
   ```
2. The batch pipeline iterates through `corpus/city_ordinances/`, extracts high-resolution page images via `PyMuPDF`, prompts the local VLM to output structured Markdown/JSON, and automatically appends clean records to `output/davao_ordinances.jsonl`.

---

## Google Colab Workflows

For GPU-accelerated training, dense vector index construction, and transformer cross-encoding:
1. Open [`notebooks/01_corpus_preparation_and_topic_modeling.ipynb`](file:///c:/Users/SHRIMP/Documents/thesis-repo/notebooks/01_corpus_preparation_and_topic_modeling.ipynb) in Google Colab.
2. Select a **T4 GPU** runtime (`Runtime` $\rightarrow$ `Change runtime type` $\rightarrow$ `T4 GPU`).
3. Execute the cells sequentially to run **BERTopic**, generate interactive 2D topic maps, and test zero-shot ordinance classification.

---

## Git & Large File Management

To comply with GitHub repository size limits ($<100\text{ MB}$ per file), the [`.gitignore`](file:///c:/Users/SHRIMP/Documents/thesis-repo/.gitignore) is pre-configured to exclude:
* `corpus/` (Raw JSONLs and heavy scanned PDF folders).
* `output/*.jsonl` and `output/*.pkl` (Generated dataset binaries).
* LaTeX auxiliary compilation caches (`*.aux`, `*.log`, `*.toc`, `*.bbl`, etc.).

*All dataset binaries and serialized vector models are reproduced automatically by running the setup scripts.*

---

