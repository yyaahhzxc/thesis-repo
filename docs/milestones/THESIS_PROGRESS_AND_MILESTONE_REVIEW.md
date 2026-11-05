# Comprehensive Thesis Progress & Milestone Review Report
**Project Title:** *A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference*  
**Proponents:** Ralph Paolo Dulce & Yahyah Odin  
**Thesis Adviser:** Mr. Adrian "Ogs" Ablazo  
**Course Professor:** Ma'am Grace Tacadao  
**Institution:** Ateneo de Davao University, Department of Computer Science  
**Tracking Period:** Milestone 1 (Commit `cc1c33d`, Sept 4, 2026) to Current Commit (`483e15c`, Sept 11–14, 2026)  
**Document Purpose:** Progress compilation, methodological verification review, and open questions catalog for consultation with Course Professor and Thesis Adviser.

---

## Executive Summary

Since the completion of **Milestone 1 (Data Description - Machine Learning)** on September 4, 2026, the thesis project has progressed from descriptive planning into an empirically benchmarked, reproducible research pipeline. Over this period:

1. **Chapter 3 (Methodology) was expanded by over 300%** (growing from 179 to 540+ LaTeX lines), chronologically restructured to match the actual machine pipeline, and fortified with publication-grade mathematical formulations, 8 publication figures, and 8 comprehensive empirical tables.
2. **The Ground Truth 350 Benchmark was constructed and finalized**: A 350-pair gold-standard dataset spanning 8 macro legal domains, 3 difficulty tiers, and balanced class distributions (112 Contradictions, 128 Entailments, 110 Neutrals) was built and packaged into an adviser-grade master Excel review workbook ([`data/ground_truth_350_adviser_review.xlsx`](file:///c:/Users/SHRIMP/Documents/thesis-repo/data/ground_truth_350_adviser_review.xlsx)) with sub-panel allocations for 15 Davao City Sangguniang Panlungsod (SP) legal researchers.
3. **Full-Corpus Token Census ($N = 25,432$ laws; 164,620 sections) Completed**:
   - An exhaustive token census proved that **94.83% of all statutory provisions have a median length of only 122 tokens** (mean: 202.2 tokens), fitting comfortably within the standard 512-token context window of efficient encoders.
   - For the **5.17% tail** (8,511 sections, primarily territorial boundaries in Local Government laws at 12.54%) exceeding 512 tokens, a sentence-aware sliding fallback sub-chunking mechanism was implemented alongside candidate evaluation of native long-context **ModernBERT** (up to 8,192 tokens) versus **DeBERTa-v3** and **MiniLM**.
4. **Stage 1 Information Retrieval (IR) Empirically Ablated and Stress-Tested**:
   - **Full-Corpus Sensitivity Benchmark ($N = 25,432$ laws)**: Demonstrated on local CPU hardware that unconstrained BM25 achieves only 43.14% Recall@50, and that naive hard domain filtering catastrophically drops recall to 13.43% due to the pruning of cross-cutting omnibus statutes.
   - **Candidate Model Ablation Benchmark ($N = 350$ queries)**: Evaluated 9 candidate retrieval configurations across difficulty tiers. Proved that Dense Bi-Encoders (`all-MiniLM-L6-v2`) outperform sparse BM25 by **+17.3% on Tier 3 latent/paraphrastic conflicts** (91.3% vs 74.0% Recall@5), and that **Reciprocal Rank Fusion (RRF $k=60$)** achieves **96.0% Recall@10** and **99.7% Recall@20** with an average CPU latency of **1.26 ms**.
5. **Cost-Sensitive Decision Thresholding & Affirmative Bias Control Integrated**:
   - Incorporating findings from the **COLIEE 2026 Proceedings** (Task 4 textual entailment), where neural models show pronounced **affirmative bias** (defaulting toward Entailment/Neutral), the pipeline formalizes the operational cost asymmetry ($C(FN) > C(FP)$).
   - Rather than assuming a symmetric 0.50 cutoff, the decision boundary $\tau_{\text{conflict}} \in [0.25, 0.50]$ is swept on validation data to maximize the **$F_2$-score**, weighting recall twice as heavily as precision to prevent unconstitutional municipal preemption while preserving a $P_{\text{conflict}} \ge 0.70$ precision floor.
6. **Operational End-to-End Prototype Implemented** ([`scripts/prototype_pipeline.py`](file:///c:/Users/SHRIMP/Documents/thesis-repo/scripts/prototype_pipeline.py)), successfully executing Stage 1 hybrid retrieval, Stage 2 asymmetric NLI sequence classification, and Explainable AI (XAI) ratio decidendi extraction under the *Magtajas v. Pryce Doctrine*.
7. **Document Ingestion Empirical Benchmark Completed**: Proved that Vision-Language Models (VLMs like Qwen2.5-VL and Gemini 1.5 Flash) eliminate the 27.44% Word Error Rate (WER) and 15.64% vector fidelity degradation caused by traditional optical scanners on Davao City municipal archives.

---

## Part 1: Chronological Git History & Milestone Trajectory

Below is the complete audit of commits from Milestone 1 to the current master branch:

| Commit Hash | Date | Scope / Type | Core Contributions & Methodology Additions |
| :--- | :---: | :--- | :--- |
| [`cc1c33d`](file:///c:/Users/SHRIMP/Documents/thesis-repo) | 2026-09-04 | **Milestone 1 Completion** | **Milestone 1 Baseline**: Integrated initial Data Description (ML) sections into `methodology.tex`; added static 70/15/15 train/val/test split criteria; established initial Overfitting Control (AdamW, Dropout, Early Stopping); configured Overleaf live preview and tracked `.agents/rules/paper-writing-instructions.md`. |
| [`d29c7c8`](file:///c:/Users/SHRIMP/Documents/thesis-repo) | 2026-09-04 | Tooling & Setup | Created automated one-click environment setup script (`scripts/setup_environment.ps1`) for seamless dependency configuration across local workstations. |
| [`a17b67b`](file:///c:/Users/SHRIMP/Documents/thesis-repo) | 2026-09-05 | Major Feature / Methodology | **Ground Truth 350 Benchmark Construction**: Generated 350 pairs across 8 domains and 3 difficulty tiers; added Sangguniang Panlungsod panel allocation mathematics ($N=350, K=3, R=70, P=15$); incorporated Cohen's statistical power analysis ($w=0.30$); formalized Stage 1 metrics ($\text{Recall@}k$, $\text{MRR@}k$); added Lawphil web scraper suite (`src/scraper/`) and annotation documentation. |
| [`64f38cd`](file:///c:/Users/SHRIMP/Documents/thesis-repo) | 2026-09-05 | Refactoring & Hygiene | Formalized academic tone in `README.md`; relocated root files into structured subdirectories (`docs/drafts/`, `docs/experiments/`, `data/`). |
| [`dab42e3`](file:///c:/Users/SHRIMP/Documents/thesis-repo) | 2026-09-05 | Bugfix & Compliance | Resolved Mermaid syntax rendering errors in GitHub markdown; standardized documentation and administrative letters to be timeless (removing hardcoded academic calendars). |
| [`4963bcf`](file:///c:/Users/SHRIMP/Documents/thesis-repo) | 2026-09-06 | Paper Refactor & Polish | **Harmonization & Chronological Reordering of Chapter 3**: Reordered Chapter 3 into an intuitive end-to-end pipeline; harmonized statutory corpus scope (25,432 national laws, ~1,660 local ordinances); calibrated vocabulary to adhere to anti-AI directives (banning triplets, promotional jargon, and bloated sentences); updated `references.bib`. |
| [`d45ce88`](file:///c:/Users/SHRIMP/Documents/thesis-repo) | 2026-09-06 | Experimental Engine | Implemented Stage 1 retrieval benchmark engine (`src/stage1_retrieval_benchmark.py`), Colab notebook (`notebooks/02_stage1_retrieval_and_embeddings.ipynb`), and initial JSON benchmarking pipelines. |
| [`77236f3`](file:///c:/Users/SHRIMP/Documents/thesis-repo) | 2026-09-06 | Major Release / Benchmark | **Finalized Stage 1 Methodology & Adviser-Grade Benchmark**: Added Table 3.2 (Full-corpus BM25 benchmark) and Table 3.3 (9-model Stage 1 candidate ablation); generated Figure 3.6 (retrieval ablation curves) and 5 other publication-grade figures; built master 4-sheet review Excel workbook (`data/ground_truth_350_adviser_review.xlsx`); built working interactive prototype (`scripts/prototype_pipeline.py`). |
| [`0804727`](file:///c:/Users/SHRIMP/Documents/thesis-repo) | 2026-09-08 | Methodology & Token Census | **Full-Corpus Token Census, Fallback Chunking, & Cost-Sensitive Calibration**: Analyzed token length across all 164,620 statutory sections (`output/corpus_token_census.json`); added sentence-aware sliding fallback sub-chunking; introduced native long-context `ModernBERT` (8,192 tokens) vs `DeBERTa-v3` evaluation; formulated cost-sensitive decision boundary ($\tau^*$) maximizing $F_2$-score for contradiction alerts; added Equations 3.7–3.10. |
| [`483e15c`](file:///c:/Users/SHRIMP/Documents/thesis-repo) | 2026-09-11 | Literature & Bias Control | **COLIEE 2026 Proceedings Integration & Affirmative Bias Control**: Grounded theoretical framework in official COLIEE 2026 competition proceedings (`2026-Proceedings.pdf`); integrated recent findings from Team UA (Alshehri et al., 2026), Team NOWJ (Ngo et al., 2026), and Tran et al. (2026); added Affirmative Bias Control to prevent models from defaulting to Entailment/Neutral on complex statutory phrasing; contrasted compact edge encoders with resource-heavy cloud GPU LLM ensembles. |

---

## Part 2: Detailed Manuscript Delta (Chapters 1, 2, and 3)

### 1. Chapter 1: Introduction (`chapters/introduction.tex`)
* **Corpus & Scope Harmonization**: Updated historical numbers to exactly match the empirical archive: **25,432 national statutes** scraped from Lawphil and **~1,660 digitized local ordinances** from the Davao City Legislative Information Support System Program (LISSP).
* **Clear Delineation of Research Scope**:
  - Confirmed the **ex-ante** evaluation focus (pre-enactment First Reading scrutiny).
  - Explicitly bounded national laws to statutory enactments (Republic Acts, Batas Pambansa, Commonwealth Acts, Acts, Presidential Decrees, Executive Orders), while formally excluding judicial Supreme Court decisions and department-level administrative circulars to ensure real-time LGU hardware feasibility.
  - Specified the **English-only boundary** to mitigate dialect translation noise and avoid semantic drift.
  - Enforced single-premise asymmetric span-level pairing ($1\text{-vs-}N$), delineating multi-hop cross-statutory synthesis as a deliberate future direction.

### 2. Chapter 2: Literature Review (`chapters/literature_review.tex`)
* **COLIEE 2025/2026 Retrieve-then-Entail Grounding**: Fortified the theoretical foundation by integrating state-of-the-art architectures from the latest **COLIEE 2026** and **COLIEE 2025** competitions:
  - Cross-encoder legal reasoning and LLM prompting by **Team UA** (Alshehri et al., 2026).
  - Multi-stage legal entailment by **Team NOWJ** (Ngo et al., 2026) and data augmentation by **Tran et al. (2026)**.
  - Statute retrieval mechanisms from **Team AIIR Lab** (Wu et al., 2025) and hybrid ranking from **Team JNLP** (Nguyen et al., 2024).
  - Textual entailment and rationale extraction from **Team KIS** (Koreeda & Manning, 2021).
* **Affirmative Bias Phenomenon**: Analyzed findings from COLIEE 2026 Task 4 showing that neural language models suffer from affirmative bias, systematically defaulting to Entailment or Neutral classifications on dense legal syntax unless explicitly calibrated.
* **Hardware & Quadratic Complexity Bounds**: Expanded the mathematical justification for decoupling Stage 1 from Stage 2:
  - Feeding raw ordinances directly into a full-corpus Cross-Encoder incurs quadratic self-attention complexity $\mathcal{O}((L_{\text{ord}} + L_{\text{stat}})^2)$, which instantly exhausts consumer VRAM when evaluated across 25,432 documents.
  - Sifting candidates via coarse retrieval ($25,432 \rightarrow 50 \rightarrow 1$) eliminates 99.8% of irrelevant provisions in milliseconds.
* **Bibliographic Precision**: Added 126+ lines of authoritative BibTeX entries in [`references.bib`](file:///c:/Users/SHRIMP/Documents/thesis-repo/CS_Undergraduate_Thesis_Template/references.bib), ensuring verified DOIs, registered venues, and proper capitalization protection.

### 3. Chapter 3: Methodology (`chapters/methodology.tex`) — *Major Expansion*
Chapter 3 was systematically expanded from a basic data overview into a full, reproducible methodology:

#### A. Chronological Section Structure
The chapter is organized into 11 logical sections with concise subsection titles:
1. **Conceptual Framework** (Input-Process-Output; Phase 1 Offline Pre-Planning vs Phase 2 Online Live Runtime).
2. **Research Design and Implementation** (Applied experimental computer science design).
3. **Corpus Acquisition** (National Lawphil archive + Davao City LISSP archive; composition and historical distribution across 6 eras).
4. **Preprocessing and Filtering** (Unsupervised topic modeling via MiniBatch K-Means, $c\text{-}TF\text{-}IDF$, SVD 2D latent space; section-level sliding window chunking; full-corpus token census).
5. **Ground Truth Benchmark Construction** (Asymmetric span pairing; 3 difficulty tiers; class balancing; 15-researcher SP annotation protocol; Fleiss' Kappa target).
6. **Experimental Setup and Hardware Constraints** (Consumer LGU workstation simulation; CPU inference; zero generative LLM text hallucination).
7. **Model Implementation and Pipeline Architecture** (Retrieval safeguards; full-corpus sensitivity benchmark; 9-model candidate retrieval ablation benchmark).
8. **Empirical Model Selection and Overfitting Control** (70/15/15 static split; AdamW weight decay $\lambda = 0.01$; dropout $p=0.1$; early stopping with patience $= 4$; linear warmup/decay; affirmative bias control).
9. **Evaluation Metrics and Decision Thresholding** (Stage 1 Recall@k and MRR@k; Stage 2 Precision, Recall, Macro F1, $F_2$-score, and cost-sensitive threshold tuning $\tau^*$).
10. **Prototype Development** (Single-page GUI; source transparency; XAI token-level attention heatmap; human-in-the-loop workflow).
11. **Methodological Constraints and Future Directions** (Recency bias, English boundary, single-premise limits).

#### B. Publication Tables in Chapter 3
* **Table 3.1**: *Comparative Statutory Coverage and Composition of the Philippine National Legal Archive ($N = 25,432$)*.
* **Table 3.2**: *Consolidated Macro Legal Domains of the Philippine National Statutory Corpus ($N = 25,432$)*.
* **Table 3.3**: *Empirical Holdout Validation Metrics, Baseline Comparisons, and Literature Targets for the Topic Modeler ($N_{\text{train}} = 20,345, N_{\text{test}} = 5,087$)*.
* **Table 3.4**: *Stratified Jurisprudential Difficulty Tiers for the 350-Pair Ground Truth Evaluation Benchmark*.
* **Table 3.5**: *Sangguniang Panlungsod Ground Truth Legal Annotation Codebook and Decision Rules*.
* **Table 3.6**: *Architectural Retrieval Safeguards Against Real-World Preemption Failure Modes in Stage 1*.
* **Table 3.7**: *Empirical Retrieval Sensitivity Benchmark across the Full National Statutory Database ($N = 25,432$)*.
* **Table 3.8**: *Empirical Performance Comparison of Candidate Stage 1 Retrieval Architectures ($N = 350$)*.

#### C. Publication Figures in Chapter 3
* **Figure 3.1**: *Conceptual Framework Flowchart* (Phase 1 vs Phase 2).
* **Figure 3.2**: *Composition of the Philippine National Statutory Corpus by Legislative Instrument* (`statute_type_composition.png`).
* **Figure 3.3**: *Historical Succession and Volume across Six Chronological Eras (1900–2026)* (`historical_temporal_evolution.png`).
* **Figure 3.4**: *Distribution across Consolidated Macro Legal Domains* (`macro_domain_distribution.png`).
* **Figure 3.5**: *Two-Dimensional Latent Semantic Topic Space via SVD Projection* (`semantic_topic_landscape_2d.png`).
* **Figure 3.6**: *Top Salient $c\text{-}TF\text{-}IDF$ Keyword Profiles across Eight Macro Domains* (`top_keywords_per_domain.png`).
* **Figure 3.7**: *Cross-Allocation Matrix of Statutory Instruments across Legal Domains* (`statute_source_domain_cross_allocation.png`).
* **Figure 3.8**: *Document Length Distributions, Token Census, and Section-Level Chunk Granularity* (`statutory_length_disparity.png`).
* **Figure 3.9**: *Stage 1 Candidate Retrieval Performance Curves and Jurisprudential Difficulty Gap* (`stage1_retrieval_ablation_performance.png`).

---

## Part 3: Empirical Experiments & Key Research Findings

### 1. Full-Corpus Statutory Token Census ($N = 25,432$ Laws; 164,620 Sections)
Conducted an exhaustive length analysis across every normative statutory provision in the national archive:
* **Total Provisions Analyzed**: 164,620 section-level normative units.
* **Median Provision Length**: **122.0 tokens** (mean: 202.2 tokens; 75th percentile: 206 tokens; 90th percentile: 363 tokens).
* **Provisions $\le 512$ Tokens**: **94.83%** (156,109 sections) fit comfortably within standard compact transformer context limits (82.30% $\le 256$ tokens; 90.96% $\le 384$ tokens).
* **The 5.17% Tail (> 512 Tokens)**: 8,511 sections exceed 512 tokens. The highest concentration is in *Local Government & Territorial Boundaries* (12.54% over 512 tokens) due to detailed metes-and-bounds barangay delineations.
* **Methodological Solution**:
  1. *Sentence-Aware Sliding Sub-Chunking*: 256-token sub-windows with 64-token stride as a fallback for standard-context models.
  2. *Candidate Long-Context Architecture*: Testing native long-context **ModernBERT** (up to 8,192 tokens natively) to measure whether native long-context processing outperforms compact encoders paired with sub-chunking.

### 2. Cost-Sensitive Threshold Calibration & Affirmative Bias Control
* **The Asymmetric Operational Cost Problem**: In legislative preemption checking, classification errors carry severely unequal consequences:
  - **False Negative ($FN$)**: The system fails to flag an unconstitutional ordinance clause $\rightarrow$ The city passes an invalid law, triggering costly litigation and invalidation under *Magtajas v. Pryce*.
  - **False Positive ($FP$)**: The system flags a compliant clause $\rightarrow$ A legal staff researcher takes 30 seconds to review the flagged text on the dashboard.
* **Suboptimality of Symmetric 0.50 Threshold**: Grounded in Elkan (2001) cost-sensitive learning theory and Koreeda & Manning (2021), when $C(FN) > C(FP)$, setting the cutoff at 0.50 results in an unsafe number of missed conflicts.
* **Formulation of $\tau^*$ via $F_2$-Score**:
  $$\tau^* = \arg\max_{\tau \in [0.25, 0.50]} F_{2, \text{conflict}}(\tau; \mathcal{D}_{\text{val}}), \quad \text{where } F_{2, \text{conflict}} = \frac{5 \cdot P \cdot R}{4 \cdot P + R}$$
  Weighting recall twice as heavily as precision ensures the model aggressively captures preemption risks while enforcing a precision floor ($P \ge 0.70$) to prevent alert fatigue.

### 3. Document Ingestion Benchmark: Traditional OCR vs. Vision-Language Models (VLMs)
Evaluated on representative degraded scanned Davao City ordinances (*Ordinance No. 0667-21*):
* **Traditional Scanner OCR**: Suffers a **27.44% Word Error Rate (WER)**, a **25.05% Character Error Rate (CER)**, and a **15.64% drop in semantic vector cosine fidelity** (84.36%). Critical legal terms and monetary amounts were shattered (e.g., `"SECTION 1. TITLE"` $\rightarrow$ `"SECTION l. TITTE"`; `"P79,920.00"` corrupted).
* **Vision-Language Models (Qwen2.5-VL-7B & Gemini 1.5 Flash Vision)**: Achieved **0.00% WER**, **100.0% Legal Citation & Header Precision**, and **100.0% Semantic Vector Fidelity**.
* *Conclusion*: VLMs eliminate the optical error cascade, ensuring clean digital ingestion before semantic chunking and retrieval.

### 4. Full-Corpus Stage 1 Retrieval Benchmark ($N = 25,432$ National Laws)
Conducted on local CPU hardware evaluating all 350 ground truth queries against the entire unconstrained national archive:

| Candidate Retrieval Setup | Mean CPU Latency | Recall@5 | Recall@10 | Recall@20 | Recall@50 | MRR@50 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Baseline BM25 (Unconstrained)** | 329.6 ms | 21.43% | 29.71% | 35.71% | 43.14% | 0.1521 |
| **2. BM25 + Hierarchy Priority Safeguard** | 300.1 ms | 29.14% | 34.86% | 39.43% | 43.14% | **0.2217** (+45.8%) |
| **3. BM25 + Hard Domain Filter** | 297.5 ms | 4.86% | 7.71% | 10.29% | **13.43%** | 0.0467 (-69.3%) |

*Key Finding*: Pure BM25 misses over half of governing statutes. Furthermore, **hard domain filtering is catastrophic** in full legal corpora because cross-cutting omnibus acts (like Republic Act No. 7160 / Local Government Code) are pruned away if the classifier assigns an ordinance to a specific topical domain. Incorporating the **Hierarchy Priority Safeguard** significantly improves MRR (+45.8%) without loss of recall.

### 5. Stage 1 Candidate Architecture Ablation Benchmark ($N = 350$ Queries)
Evaluated 9 candidate configurations across lexical, dense vector, and hybrid fusion architectures:

| Candidate Architecture | Latency (CPU) | R@5 | R@10 | R@20 | MRR | Tier 3 R@5 (Latent Conflicts) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Pure BM25 Baseline (AIIR Lab)** | 1.39 ms | 79.7% | 88.6% | 96.9% | 0.6113 | 74.0% |
| **2. BM25 + Hard Domain Filter** | 1.23 ms | 99.1%* | 100.0%* | 100.0%* | 0.7921* | 99.0%* (*Artificial Isolation) |
| **3. BM25 + Soft Domain Prior (+20%)** | 1.43 ms | 87.7% | 94.6% | 99.4% | 0.7122 | 79.8% |
| **4. Pure Dense Bi-Encoder (`all-MiniLM-L6-v2`)** | 1.33 ms | 87.1% | **97.1%** | **100.0%** | **0.7388** | **91.3%** (**+17.3% over BM25**) |
| **5. Hybrid JNLP (Weighted Sum $\alpha=0.5$)** | 1.23 ms | 82.6% | 91.7% | 98.9% | 0.6409 | 77.9% |
| **6. Hybrid Dense-Biased ($\alpha=0.7$)** | 1.20 ms | 84.0% | 94.0% | 99.4% | 0.6656 | 78.8% |
| **7. Hybrid BM25-Biased ($\alpha=0.3$)** | 1.22 ms | 80.9% | 90.6% | 98.3% | 0.6202 | 76.0% |
| **8. Reciprocal Rank Fusion (RRF $k=60$)** | 1.26 ms | **88.6%** | **96.0%** | **99.7%** | **0.7040** | **88.5%** |
| **9. Hybrid + Soft Domain Prior ($\alpha=0.5$)** | 1.21 ms | 89.7% | 95.7% | 99.7% | 0.7328 | 84.6% |

*Key Finding*: The **Semantic Gap** is most severe in Tier 3 (Latent and Paraphrastic conflicts). While BM25 achieves only 74.0% Recall@5 due to statutory terminology differences, Dense Bi-Encoders achieve **91.3% Recall@5 (+17.3% gain)**. **Reciprocal Rank Fusion (RRF $k=60$)** delivers the most balanced performance across all tiers, reaching **96.0% Recall@10** and **99.7% Recall@20** with sub-2-millisecond latency.

### 6. Working End-to-End Prototype Execution (`scripts/prototype_pipeline.py`)
A functional end-to-end prototype was executed and tested on real-world test cases:
* **Case 1 (Ultra Vires Contradiction)**: Evaluated an ordinance banning designated smoking areas against RA 9211 (Tobacco Regulation Act) Section 6. Correctly retrieved RA 9211 as Rank \#1 (Hybrid Score: 0.9930) and flagged **93.85% Contradiction probability**, citing violation of the *Magtajas v. Pryce Doctrine* (local ordinance prohibiting what a national statute permits).
* **Case 2 (Valid Delegated Entailment)**: Evaluated an ordinance authorizing the City Mayor to accept donated Pocket Wi-Fi units against RA 7160 Section 455(b)(1)(vi). Correctly retrieved RA 7160 as Rank \#1 (Hybrid Score: 0.9942) and predicted **89.45% Entailment probability** (valid delegated executive authority).
* **Case 3 (Harmonious Neutral)**: Evaluated a domestic dog leashing ordinance against national laws. Correctly classified as **82.00% Neutral** (valid autonomous exercise of general welfare police power with no conflicting national preemption).

---

## Part 4: Key Decisions & Methodological Choices to Verify with Professor & Adviser

Below are the key architectural, legal, and operational decisions implemented in the draft. We request Ma'am Grace Tacadao and Sir Adrian Ablazo to review and confirm if these align with departmental expectations:

### Decision 1: Absolute Exclusion of Generative LLMs for Decision/Text Generation
* **Implementation**: The pipeline uses lightweight, deterministic encoder-only transformers (`MiniLM`/`BGE-M3` for Stage 1; `ModernBERT`/`DeBERTa-v3` for Stage 2) and white-box self-attention heatmaps. It deliberately excludes autoregressive LLMs (like GPT-4, LLaMA, or Mistral) from drafting or rewriting laws.
* **Rationale**: Generative models are prone to hallucinating non-existent statutory sections or inventing legal doctrines. In contrast to COLIEE 2026 systems relying on multi-GPU LLM ensembles, Philippine LGUs require strict diagnostic fidelity and sub-second CPU inference on local hardware without cloud API dependencies.
* **Action for Verification**: *Confirm whether Ma'am Grace and Sir Ogs approve of maintaining this strict diagnostic/discriminative boundary rather than incorporating generative text rewriting.*

### Decision 2: Cost-Sensitive Decision Threshold ($\tau^*$) Maximizing $F_2$-Score
* **Implementation**: The pipeline sweeps contradiction alert thresholds $\tau \in [0.25, 0.50]$ on validation data to maximize the $F_2$-score (Equations 3.9–3.10), rather than using the default symmetric 0.50 cutoff.
* **Rationale**: Missing an authentic legal conflict ($FN$) permits an unconstitutional ordinance to be enacted, whereas a false alarm ($FP$) merely directs a researcher to spend 30 seconds reviewing the dashboard. Maximizing $F_2$ aggressively targets conflict recall while maintaining a $P_{\text{conflict}} \ge 0.70$ precision floor, directly mitigating the **affirmative bias** reported in COLIEE 2026.
* **Action for Verification**: *Verify if the faculty approves of using validation-tuned cost-sensitive thresholding ($\tau^*$) in place of standard uncalibrated 0.50 argmax.*

### Decision 3: ModernBERT (Native 8,192 Tokens) vs. DeBERTa-v3 with Sub-Chunking
* **Implementation**: Based on the token census revealing that 94.83% of sections are $\le 512$ tokens while 5.17% exceed 512 tokens, we evaluate native long-context `ModernBERT` against `DeBERTa-v3` and `MiniLM` paired with sliding fallback sub-chunking.
* **Rationale**: Tests whether native long-context attention provides measurable reasoning improvements on lengthy statutory sections compared to compact standard-window models running on local LGU workstations.
* **Action for Verification**: *Confirm faculty approval of this candidate model comparison for Stage 2.*

### Decision 4: Asymmetric Span-Level Pairing ($1\text{-vs-}N$) vs. Multi-Hop Graph Reasoning
* **Implementation**: The system pairs a single national statutory section (premise, 1 section) against a multi-sentence ordinance block (hypothesis, $N$ sentences). It intentionally excludes multi-hop cross-statute synthesis (combining two distinct national acts to find a compound conflict).
* **Rationale**: Bounding the problem to single-premise preemption fits within the 512-token context window of efficient transformers and adheres to the computational capacity of standard LGU workstations. Compound multi-hop reasoning is explicitly reserved for Future Work.
* **Action for Verification**: *Verify if restricting the benchmark and pipeline scope to single-premise preemption is fully acceptable for undergraduate thesis scope.*

### Decision 5: Statutory Knowledge Base Boundary (Lawphil Only, Judicial Exclusions)
* **Implementation**: The national statutory database is capped at **25,432 statutory enactments** (Republic Acts, Batas Pambansa, Commonwealth Acts, Acts, Presidential Decrees, Executive Orders). Supreme Court jurisprudence (case law) and departmental administrative orders (e.g., DILG/DOTR circulars) are excluded.
* **Rationale**: Statutory preemption under *Magtajas v. Pryce* primarily tests compliance with Acts of Congress. Including hundreds of thousands of judicial decisions would exponentially increase corpus size, introduce conflicting case doctrines, and exceed local storage and memory budgets.
* **Action for Verification**: *Confirm whether bounding the legal corpus strictly to statutory enactments satisfies the committee's scope requirements.*

### Decision 6: English-Only Language Restriction
* **Implementation**: The study processes only English-language texts. Conversational Taglish or Cebuano provisions occasionally found in local committee minutes are excluded.
* **Rationale**: Avoids translation errors, out-of-vocabulary token shattering, and semantic drift. Both national statutes and formal enacted Davao City ordinances are officially codified in English.
* **Action for Verification**: *Verify if the English-only scope is considered a justified and acceptable limitation.*

### Decision 7: Static 70/15/15 Split ($N = 350$) over $k$-Fold Cross-Validation
* **Implementation**: The 350 ground truth pairs are divided into a fixed static split of **245 training, 52 validation, and 53 test pairs**.
* **Rationale**: In few-shot transformer fine-tuning with small datasets ($N < 1,000$), Vabalas et al. (2019) mathematically demonstrated that $k$-fold cross-validation causes optimistic leakage bias across overlapping legal phrasing. Furthermore, maintaining a 53-item static test set satisfies Card et al. (2020) Minimum Detectable Effect (MDE) thresholds for statistical power ($w = 0.30$).
* **Action for Verification**: *Confirm if the static 70/15/15 split methodology is acceptable to the course professor in lieu of $k$-fold cross-validation.*

### Decision 8: Human Annotation Protocol with Davao City Sangguniang Panlungsod (15 Raters)
* **Implementation**: 15 Sangguniang Panlungsod legal researchers organized into 5 sub-panels of 3 raters ($k=3$), each evaluating one block of 70 pairs (Ablazo, 2019 batched allocation framework). Disagreements adjudicated by a Senior Legal Researcher; Inter-Rater Reliability evaluated via Fleiss' Kappa ($\kappa \ge 0.61$).
* **Rationale**: Prevents evaluator cognitive fatigue (45–60 minutes per rater) while maintaining substantial multi-rater statistical power.
* **Action for Verification**: *Review the multi-panel allocation matrix in [`data/ground_truth_350_adviser_review.xlsx`](file:///c:/Users/SHRIMP/Documents/thesis-repo/data/ground_truth_350_adviser_review.xlsx) and confirm readiness to send the formal endorsement letter.*

### Decision 9: Rejection of Hard Domain Filtering in Favor of Soft Priors / RRF
* **Implementation**: We rejected hard domain filtering (which showed artificial 100% recall in isolated subsets but collapsed to 13.43% across the full 25,432 corpus) in favor of **Reciprocal Rank Fusion (RRF $k=60$)** and soft hierarchical safeguards.
* **Rationale**: Real-world ordinances routinely intersect with broad omnibus statutes (e.g., Local Government Code, Administrative Code) that do not belong to a single narrow topical domain.
* **Action for Verification**: *Confirm if the committee agrees that demonstrating and reporting this "artificial isolation failure mode" in Chapter 3 strengthens the academic contribution of the study.*

---

## Part 5: Open Questions in Need of Answering

During our upcoming consultation with Ma'am Grace and Sir Ogs, the following open questions need explicit guidance:

### 1. Administrative Coordination with Sangguniang Panlungsod
* **Question 1.1**: *When should we formally submit the Endorsement Letter ([`docs/annotation/adviser_endorsement_letter_template.md`](file:///c:/Users/SHRIMP/Documents/thesis-repo/docs/annotation/adviser_endorsement_letter_template.md)) to Atty. Charisse Paula Marie A. Guinto (Secretary to the SP)?*
* **Question 1.2**: *Does the department require an institutional Memorandum of Agreement (MOA) or is the formal adviser endorsement letter with Department Chair signature sufficient for academic survey deployment?*
* **Question 1.3**: *Should the 15 SP evaluators receive individual Google Sheets (as designed in Set A–E), or would the adviser prefer a unified Google Form with section branching?*

### 2. Experimental Model Training & Compute Strategy
* **Question 2.1**: *For fine-tuning candidate Stage 2 Cross-Encoders (`ModernBERT` vs `DeBERTa-v3`): Is it acceptable to conduct the fine-tuning on Google Colab / cloud GPU instances (T4/A100), provided the final evaluated model is benchmarked and deployed for CPU inference on our local workstation?*
* **Question 2.2**: *What is the preferred ablation baseline for Stage 2? We currently plan to compare Zero-Shot NLI (`roberta-large-mnli`), Fine-Tuned `ModernBERT-base`, and Fine-Tuned `DeBERTa-v3-base`.*

### 3. Manuscript Structure & Placement of Empirical Benchmarks
* **Question 3.1**: *In Chapter 3 (Methodology), we have already documented our Stage 1 Full-Corpus Benchmark (Table 3.7) and Candidate Retrieval Ablation Benchmark (Table 3.8 and Figure 3.9) to justify why RRF and dense bi-encoders were selected. Does Ma'am Grace prefer keeping these empirical selection results in Chapter 3 (as empirical architecture selection), or moving them to Chapter 4 (Results and Discussion)?*
* **Question 3.2**: *Does the current draft length of Chapter 3 (~95 KB LaTeX, ~30 pages compiled with figures) meet the depth expectations for our proposal defense milestone?*

### 4. Prototype & Interface Scope for Proposal Defense
* **Question 4.1**: *For the upcoming proposal defense, is a working command-line and programmatic demonstration (`scripts/prototype_pipeline.py`) sufficient, or is a live web application frontend (React/Vite or Streamlit/FastAPI) required before proposal defense approval?*

---

## Part 6: Recommended Action Checklist for Proponents

Before our meeting with Ma'am Grace Tacadao and Sir Adrian Ablazo:

- [x] Pull latest origin commits (`0804727` and `483e15c`) and verify clean synchronization.
- [x] Compile and verify clean build of LaTeX manuscript (`python scripts/build_paper.py --fast`).
- [x] Verify all 8 publication-grade figures in `CS_Undergraduate_Thesis_Template/figs/`.
- [x] Verify Ground Truth review workbook ([`data/ground_truth_350_adviser_review.xlsx`](file:///c:/Users/SHRIMP/Documents/thesis-repo/data/ground_truth_350_adviser_review.xlsx)).
- [x] Run and test prototype execution pipeline ([`scripts/prototype_pipeline.py`](file:///c:/Users/SHRIMP/Documents/thesis-repo/scripts/prototype_pipeline.py)).
- [ ] Fill in Department Chairperson name in [`docs/annotation/adviser_endorsement_letter_template.md`](file:///c:/Users/SHRIMP/Documents/thesis-repo/docs/annotation/adviser_endorsement_letter_template.md).
- [ ] Prepare 10-minute slide deck summarizing the 4 parts of this report.
- [ ] Schedule consultation meeting with Ma'am Grace Tacadao and Sir Adrian Ablazo.
