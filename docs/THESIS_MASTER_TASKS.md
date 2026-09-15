# **Master Thesis Task Tracker & Milestone Progress Journal**

**Project Title:** *A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference*  
**Authors:** Ralph Paolo Dulce & Yahyah Odin  
**Thesis Adviser:** Mr. Adrian "Ogs" Ablazo  
**Course Professor:** Ma'am Grace Tacadao  
**Institution:** Department of Computer Science, School of Arts and Sciences, Ateneo de Davao University  
**Repository:** [`https://github.com/yyaahhzxc/thesis-repo`](https://github.com/yyaahhzxc/thesis-repo)  
**Last Updated:** 2026-09-15  

---

## **Current Active Focus: Milestone 2 (Chapter 3 Methodology Finalization)**

> **Status:** `IN PROGRESS` (Review completed; LaTeX and README updates pending execution)  
> **Target Manuscript:** `CS_Undergraduate_Thesis_Template/chapters/methodology.tex`  
> **Output Build:** `CS_Undergraduate_Thesis_Template/main.pdf` (Compiling with 0 errors)  

---

## **1. Canonical System Environment Reference Card**

*This hardware and software profile reflects the local workstation environment simulating Philippine Local Government Unit (LGU) IT capacity. It must be consistently cited across all methodology sections and reproducible setup guides.*

### **A. Hardware Specifications**
| Component | Specification | Operational Role in Study |
| :--- | :--- | :--- |
| **Workstation Model** | Local Single-Workstation Desktop Testbed | Simulates standard LGU IT infrastructure |
| **CPU** | Intel(R) Core(TM) i3-10105F @ 3.70 GHz (4 Cores, 8 Threads) | Stage 1 Sparse/Dense Retrieval & Corpus Tokenization |
| **GPU** | AMD Radeon RX 6600 (8 GB GDDR6 VRAM, PCIe 4.0) | Stage 2 Cross-Encoder Fine-Tuning & Inference |
| **System RAM** | 8.00 GB DDR4 | In-memory DataFrame indexing and batch collation |
| **Storage** | High-Speed NVMe Solid-State Drive | Fast I/O for 25,432 national statutory documents |

### **B. Software Specifications**
| Layer | Environment / Package | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Operating System** | Microsoft Windows 10 Pro 64-bit | Build 19045 | Base OS environment |
| **Runtime / Language** | Python | 3.10+ / 3.14 | Core execution engine |
| **Deep Learning Framework** | PyTorch (`torch`) | 2.14.0+ | Tensor operations and neural attention layers |
| **Transformer Library** | Hugging Face (`transformers`) | 5.16.1+ | Cross-Encoder (`ModernBERT`, `DeBERTa-v3`) models |
| **Dense Embeddings** | Sentence-Transformers | 6.0.1+ | Stage 1 Bi-Encoder (`all-MiniLM-L6-v2`) vectors |
| **Lexical Retrieval** | `rank-bm25` | 0.2.2+ | Stage 1 Sparse BM25 scoring with sublinear scaling |
| **Classical ML / Metrics** | `scikit-learn` / `scipy` | 1.9.0 / 1.18.1 | McNemar's test, Friedman test, Silhouette, SVD |
| **Data Processing** | `pandas` / `numpy` | 3.0.5 / 2.5.2 | Corpus census and Ground Truth manipulation |
| **Document Ingestion** | `pymupdf` (`fitz`) / `pypdf` | 1.28.2 / 6.16.2 | PDF text extraction from municipal scans |
| **LaTeX Environment** | TeX Live 2026 / MiKTeX (`pdflatex`, `bibtex`) | Current | Full Overleaf-compatible PDF compilation |

---

## **2. Verbatim Milestone Instructions Archive**

### **Milestone 1: Data Description - Machine Learning**
* **Status:** `COMPLETED` (Completed on September 4, 2026; Commit `cc1c33d`).
* **Summary:** Integrated corpus breakdown (25,432 national laws, ~1,660 local ordinances), static 70/15/15 split, initial overfitting regularization (AdamW, dropout, early stopping), and initial Overleaf preview configuration.

---

### **Milestone 2: Methodology Revisions**
* **Status:** `ACTIVE / IN PROGRESS`
* **Official Prompt Provided by Course Professor:**

> *"Revise the portion of your Chapter 3: Methodology to include the following:*
>
> *1. **Hardware and software environment:** Indicate the exact hardware (CPU, GPU, RAM) and software environment (OS, PL and version, key libraries and their versions).*  
> *2. **Version control and reproducibility:** Provide a link to a private or public repository (GitLab or GitHub). The repository must include a README.md with instructions on how to install dependencies and how to run a minimal working example of your code.*  
> *3. **Baseline selection:** Identify at least one standard baseline or approach (can be from related literature cited in Chapter 2) that you will compare your work against. Also explain why this is the baseline chosen.*  
>
> *Moreover, you should also include the following:*  
>
> *4. **Machine Learning:***  
> *   * **Evaluation metrics:** List the statistical metrics that you will use to judge model performance. Again, justify your choices based on your problem context.*  
> *   * **Hyperparameter tuning:** Document your strategy. Specify which parameters are fixed, which are variable, and which search method are you using (e.g., grid search, random search, or Bayesian).*  
> *   * **Statistical model comparison:** Describe the test(s) (including the equations) that you are going to use (i.e., Friedman Test, McNemar's test, Paired t-test). This depends on the number of models that you are going to compare and the number of datasets.*  
>
> *This revisions should complete Chapter 3: Methodology. As mentioned previously, submit the entire thesis manuscript in Overleaf-LaTeX format."*

---

### **Milestone 3: [Reserved for Milestone 3 Instructions]**
* **Status:** `UPCOMING`
* *(Awaiting user input. The agent will paste the exact instructions here verbatim and generate the corresponding actionable task breakdown).*

---

## **3. Master Checklist: Milestone 2 Deliverables**

### **Item 1: Hardware and Software Environment**
- [x] **Audit current manuscript**: Reviewed `methodology.tex` §3.5; identified that high-level conceptual text exists but exact models/versions were omitted.
- [ ] **Draft LaTeX specification in `methodology.tex` §3.5**:
  - [ ] Add formal subsection/text detailing CPU (Intel i3-10105F), GPU (AMD Radeon RX 6600 8GB), and RAM (8GB).
  - [ ] Add software environment details (Windows 10 Pro 64-bit, Python 3.10+, PyTorch 2.14+, Transformers 5.16+, sentence-transformers 6.0+, rank-bm25 0.2.2+).
  - [ ] Insert publication-grade `booktabs` summary table (`tab:hardware_software_specs`).

### **Item 2: Version Control and Reproducibility**
- [x] **Verify Git Remote**: Confirmed active GitHub remote at `https://github.com/yyaahhzxc/thesis-repo`.
- [ ] **Add Repository & Reproducibility Subsection in `methodology.tex`**:
  - [ ] Formalize `\subsection{Version Control and Reproducibility}` in Chapter 3.
  - [ ] Provide explicit clickable GitHub URL and commit hash tracking.
  - [ ] Detail reproducibility protocol (virtual environment, requirements, fixed random seeds).
- [ ] **Enhance `README.md` with Minimal Working Example (MWE)**:
  - [ ] Add a dedicated `## Minimal Working Example (MWE)` section.
  - [ ] Provide a 1-command runnable script (`python scripts/run_mwe.py` or interactive CLI command) that executes an immediate sample conflict detection test in $< 5$ seconds.

### **Item 3: Baseline Selection and Justification**
- [x] **Stage 1 Retrieval Baseline**: Verified BM25 baseline from Wu et al. (2025 AIIR) is already benchmarked in Table 3.6 and Table 3.7.
- [ ] **Stage 2 NLI Baseline Formulation**:
  - [ ] Formally designate standard off-the-shelf zero-shot Cross-Encoder (e.g., `deberta-v3-base` without task-specific fine-tuning / COLIEE Task 4 baseline from Rabelo et al., 2022 and Tran et al., 2026).
- [ ] **Draft `\subsubsection{Baseline Selection and Justification}` in `methodology.tex` §3.6**:
  - [ ] Synthesize Stage 1 (BM25 lexical benchmark) and Stage 2 (Zero-shot legal NLI benchmark).
  - [ ] Explain rationale grounded in Chapter 2 literature (measuring exact value added by domain fine-tuning and hybrid rank fusion).

### **Item 4: Machine Learning Evaluation Metrics**
- [x] **Audit Existing Metrics**: Verified that `methodology.tex` §3.7 already includes:
  - Stage 1: $\text{Recall@}k$ ($k \in \{10, 30, 50\}$) [Eq. 3.4], $\text{MRR@}k$ [Eq. 3.5].
  - Stage 2: Precision, Recall, $F_1$-score [Eq. 3.6], Macro $F_1$ [Eq. 3.7].
  - Cost-sensitive decision thresholding: $F_{2, \text{conflict}}$ [Eq. 3.8] and validation threshold tuning $\tau^*$ [Eq. 3.9].
  - Annotation IRR: Fleiss' Kappa ($\kappa$) in §3.4.
- [ ] **Minor Enhancement**: Add explicit mention of query latency (milliseconds per query) and memory footprint as operational throughput metrics.

### **Item 5: Hyperparameter Tuning Strategy**
- [x] **Audit Existing Parameters**: Identified that AdamW $\lambda = 0.01$, dropout $p = 0.1$, patience $= 4$, and threshold sweep $\tau \in [0.25, 0.50]$ are currently scattered in narrative prose.
- [ ] **Draft `\subsubsection{Hyperparameter Tuning Strategy}` in `methodology.tex` §3.6**:
  - [ ] Declare **Grid Search** as the primary search strategy across candidate parameters.
  - [ ] Justify Grid Search over Bayesian/Random search based on the compact search space and local GPU execution feasibility ($< 2$ hours).
  - [ ] Delineate **Fixed Hyperparameters**: AdamW optimizer, $\lambda = 0.01$, dropout $p = 0.10$, patience $= 4$, warmup ratio $= 0.10$, RRF smoothing constant $k_{\text{rrf}} = 60$.
  - [ ] Delineate **Variable Hyperparameters & Search Bounds**: Peak learning rate $\eta \in \{1\times 10^{-5}, 2\times 10^{-5}, 3\times 10^{-5}, 5\times 10^{-5}\}$, batch size $B \in \{8, 16\}$, max sequence length $L \in \{256, 512\}$, decision threshold $\tau \in [0.25, 0.50]$ ($\Delta \tau = 0.01$), fusion weight $\alpha \in [0.0, 1.0]$.
  - [ ] Insert publication `booktabs` table (`tab:hyperparameter_tuning_space`).

### **Item 6: Statistical Model Comparison**
- [x] **Audit Existing Content**: Confirmed statistical significance testing is completely absent in Chapter 3.
- [ ] **Draft `\subsubsection{Statistical Model Comparison}` in `methodology.tex` §3.7**:
  - [ ] **McNemar's Test (Pairwise Stage 2 Classification)**:
    - Detail 2x2 contingency table ($a, b, c, d$) on the static holdout test set ($N_{\text{test}} = 53$).
    - State equation with continuity correction:
      $$\chi^2 = \frac{(|b - c| - 1)^2}{b + c} \sim \chi^2_1$$
    - Justify via Dietterich (1998) for paired categorical outcomes where Paired $t$-tests fail normality.
  - [ ] **Friedman Test (Multi-Model Stage 1 Retrieval Ranking)**:
    - Detail ranking of $k > 2$ retrieval architectures across $N = 350$ paired test queries.
    - State equation:
      $$\chi_F^2 = \frac{12N}{k(k+1)} \left[ \sum_{j=1}^k R_j^2 - \frac{k(k+1)^2}{4} \right]$$
    - Justify via Demšar (2006) for non-parametric rank comparison across information retrieval models.
    - Detail post-hoc **Wilcoxon Signed-Rank Test** with Bonferroni correction ($\alpha / m$) when $H_0$ is rejected.

### **Item 7: Overleaf-LaTeX Compilation & Submission Readiness**
- [x] **Compile Local Document**: Verified zero-error build via `python scripts/build_paper.py --fast` (97 pages).
- [ ] **Full Four-Pass Build**: Execute `python scripts/build_paper.py` after editing to rebuild all citations and cross-references.
- [ ] **Overleaf Sync Check**: Confirm directory structure and files are 100% compliant with Overleaf import standards.

---

## **4. Broad Project Components & Work Streams Tracker**

### **A. Thesis Manuscript (`CS_Undergraduate_Thesis_Template/`)**
- [x] **Chapter 1 (Introduction)**: Finished; harmonized corpus scope ($N = 25,432$ laws; ~1,660 ordinances; English-only; $1\text{-vs-}N$ boundary).
- [x] **Chapter 2 (Literature Review)**: Finished; includes COLIEE 2026 proceedings, affirmative bias analysis, quadratic complexity bounds, and verified BibTeX keys.
- [-] **Chapter 3 (Methodology)**: In active revision for Milestone 2 compliance.
- [ ] **Chapter 4 (Results and Discussion)**: Pending live fine-tuning runs and full empirical evaluation.
- [ ] **Chapter 5 (Conclusions and Recommendations)**: Scheduled for post-evaluation phase.

### **B. Core Machine Engine & Scripts (`src/`, `scripts/`)**
- [x] Unsupervised Statutory Topic Modeler (`src/topic_modeler.py`): 11 macro domains, SVD 2D projection.
- [x] Out-of-sample holdout validation (`src/visualize_and_validate.py`): 97.5% classification accuracy.
- [x] Full-corpus token census (`output/corpus_token_census.json`): 94.83% sections $\le 512$ tokens.
- [x] Stage 1 candidate retrieval ablation benchmark (`src/stage1_retrieval_benchmark.py`).
- [x] Full-corpus retrieval benchmark ($N = 25,432$ laws): Proved BM25 has 43.14% R@50 and hard-filtering fails.
- [x] Working interactive prototype (`scripts/prototype_pipeline.py`): Demonstrates retrieve-then-entail on sample cases.
- [ ] Minimal Working Example runner (`scripts/run_mwe.py`): Quick standalone test for README.
- [ ] Stage 2 Cross-Encoder fine-tuning and validation script (`ModernBERT` vs `DeBERTa-v3`).
- [ ] Statistical test script (`scripts/statistical_tests.py`): Automatic execution of McNemar's and Friedman tests.

### **C. Ground Truth Benchmark & Human Evaluation (`data/`, `docs/annotation/`)**
- [x] Master 350-pair Ground Truth dataset (`data/ground_truth_350.jsonl`, `.csv`).
- [x] Master 4-sheet review Excel workbook (`data/ground_truth_350_review.xlsx`).
- [x] Evaluation set partitions (Set A to Set E, 70 pairs each).
- [x] Sangguniang Panlungsod annotator directory (15 legal researchers, 5 panels).
- [x] Formal Legal Codebook & Decision Rules (`docs/annotation/sp_annotation_cheat_sheet.md`).
- [x] Adviser endorsement letter template (`docs/annotation/adviser_endorsement_letter_template.md`).
- [ ] Collection of 15 SP evaluator responses via Google Forms.
- [ ] Fleiss' Kappa ($\kappa$) calculation script on actual rater judgments.

---

## **5. Chronological Progress Journal**

| Date | Scope | Actions Accomplished | References / Files |
| :--- | :---: | :--- | :--- |
| **2026-09-04** | Milestone 1 | Completed Milestone 1 (Data Description - Machine Learning); integrated train/val/test splits and overfitting controls. | Commit `cc1c33d` |
| **2026-09-05** | Ground Truth | Generated 350-pair Ground Truth benchmark; Cohen's power analysis ($w=0.30$); SP workload allocation formulas. | Commit `a17b67b` |
| **2026-09-06** | Methodology | Restructured Chapter 3 into chronological 11-section pipeline; added full-corpus and 9-model retrieval benchmarks. | Commit `4963bcf`, `77236f3` |
| **2026-09-08** | Token Census | Completed token length census across 164,620 sections; formulated cost-sensitive threshold $\tau^*$ via $F_2$-score. | Commit `0804727` |
| **2026-09-11** | Literature | Integrated COLIEE 2026 proceedings; analyzed affirmative bias phenomenon; contrasted edge vs cloud models. | Commit `483e15c` |
| **2026-09-15** | Milestone 2 | Audited thesis against Milestone 2 instructions; established master task tracker (`docs/THESIS_MASTER_TASKS.md`) and persistent agent tracking rule (`.agents/rules/task-tracking-instructions.md`). | Current Turn |
