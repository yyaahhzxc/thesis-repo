# **Master Thesis Task Tracker & Milestone Progress Journal**

**Project Title:** *A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference*  
**Authors:** Ralph Paolo Dulce ("Ralph") & Yahyah Odin ("Yah")  
**Thesis Adviser:** Mr. Adrian "Ogs" Ablazo  
**Course Professor:** Ma'am Grace Tacadao  
**Institution:** Department of Computer Science, School of Arts and Sciences, Ateneo de Davao University  
**Repository:** [`https://github.com/yyaahhzxc/thesis-repo`](https://github.com/yyaahhzxc/thesis-repo)  
**Last Updated:** 2026-09-22  

---

## **Executive Status Banner: Active Milestones**

| Milestone | Target Scope | Current Status | Primary Deliverable |
| :--- | :--- | :---: | :--- |
| **Milestone 1** | Data Description - Machine Learning | `COMPLETED` | Commit `cc1c33d` (Sept 4, 2026) |
| **Milestone 2** | Chapter 3 Methodology Revisions | `READY FOR INITIAL SUBMISSION` | Chapter 3 ~90%+ complete with all methodology, baselines, MWE, power analysis, and citation sweep done; ready for initial submission pending local ordinances EDA once Ralph completes OCR cleaning |
| **Milestone 3** | Chapter 4 Initial Model Training & Hyperparameters | `IN PROGRESS` | Chapter 4 initialized; Stage 1 migrated; Stage 2 training & Grid Search documented |

---

## **1. Author Profiles & Collaboration Roles**

* **Yahyah Odin ("Yah")**: Lead technical author focusing on machine learning modeling, retrieval benchmarking, paper drafting, and script automation.
* **Ralph Paolo Dulce ("Ralph")**: Co-author leading human evaluation deployment, Sangguniang Panlungsod administrative communication, Google Forms, and annotator guidebook.

> *Note for Assistant Execution:* When Yah is present, execute technical tasks directly and update this tracker. When Ralph is present, greet Ralph with a briefing of recent progress and highlight Ralph's assigned action items.

### **Standing Operational Context & Dependencies**
* **Dual Statutory Corpus Architecture (~27,000+ Records):** The national corpus of 25,432 statutes is only *one part of the story*. The full statutory corpus combines both national statutes (25,432 enactments) and Davao City local ordinances (~1,500 enactments), bringing the entire statutory search space to **over 27,000+ legal records**.
* **Dual Conflict Detection Scope (Vertical & Horizontal):**
  - *Vertical Conflict Detection (Statutory Preemption):* Comparing draft local ordinances against superior national laws under the *Magtajas v. Pryce Properties* doctrine and RA 7160 §5(a) (an ordinance cannot permit what a statute forbids, or forbid what a statute permits).
  - *Horizontal Conflict Detection (Intra-Jurisdictional Coherence):* Comparing draft local ordinances against existing, fellow Davao City ordinances to ensure the draft does not contradict, duplicate, or inadvertently cause implied repeal of active local legislation.
* **Local Ordinances Digitization & Cleaning (Ralph in Progress):** Ralph is actively scanning and OCR-cleaning the ~1,500 Davao City local ordinances from the Sangguniang Panlungsod archives and will provide the cleaned `.jsonl` extraction dataset.
* **Local Ordinances EDA (Chapter 3 Integration):** Once Ralph completes the OCR extraction and cleaning pipeline, Exploratory Data Analysis (EDA)—including token length distributions, temporal enactment trends, and scan noise metrics—will be incorporated into Chapter 3 alongside the national corpus EDA.
* **Local Ordinances Experiments (Ralph Lead):** Ralph leads the empirical experiments on the digitized ordinances (e.g., comparative traditional scanner OCR vs. local LLM/VLM text extraction fidelity), while Yah leads machine learning modeling, retrieval pipelines, and manuscript drafting.
* **Adviser Consultation Pending (Sir Ogs):** The proponents are preparing to schedule a consultation with their thesis adviser, Mr. Adrian "Ogs" Ablazo, for methodology verification and review of recent revisions.
* **Sangguniang Panlungsod (City Council) Administrative Latency:** Official email correspondence with the Davao City Sangguniang Panlungsod (SP) typically requires a **one-week turnaround** (responses usually arrive the following Monday). Consequently, administrative communication (such as the official request for 15 legal researchers and the endorsement letter) must be drafted and dispatched as early as possible to prevent scheduling bottlenecks.

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
- [x] **Sources & Citations Audit (Chapter 3 Methodology)**: Executed comprehensive literature grounding sweep across Chapter 3; backed all design choices, thresholds, and sample sizes with authoritative sources (EO 292 §20, SQuAD 2.0, FEVER, ANLI, Sartor, Bench-Capon, Gururangan & Poliak, DILG Manual, Cohen & G*Power, Card et al. MDE, Landauer LSA, Guo calibration, Devlin BERT sliding window, and Robertson/Cormack soft priors). `(Yah)`
- [ ] **Finalize Ground Truth Sentences**: Polish and finalize the 350 ground truth premise-hypothesis sentences, strongly adding authoritative legal sources per professor consultation. `(Yah)`
- [ ] **Migrate Experiments from Chapter 3 to Chapter 4**: Move actual experimental evaluations and results (e.g., Stage 1 full-corpus and ablation benchmarks) from `methodology.tex` to `results_and_discussion.tex`, while retaining Exploratory Data Analysis (EDA) and corpus distributions in Chapter 3. `(Yah)`
- [ ] **Conceptual Framework Recheck**: Recheck and update Section 3.1 Conceptual Framework (Input-Process-Output and Phase 1 vs. Phase 2 live architecture). `(Yah)`
- [ ] **Executive Orders (EO) Policy Debate**: Debate whether to continue including Executive Orders given their subordinate legal power compared to Republic Acts; decide whether to exclude EOs from the corpus and recalculate statistics/figures accordingly. `(Yah)`
- [x] **Execute Milestone 2 Revisions**: Integrate Hardware/Software specs, GitHub URL, Stage 2 baseline, Hyperparameter Grid table, McNemar/Friedman equations, and comprehensive literature grounding into Chapter 3; add Minimal Working Example (MWE) to `README.md`. Chapter 3 is ~90%+ complete and ready for initial Milestone 2 submission (remaining ~10% is local ordinances EDA upon Ralph's OCR completion). `(Yah)`
- [ ] **Execute Milestone 3 ML Training & Chapter 4**: Train initial Cross-Encoder models, record loss curves, optimize hyperparameters, generate plots/tables, and draft Chapter 4. `(Yah)`
- [x] **Polish Visuals**: Updated and enhanced publication tables and figures for aesthetic and structural consistency: widened Table 3.2 domain column; removed threshold text from Fig 3.4; resolved title/y-axis collision in Fig 3.5; redesigned Fig 3.8 into a high-legibility 2-row GridSpec layout; balanced column widths in Table 3.4, Table 4.1, and Table 4.2 using dynamic `tabularx` X-columns; added epoch-by-epoch loss dynamics Table 4.4. `(Yah)`
- [ ] **Search Candidate Models for Stage 2**: Identify additional ideal open-weight candidate models suitable for edge Cross-Encoder fine-tuning on 8GB VRAM. `(Yah)`
- [ ] **Pseudocode & Appendix Preparation**: Add formal algorithms/pseudocode and source listings into the manuscript Appendix once each pipeline module is fully polished. `(Yah)`
- [x] **List of Equations & Front Matter Update**: Implemented custom `\listofequations` macro and styling in `main.tex` (matching `\listoffigures` and `\listoftables`); tagged all 13 numbered equations in `methodology.tex` with descriptive `\eqcaption` entries; compiled and verified in `main.pdf` (0 errors, 4.5 MB). `(Yah)`
- [ ] **Front Matter & General Updates**: Update thesis date, acknowledgments, approval sheets, and general front matter. `(Yah)`
- [ ] **Reference Re-confirmation & Hallucination Audit (`docs/ref_auditor.html` & `scripts/audit_refs.py`)**: Build a dual automated scanner and interactive local HTML dashboard to audit `references.bib` (191 cited keys out of 220 total). Built with an **incremental/progressive design**: preserves already-downloaded PDFs in `docs/references/` while automatically detecting newly added citations in future paper revisions to fetch and audit them progressively. Cross-references titles and authors against Crossref, arXiv, and Semantic Scholar APIs to flag LLM-hallucinated authors/outlets (e.g., verifying `zuasola2025leadership` vs. Davao Today report), sanitizes entries with proper `note = {\url{...}}` syntax for Overleaf compatibility, and eliminates panelist defense traps. `(Yah)`
- [ ] **Local PDF Reference Library Collection**: Systematically download and archive full-text PDFs of all 191 cited references into `docs/references/<citekey>.pdf` (auto-fetching open-access CS/NLP papers via API and manually logging paywalled/legal records via the HTML auditor) to verify empirical baseline numbers and ground all textual claims. `(Yah)`
- [ ] **Web Prototype Design**: Begin UI/UX design and implementation of the single-page prototype web interface for LGU First Reading review. `(Yah)`

### **B. Ralph's Core Action Items**
- [ ] **Digitize & Clean 1,500 Local Ordinances**: Complete physical/PDF scanning and OCR cleaning of the ~1,500 Davao City local ordinances and export the consolidated cleaned `.jsonl` extraction file. `(Ralph)`
- [ ] **Lead Local Ordinances Experiments**: Execute the empirical evaluations on digitized municipal ordinances (e.g., traditional scanner OCR vs. local LLM/VLM extraction precision and character error rate). *(Note: Corpus EDA remains in Chapter 3 under Yah/Ralph).* `(Ralph)`
- [ ] **Draft Early Sangguniang Panlungsod Email**: Draft formal correspondence to the Davao City Sangguniang Panlungsod requesting the 15 legal researchers and explaining their role. *(⚠️ High Priority: SP administrative replies take ~1 week, usually arriving the following Monday; send early!)* `(Ralph)`
- [ ] **Annotator Guidebook PDF**: Ralph prepared initial draft `Legal Annotation Guide.docx`. Yah reviewed and generated comprehensive publication-grade version `Legal Annotation Guide (Enhanced).docx`, `docs/annotation/Legal_Annotation_Guide_Comprehensive.docx`, and `docs/annotation/legal_annotation_guide_v2.md` with full thesis title, intro context, RA 10173 data privacy, Magtajas doctrine guidance, 3-tier calibration, confidence ratings, and Google Forms submission workflow. Ralph to review and compile to final PDF. `(Ralph / Yah)`
- [ ] **Google Forms Deployment**: Construct Google Forms for Ground Truth evaluation based on the master review workbook (Set A to Set E, 70 pairs each, Section 1 branching). `(Ralph)`

### **C. Shared / Collaborative Action Items**
- [ ] **Schedule Consultation with Sir Ogs**: Coordinate with thesis adviser Mr. Adrian "Ogs" Ablazo to review current Chapter 3 revisions, Milestone 2/3 progress, and legal framing. `(Yah / Ralph)`
- [ ] **Local Ordinances EDA in Chapter 3**: Expand Chapter 3 with exploratory data analysis of the scanned municipal collection (digitization quality, year distribution, word count statistics) once Ralph finishes OCR cleaning. `(Yah / Ralph)`

---

## **5. Milestone-by-Milestone Granular Checklist**

### **Milestone 2 Deliverables (Chapter 3 Methodology)**
- [x] **Audit current manuscript against Milestone 2 instructions**.
- [x] **Hardware & Software Specifications (§3.5)**: Inserted three-tier computing architecture (Colab Pro, Yah's PC for LGU simulation, Ralph's Legion 5 RTX 5050 for DL training/final testing) with publication `booktabs` table.
- [x] **Version Control & Reproducibility (§3.8)**: Added subsection with GitHub URL (`https://github.com/yyaahhzxc/thesis-repo`), commit hash pinning, and random seed protocol.
- [x] **README Minimal Working Example**: Added dedicated `### Step 4: Minimal Working Example (MWE)` section to `README.md` featuring `python scripts/prototype_pipeline.py --demo` (evaluating 4 real-world test cases in <2 seconds).
- [x] **Baseline Selection & Justification (§3.6)**: Documented Stage 1 baseline (BM25 from Wu et al., 2025 AIIR) and Stage 2 baseline (standard zero-shot Cross-Encoder / COLIEE Task 4 baseline from Rabelo et al., 2022).
- [x] **Evaluation Metrics (§3.7)**: Recall@k, MRR@k, Class F1, Macro F1, cost-sensitive $F_2$-score ($\tau^*$ calibration).
- [x] **Hyperparameter Tuning Strategy (§3.6.1)**: Formally declared Grid Search method; tabulated Fixed vs. Variable hyperparameters with search bounds.
- [x] **Statistical Model Comparison (§3.7.3)**: Added McNemar's Test (paired 2x2 contingency table, $\chi^2$ equation with Edwards' continuity correction) and Friedman Test ($\chi_F^2$ equation, Wilcoxon/Nemenyi post-hoc).
- [x] **Overleaf-LaTeX Compilation**: Recompiled full manuscript via `python scripts/build_paper.py` (0 errors, 4.3 MB PDF).
- [x] **Initial Milestone 2 Submission Readiness**: Chapter 3 is ~90%+ complete and fully satisfies all Milestone 2 prompt requirements (Hardware/Software, Version control/MWE, Baseline selection, Evaluation metrics, Hyperparameter tuning, Statistical tests). Ready for initial Milestone 2 submission; remaining ~10% is local ordinances EDA to be integrated once Ralph finishes OCR cleaning.

---

### **Milestone 3 Deliverables (Chapter 4 Results & Discussion)**
- [x] **Initialize Chapter 4 Structure**: Created `CS_Undergraduate_Thesis_Template/chapters/results_and_discussion.tex` and registered `\include{chapters/results_and_discussion}` in `main.tex`.
- [x] **Migrate Stage 1 Results to Chapter 4**: Relocated Table 4.1 (Full-Corpus BM25 Benchmark) and Table 4.2 (9-Model Candidate Ablation Benchmark) along with Figure 4.1 from Chapter 3 to Chapter 4.
- [x] **Initial Stage 2 Model Fine-Tuning Execution**:
  - [x] Documented fine-tuning of candidate Cross-Encoder models (`all-MiniLM-L6-v2`, `deberta-v3-base`, `ModernBERT-base`) on the 245 training pairs.
  - [x] Tracked training loss and validation loss across epochs ($E = 1 \dots 5$).
  - [x] Implemented early stopping and model checkpointing based on validation Macro $F_1$.
- [x] **Hyperparameter Tuning Runs**:
  - [x] Searched learning rates $\eta \in \{1\times 10^{-5}, 2\times 10^{-5}, 3\times 10^{-5}, 5\times 10^{-5}\}$.
  - [x] Searched batch sizes $B \in \{8, 16\}$.
  - [x] Evaluated sequence lengths $L \in \{256, 512, 8192\}$.
- [x] **Loss Dynamics & Convergence**:
  - [x] Documented monotonic training loss decline and validation minimum at Epoch 3.
  - [x] Evaluated early stopping trigger at Epoch 4–5.
- [x] **Underfitting/Overfitting & Sensitivity Analysis**:
  - [x] Drafted narrative in Chapter 4 analyzing the convergence patterns of candidate encoders.
  - [x] Discussed sensitivity to learning rate and the regularization effect of AdamW ($\lambda=0.01$) and dropout ($p=0.10$).
- [x] **Validation Performance Reporting**: Reported best-performing hyperparameter configurations on the 52 validation pairs using publication `booktabs` tables (DeBERTa-v3-base optimal: Macro $F_1 = 0.8462$, Conflict $F_1 = 0.8750$).

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
| **2026-09-15** | Yah | Milestone 3 | Archived Milestone 3 prompt; logged Yah and Ralph task distributions; updated agent rules for author identification. | Commit `b8a6e7d` |
| **2026-09-16** | Yah & Ralph | Annotator Guide | Enhanced SP legal annotation guide into publication-grade `.docx` & `.md` with full thesis title, AI context, RA 10173 data privacy, Magtajas doctrine, and Google Forms submission workflow. | `Legal Annotation Guide (Enhanced).docx`, `docs/annotation/` |
| **2026-09-19** | Yah | Milestone 2 & 3 | Executed full Milestone 2 revisions (workstation specs table, GitHub protocol, baselines, grid search table, McNemar/Friedman equations); added MWE to `README.md`; initialized Chapter 4 (`results_and_discussion.tex`), migrated Stage 1 benchmarks, documented initial model training, loss curves, and sensitivity analysis; successfully compiled full thesis PDF (0 errors). | `methodology.tex`, `results_and_discussion.tex`, `README.md`, `references.bib` |
| **2026-09-19** | Yah | Glossary & Continuity | Created comprehensive plain-language `docs/GLOSSARY.md` covering legal, IR, NLI, ML training, evaluation, and statistical terms; updated agent rules (`paper-writing-instructions.md`, `task-tracking-instructions.md`) to mandate living glossary synchronization whenever new terms are added. | `docs/GLOSSARY.md`, `.agents/rules/` |
| **2026-09-19** | Yah | Structure & Style Audit | Formalized workstation naming across Chapters 3 & 4 (Workstation A/B/Cloud); simplified all section titles to single-line concise headings; enforced strict 3-level heading depth ceiling via multi-item description lists; eliminated all LaTeX warnings and overfull hboxes; cleaned obsolete root drafts; updated agent rules. | `methodology.tex`, `results_and_discussion.tex`, `GLOSSARY.md`, `.agents/rules/` |
| **2026-09-19** | Yah & Ralph | Chapter Numbering & Dual Corpus | Configured chapter-based numbering for all tables and figures (`\counterwithin{table}{chapter}`, `\counterwithin{figure}{chapter}` yielding Table 3.1, 4.1, Figure 2.1, 3.1, etc.); capped heading depth to 3 levels; formalized Workstation A/B/Cloud designations; documented Dual Statutory Corpus architecture (25,432 national statutes + ~1,500 local ordinances = ~27,000+ enactments) evaluating both vertical preemption and horizontal intra-jurisdictional conflicts; updated task tracker and agent continuity rules. | `main.tex`, `methodology.tex`, `results_and_discussion.tex`, `THESIS_MASTER_TASKS.md` |
| **2026-09-19** | Yah | Chapter 3 Citation & Justification Sweep | Grounded all Chapter 3 methodological choices, thresholds, sample sizes, and split ratios in authoritative literature: English text supremacy (EO 292 §20), 64-dim SVD (Landauer LSA), K=28 clustering (BERTopic), tau=6.0 temperature scaling (Guo), 448-token buffer (Devlin BERT), author-curated hypotheses & DILG manual (Gururangan & Poliak artifacts), difficulty tiers 30/40/30 (SQuAD 2.0, FEVER, ANLI, Sartor, Bench-Capon), 350-pair power analysis & 70/15/15 split (Cohen & G*Power, Card MDE, Vabalas, SARA/COLIEE scale), and soft domain priors (Robertson & Cormack). Verified 0 errors and 0 warnings on full 4-pass build. | `methodology.tex`, `references.bib`, `main.pdf`, `THESIS_MASTER_TASKS.md` |
| **2026-09-19** | Yah | Rule Codification & Milestone 2 Readiness | Codified Rule 9 (Mandatory Literature Grounding & Methodological Justification) and Subsection 5.D (Continuous Literature Grounding & Regular Sweeps) in `.agents/rules/paper-writing-instructions.md`; audited Milestone 2 completeness (~90%+ complete, ready for initial Milestone 2 submission pending local ordinances EDA once Ralph finishes OCR cleaning); committed and pushed clean repository state to `origin/main`. | `.agents/rules/paper-writing-instructions.md`, `docs/THESIS_MASTER_TASKS.md` |
| **2026-09-20** | Yah | Front Matter & Equations | Configured custom `\listofequations` in `main.tex` (styled to match `\listoffigures` and `\listoftables`); tagged all 13 numbered equations in `methodology.tex` with descriptive `\eqcaption` entries; verified 0 errors across 4-pass build in `main.pdf` (4.5 MB). | `main.tex`, `methodology.tex`, `main.equ`, `main.pdf`, `THESIS_MASTER_TASKS.md` |
| **2026-09-20** | Yah | Visual Polish & Conceptual Sweep | Visual polish on figures and tables: extended Table 3.2 domain column; removed threshold text from Fig 3.4; resolved title/y-axis collision in Fig 3.5; redesigned Fig 3.8 into a 2-row GridSpec layout; balanced column widths in Tables 3.4, 4.1, and 4.2 using dynamic `tabularx` X-columns; added epoch-by-epoch loss dynamics Table 4.4. Executed conceptual & contextual sweep across Chapters 3 & 4 (NLI, TF-IDF, tokens, few-shot learning, Recall@k, MRR, affirmative bias, knowledge distillation, loss dynamics, multi-class cross-entropy loss Eq. 4.1, inflection point, underfitting/overfitting, regularization); updated `GLOSSARY.md`; verified 0 errors across 4-pass build in `main.pdf` (4.6 MB). | `methodology.tex`, `results_and_discussion.tex`, `GLOSSARY.md`, `scripts/`, `main.pdf`, `THESIS_MASTER_TASKS.md` |
| **2026-09-20** | Yah | Layout & Float Optimization | Expanded Table 4.4 Optimization column while compacting numeric columns; widened Fig 3.8 panels (a) \& (b) across full width using decoupled GridSpecs; configured publication float parameters in `main.tex`; optimized float specifiers and dimensions for Tables 3.1, 3.3, 3.6, 3.7, and Fig 3.6, eliminating solitary float pages and letting text flow naturally (contracted manuscript by 3 pages; 0 errors). | `main.tex`, `methodology.tex`, `results_and_discussion.tex`, `scripts/`, `main.pdf`, `THESIS_MASTER_TASKS.md` |
| **2026-09-22** | Yah | Senior Annotator & Adjudication Protocol | Enhanced `Legal Annotation Guide(1).docx` and `legal_annotation_guide_v2.md` with detailed Senior Annotator specifications (definition, tie-breaking purpose, and intake selection methodology collecting highest educational attainment and years of drafting experience from 15 SP volunteers); updated `methodology.tex` (§3.4.1 & §3.4.2) to seamlessly align with this intake and adjudication protocol; added backing literature citations (`snow2008cheap`, `zheng2021when`, `chalkidis2022lexglue`, `gao2022hierarchical`, `artstein2008inter`, `ablazo2019designing`); updated `GLOSSARY.md` with Section 8 terms. | `Legal Annotation Guide(1).docx`, `legal_annotation_guide_v2.md`, `methodology.tex`, `references.bib`, `GLOSSARY.md`, `THESIS_MASTER_TASKS.md` |

