# **Master Thesis Task Tracker & Milestone Progress Journal**

**Project Title:** *A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference*  
**Authors:** Ralph Paolo Dulce ("Ralph") & Yahyah Odin ("Yah")  
**Thesis Adviser:** Mr. Adrian "Ogs" Ablazo  
**Course Professor:** Ma'am Grace Tacadao  
**Institution:** Department of Computer Science, School of Arts and Sciences, Ateneo de Davao University  
**Repository:** [`https://github.com/yyaahhzxc/thesis-repo`](https://github.com/yyaahhzxc/thesis-repo)  
**Last Updated:** 2026-09-15  

---

## **Executive Status Banner: Active Milestones**

| Milestone | Target Scope | Current Status | Primary Deliverable |
| :--- | :--- | :---: | :--- |
| **Milestone 1** | Data Description - Machine Learning | `COMPLETED` | Commit `cc1c33d` (Sept 4, 2026) |
| **Milestone 2** | Chapter 3 Methodology Revisions | `IN PROGRESS` | Audit complete; awaiting LaTeX & README updates |
| **Milestone 3** | Chapter 4 Initial Model Training & Hyperparameters | `IN PROGRESS` | Instructions archived; audit complete |

---

## **1. Author Profiles & Collaboration Roles**

* **Yahyah Odin ("Yah")**: Lead technical author focusing on machine learning modeling, retrieval benchmarking, paper drafting, and script automation.
* **Ralph Paolo Dulce ("Ralph")**: Co-author leading human evaluation deployment, Sangguniang Panlungsod administrative communication, Google Forms, and annotator guidebook.

> *Note for Assistant Execution:* When Yah is present, execute technical tasks directly and update this tracker. When Ralph is present, greet Ralph with a briefing of recent progress and highlight Ralph's assigned action items.

---

## **2. Canonical System Environment Reference Card**

*Local workstation environment simulating Philippine Local Government Unit (LGU) IT capacity. Cited across all methodology sections and reproducibility guides.*

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

## **3. Verbatim Milestone Instructions Archive**

### **Milestone 1: Data Description - Machine Learning**
* **Status:** `COMPLETED` (Completed on September 4, 2026; Commit `cc1c33d`).
* **Summary:** Integrated corpus breakdown (25,432 national laws, ~1,660 local ordinances), static 70/15/15 split, initial overfitting regularization (AdamW, dropout, early stopping), and initial Overleaf preview configuration.

---

### **Milestone 2: Methodology Revisions**
* **Status:** `ACTIVE / IN PROGRESS`
* **Official Prompt Provided by Course Professor (Verbatim):**

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

### **Milestone 3: Results and Discussion (Initial Model Training & Hyperparameters)**
* **Status:** `ACTIVE / IN PROGRESS`
* **Official Prompt Provided by Course Professor (Verbatim):**

> *"Present your first set of concrete experimental results and provide explanations of what these results mean in Chapter 4: Results and Discussion. Present your preliminary data using structured tables and plots (i.e., boxplots, line graphs). Raw and unformatted output is not acceptable.*
>
> *Machine Learning*
>
> *You should have trained your initial models and began optimising their internal configurations. This should include the hyperparameter you tuned (e.g., learning rate, network depth, batch size). For each parameter, state the search range and the method used. Also include the training/validation loss curves over time. Report the performance of the best-performing hyperparameter configurations on your validation set. Analyze the training patterns and discuss underfitting/overfitting and hyperparameter sensitivity."*

---

## **4. Master Priority Task Checklist (By Author)**

### **A. Yah's Core Action Items**
- [ ] **Sources & Citations Audit**: Add verified sources on statements/sections that still need citations (Yah will instruct on specific sentences; requires full text reading). `(Yah)`
- [ ] **Finalize Ground Truth Sentences**: Polish and finalize the 350 ground truth premise-hypothesis sentences, strongly adding authoritative legal sources per professor consultation. `(Yah)`
- [ ] **Migrate Experiments from Chapter 3 to Chapter 4**: Move actual experimental evaluations and results (e.g., Stage 1 full-corpus and ablation benchmarks) from `methodology.tex` to `results_and_discussion.tex`, while retaining Exploratory Data Analysis (EDA) and corpus distributions in Chapter 3. `(Yah)`
- [ ] **Conceptual Framework Recheck**: Recheck and update Section 3.1 Conceptual Framework (Input-Process-Output and Phase 1 vs. Phase 2 live architecture). `(Yah)`
- [ ] **Executive Orders (EO) Policy Debate**: Debate whether to continue including Executive Orders given their subordinate legal power compared to Republic Acts; decide whether to exclude EOs from the corpus and recalculate statistics/figures accordingly. `(Yah)`
- [ ] **Execute Milestone 2 Revisions**: Integrate Hardware/Software specs, GitHub URL, Stage 2 baseline, Hyperparameter Grid table, and McNemar/Friedman equations into Chapter 3; add Minimal Working Example (MWE) to `README.md`. `(Yah)`
- [ ] **Execute Milestone 3 ML Training & Chapter 4**: Train initial Cross-Encoder models, record loss curves, optimize hyperparameters, generate plots/tables, and draft Chapter 4. `(Yah)`
- [ ] **Polish Visuals**: Update and enhance publication tables and figures for aesthetic and structural consistency. `(Yah)`
- [ ] **Search Candidate Models for Stage 2**: Identify additional ideal open-weight candidate models suitable for edge Cross-Encoder fine-tuning on 8GB VRAM. `(Yah)`
- [ ] **Pseudocode & Appendix Preparation**: Add formal algorithms/pseudocode and source listings into the manuscript Appendix once each pipeline module is fully polished. `(Yah)`
- [ ] **Front Matter & General Updates**: Update thesis date, acknowledgments, approval sheets, and general front matter. `(Yah)`
- [ ] **Reference Re-confirmation & Verification**: Recheck and reconfirm all bibliography keys for DOI, volume, page, and venue accuracy. `(Yah)`
- [ ] **Download Reference PDFs**: Attempt to download PDFs of all cited references to assemble a complete local reference library for full context. `(Yah)`
- [ ] **Web Prototype Design**: Begin UI/UX design and implementation of the single-page prototype web interface for LGU First Reading review. `(Yah)`

### **B. Ralph's Core Action Items**
- [ ] **Google Forms Deployment**: Construct Google Forms for the Ground Truth evaluation based on the master review workbook (Set A to Set E, 70 pairs each, Section 1 branching). `(Ralph)`
- [ ] **Draft Sangguniang Panlungsod Email**: Draft formal correspondence to the Davao City Sangguniang Panlungsod requesting the 15 legal researcher annotators and explaining their role. `(Ralph)`
- [ ] **Annotator Guidebook PDF**: Compile a clean, accessible PDF reference guide for legal researchers based on `docs/annotation/sp_annotation_cheat_sheet.md`. `(Ralph)`
- [ ] **Local Ordinances EDA (Shared with Yah)**: Expand Chapter 3 with exploratory data analysis of the ~1,660 scanned local ordinances, including digitization quality, year distribution, and word count statistics. `(Ralph / Yah)`

---

## **5. Milestone-by-Milestone Granular Checklist**

### **Milestone 2 Deliverables (Chapter 3 Methodology)**
- [x] **Audit current manuscript against Milestone 2 instructions**.
- [ ] **Hardware & Software Specifications (§3.5)**: Insert exact specs (i3-10105F, RX 6600 8GB, 8GB RAM, Windows 10, Python 3.10+, PyTorch, Transformers) with publication `booktabs` table.
- [ ] **Version Control & Reproducibility (§3.5 / §3.8)**: Add subsection with GitHub URL (`https://github.com/yyaahhzxc/thesis-repo`) and commit hash reproducibility protocol.
- [ ] **README Minimal Working Example**: Add a dedicated `## Minimal Working Example (MWE)` section to `README.md` with a 1-command executable script.
- [ ] **Baseline Selection & Justification (§3.6)**: Document Stage 1 baseline (BM25 from Wu et al., 2025 AIIR) and Stage 2 baseline (standard zero-shot Cross-Encoder / COLIEE Task 4 baseline from Rabelo et al., 2022).
- [x] **Evaluation Metrics (§3.7)**: Recall@k, MRR@k, Class F1, Macro F1, cost-sensitive $F_2$-score ($\tau^*$ calibration).
- [ ] **Hyperparameter Tuning Strategy (§3.6.1)**: Formally declare Grid Search method; tabulate Fixed vs. Variable hyperparameters with search bounds.
- [ ] **Statistical Model Comparison (§3.7.3)**: Add McNemar's Test (paired 2x2 contingency table, $\chi^2$ equation with continuity correction) and Friedman Test ($\chi_F^2$ equation, Wilcoxon signed-rank post-hoc).
- [ ] **Overleaf-LaTeX Compilation**: Recompile full manuscript via `python scripts/build_paper.py` (0 errors).

---

### **Milestone 3 Deliverables (Chapter 4 Results & Discussion)**
- [ ] **Initialize Chapter 4 Structure**: Create `CS_Undergraduate_Thesis_Template/chapters/results_and_discussion.tex` and register `\include{chapters/results_and_discussion}` in `main.tex`.
- [ ] **Migrate Stage 1 Results to Chapter 4**: Relocate Table 3.7 (Full-Corpus BM25 Benchmark) and Table 3.8 (9-Model Candidate Ablation Benchmark) from Chapter 3 to Chapter 4.
- [ ] **Initial Stage 2 Model Fine-Tuning Execution**:
  - [ ] Fine-tune initial Cross-Encoder models (`all-MiniLM-L6-v2`, `deberta-v3-base`, `ModernBERT-base`) on the 245 training pairs.
  - [ ] Track training loss and validation loss across epochs ($E = 1 \dots 10$).
  - [ ] Implement early stopping and model checkpointing based on validation Macro $F_1$.
- [ ] **Hyperparameter Tuning Runs**:
  - [ ] Search learning rates $\eta \in \{1\times 10^{-5}, 2\times 10^{-5}, 3\times 10^{-5}, 5\times 10^{-5}\}$.
  - [ ] Search batch sizes $B \in \{8, 16\}$.
  - [ ] Search maximum sequence lengths $L \in \{256, 512\}$.
- [ ] **Loss Curves & Visualizations**:
  - [ ] Generate line graphs showing training and validation loss curves over time/epochs.
  - [ ] Generate boxplots or bar charts of validation F1 across hyperparameter runs.
- [ ] **Underfitting/Overfitting & Sensitivity Analysis**:
  - [ ] Draft narrative in Chapter 4 analyzing the convergence patterns of candidate encoders.
  - [ ] Discuss sensitivity to learning rate and the regularization effect of AdamW ($\lambda=0.01$) and dropout ($p=0.10$).
- [ ] **Validation Performance Reporting**: Report best-performing hyperparameter configurations on the 52 validation pairs using publication `booktabs` tables.

---

## **6. Chronological Progress Journal**

| Date | Author | Scope | Actions Accomplished | References / Files |
| :--- | :---: | :---: | :--- | :--- |
| **2026-09-04** | Yah | Milestone 1 | Completed Milestone 1 (Data Description - Machine Learning); integrated train/val/test splits and overfitting controls. | Commit `cc1c33d` |
| **2026-09-05** | Yah | Ground Truth | Generated 350-pair Ground Truth benchmark; Cohen's power analysis ($w=0.30$); SP workload allocation formulas. | Commit `a17b67b` |
| **2026-09-06** | Yah | Methodology | Restructured Chapter 3 into chronological 11-section pipeline; added full-corpus and 9-model retrieval benchmarks. | Commit `4963bcf`, `77236f3` |
| **2026-09-08** | Yah | Token Census | Completed token length census across 164,620 sections; formulated cost-sensitive threshold $\tau^*$ via $F_2$-score. | Commit `0804727` |
| **2026-09-11** | Yah | Literature | Integrated COLIEE 2026 proceedings; analyzed affirmative bias phenomenon; contrasted edge vs cloud models. | Commit `483e15c` |
| **2026-09-15** | Yah | Milestone 2 | Audited thesis against Milestone 2 instructions; established master task tracker and agent continuity rule. | Commit `a3f592c` |
| **2026-09-15** | Yah | Milestone 3 | Archived Milestone 3 prompt; logged Yah and Ralph task distributions; updated agent rules for author identification. | Current Turn |
