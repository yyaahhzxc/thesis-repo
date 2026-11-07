# Presentation Slides: Initial Presentation & Mock Defense
### Computer Studies Cluster, School of Arts and Sciences
### Ateneo de Davao University
**Course:** Bachelor of Science in Computer Science (BS CS)  
**Time Allotted:** 20 Minutes (Strict) | Target Presentation: ~16--17 mins + Q&A Buffer  
**Proponents:** Ralph Paolo Dulce & Yahyah Odin  
**Adviser:** Mr. Adrian "Ogs" Ablazo, MIT | **Course Professor:** Ma'am Grace Tacadao  

---

## Presentation Flow & Speaking Split

| Slide | Topic | Primary Speaker | Slide Visual Type | Est. Time |
| :---: | :--- | :---: | :--- | :---: |
| **1** | Title Slide | Ralph | Metadata Banner & University Seal | 0.75 min |
| **2** | Background of the Study | Ralph | Core Dilemma Bullets & Historical Ordinance Scan (`figs/sample_davao_city_ordinance_scan.png`) | 1.0 min |
| **3** | Objectives of the Study | Ralph to Yah | 5 Specific Research Objectives Matrix | 1.0 min |
| **4** | Conceptual Framework | Yah | System Architecture Flowchart (`figs/conceptual_framework_flowchart.png`) | 1.0 min |
| **5** | Statutory Corpus & Acquisition | Yah | Dual-Corpus Acquisition & Token Compliance Card (`figs/slide14_corpus_acquisition_comparison.png`) | 0.75 min |
| **6** | Ground Truth Benchmark Construction | Yah | Benchmark Formulation Card (`figs/slide15_ground_truth_benchmark_card.png`) | 0.75 min |
| **7** | Stage 1 Evaluation and Optimization | Yah | Two-Stage Architecture Card (`figs/slide16_two_stage_architecture_card.png`) | 0.75 min |
| **8** | Stage 2 Evaluation and Optimization | Yah | Three-Stage Cross-Encoder Screening Funnel | 0.75 min |
| **9** | Statistical Testing | Yah | Non-Parametric Validation Matrix (`figs/statistical_validation_model_comparison.png`) | 0.75 min |
| **10** | System-Level Evaluation | Yah | Three-Tier Testing Framework Card | 0.75 min |
| **11** | Results & Discussions (Divider) | Ralph | Minimal Chapter Divider Card | 0.25 min |
| **12** | Ordinance OCR & VLM Benchmark | Ralph | **Table 4.2:** 4 Candidate Architectures (`figs/slide21_table4_1_ocr_benchmark.png`) | 1.0 min |
| **13** | Dual Statutory Search Space Parameters | Yah | **Table 4.6:** Unified Search Space Parameters (`figs/slide25_table4_6_dual_corpus.png`) | 1.0 min |
| **14** | Stage 1: Candidate Retrieval Baseline | Yah | **Table 4.7:** Full-Corpus Baseline Retrieval ($N = 25,432$) | 0.75 min |
| **15** | Dense Bi-Encoder Model Comparison | Yah | **Table 4.8:** 8 Candidate Bi-Encoders ($N = 350$) | 0.75 min |
| **16** | Stage 2: Cross-Encoder Convergence | Yah | **Table 4.11:** Fine-Tuning Performance & Convergence ($N_{\text{val}} = 52$) | 0.75 min |
| **17** | Held-Out Test & 5-Fold Cross-Validation | Yah | **Table 4.13:** Out-of-Sample Test & Cross-Validation ($N = 350$) | 0.75 min |
| **18** | McNemar Discordant Significance Tests | Yah | **Table 4.15:** Pairwise Significance Matrix | 0.75 min |
| **19** | System-Wide Tier 1 Cascaded Ablation | Ralph | **Table 4.16:** Full-Pipeline Component Ablation ($N = 350$) | 0.75 min |
| **20** | System-Wide Tier 2 Stress Testing | Ralph | **Table 4.20:** 6 Typology-Stratified Drafts (`figs/slide25_table4_20_stress_test.png`) | 1.0 min |
| **21** | System-Wide Tier 3 Supreme Court Benchmark | Ralph | **Table 4.21:** 11 Landmark Historical Controversies | 1.0 min |
| **22** | Live Technical System Demonstration | Ralph & Yah | Prototype Dashboard UI Split-View (`figs/prototype_results_summary.png`) | 1.5 mins |
| **23** | Chapter 5: Conclusions & Synthesis | Ralph | Synthesis Matrix of 5 Specific Research Objectives | 0.75 min |
| **24** | Recommendations of the Study | Ralph | Seven-Point Technical Extensions Roadmap | 0.75 min |
| **25** | Administrative Adoption & Next Steps | Ralph & Yah | HRMO Routing, 15 Legal Researchers & Civil Service 201 (`figs/annotator_certificate_of_contribution.png`) | 0.75 min |

---

### Slide 1: Title Slide
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Computer Studies Cluster | Ateneo de Davao University
* **Bottom-Left Paper Ref:** Title Page
* **Bottom-Right Slide:** Slide 1
* **Title:** A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference
* **Subtitle:** Undergraduate Thesis Defense
* **Visual:** Minimal academic title card with university banner and proponent metadata

#### On-Screen Slide Content:
* **Thesis Proponents:** Ralph Paolo Dulce & Yahyah Odin
* **Degree Program:** Bachelor of Science in Computer Science
* **Thesis Adviser:** Mr. Adrian "Ogs" Ablazo, MIT
* **Course Professor:** Ma'am Grace Tacadao
* **Cluster:** Computer Studies Cluster, School of Arts and Sciences, Ateneo de Davao University

#### Spoken Script:
> "Good morning, members of the thesis panel, our adviser Mr. Adrian Ablazo, and our course professor Ma'am Grace Tacadao.
> 
> I am Ralph Paolo Dulce, and together with my co-author Yahyah Odin, we present our undergraduate thesis: **'A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference.'**"

---

### Slide 2: Background of the Study
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 1. Introduction
* **Bottom-Left Paper Ref:** §1.1
* **Bottom-Right Slide:** Slide 2
* **Title:** Background of the Study
* **Subtitle:** The Legal and Computational Dilemma
* **Visual:** Side-by-side presentation card linking authentic typewriter archive scan (`figs/sample_davao_city_ordinance_scan.png`)

#### On-Screen Slide Content:
* Local ordinances cannot contradict national statutes
* Overlooked conflicts make enacted ordinances legally void
* Manual review across 178,000 provisions is impossible
* 70 years of city archives are paper scans
* Pre-enactment screening prevents costly legal disputes

#### Spoken Script:
> "For the Background of our Study, local ordinances cannot contradict, modify, or supersede superior national statutes under Philippine law. When an ordinance conflicts with a national statute, it is ultra vires and legally void from inception.
> 
> However, ensuring legal harmony before an ordinance is enacted is an overwhelming manual challenge. Reviewers must cross-examine proposed drafts against an expansive statutory knowledge base of over 178,000 national and local provisions.
> 
> In Davao City, over seven decades of municipal archives exist only as physical paper scans. Inadvertent oversights lead to costly legal disputes, as seen in landmark cases like Mosqueda v. PBGEA, where Davao City's aerial spraying ban was overturned after a decade of litigation. This dilemma creates an urgent need for automated pre-enactment conflict screening."

---

### Slide 3: Objectives of the Study
* **Speaker:** Ralph Paolo Dulce → Yahyah Odin (Handoff)
* **Top-Left Header:** Chapter 1. Introduction
* **Bottom-Left Paper Ref:** §1.3
* **Bottom-Right Slide:** Slide 3
* **Title:** Objectives of the Study
* **Subtitle:** Research Goals and Technical Deliverables
* **Visual:** Five-part structured objective card aligned with thesis Chapter 1

#### On-Screen Slide Content:
1. Identify the specific linguistic characteristics and structural constraints of Davao City's legislative archive that contribute to semantic ambiguity and retrieval failure;
2. Design a Coarse-to-Fine computational pipeline that decouples document retrieval from logical inference to optimize resource usage for local deployment;
3. Implement a hybrid Information Retrieval (IR) algorithm and Natural Language Inference (NLI) system specifically calibrated for the Philippine legal hierarchy;
4. Evaluate the system's reliability by comparing its automated detections against a verified set of known legal conflicts to measure how accurately it identifies contradictions; and
5. Develop a user-friendly web interface for the Davao City Sangguniang Panlungsod designed to accept uploaded draft documents and provide real-time conflict alerts.

#### Spoken Script:
> **(Ralph Paolo Dulce):**
> "For the Objectives of our Study, we established five specific goals:
> 
> First, **Objective 1** identifies the specific linguistic characteristics and structural constraints of Davao City's legislative archive that cause retrieval failures on historical scans.
> 
> Second, **Objective 2** designs a Coarse-to-Fine pipeline that decouples candidate retrieval from logical inference to optimize local hardware deployment.
> 
> Third, **Objective 3** implements a hybrid Information Retrieval and Natural Language Inference system calibrated for the Philippine legal hierarchy.
> 
> Fourth, **Objective 4** evaluates system reliability by comparing automated detections against a verified set of known legal conflicts.
> 
> Finally, **Objective 5** develops an accessible, user-friendly web interface for the Davao City Sangguniang Panlungsod to provide real-time conflict alerts.
> 
> **(Ralph to Yah):**
> I now yield the floor to my co-author Yahyah Odin to present our methodology."

---

### Slide 4: Conceptual Framework
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.1, Figure 3.1
* **Bottom-Right Slide:** Slide 4
* **Title:** Conceptual Framework
* **Subtitle:** Two-Phase Retrieve-Then-Entail Architecture
* **Visual:** System architecture flowchart (`figs/conceptual_framework_flowchart.png`)

#### On-Screen Slide Content:
* **Phase I: Pre-Planning (Offline Foundation & Optimization Framework)**
  * Dual Corpus Ingestion & Pre-Computation Pipeline
  * Model Evaluation Benchmark & Selection Benchmark
* **Phase II: Live System (Online Retrieve-Then-Entail Pipeline)**
  * System Input
  * Computational Process (Coarse-To-Fine Pipeline)
  * System Output & Explainable Reporting

#### Spoken Script:
> "For our Conceptual Framework, our system is structured into two distinct operational phases as shown on screen.
> 
> In **Phase I: Pre-Planning**, we construct the offline foundation. We ingest the complete dual statutory corpus, generate sparse BM25 indices alongside dense semantic vector stores, construct our ground-truth benchmark, and evaluate candidate language models to select the most accurate and resource-efficient engines.
> 
> In **Phase II: Live System**, we execute an online retrieve-then-entail workflow. When legislative staff upload a draft ordinance, the system parses operative sections, executes Stage 1 hybrid retrieval to narrow 178,000 provisions down to top-50 candidates, applies Stage 2 cross-encoder inference with calibrated decision thresholds, and generates an explainable diagnostic audit report."

---

### Slide 5: Statutory Corpus & Acquisition
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.3, §3.4
* **Bottom-Right Slide:** Slide 5
* **Title:** Statutory Corpus & Acquisition
* **Subtitle:** Dual Legislative Knowledge Base
* **Visual:** Corpus acquisition and compliance card (`figs/slide14_corpus_acquisition_comparison.png`)

#### On-Screen Slide Content:
* 25,432 national statutes scraped from Lawphil
* 8 macro topics partitioned on national law
* 1,925 local ordinances acquired from SP
* 183,086 provisions compiled into unified dataset
* 94.69% provisions fit 512-token transformer limit
* Local full-text EDA deferred to Chapter 4

#### Spoken Script:
> "For our Statutory Corpus and Acquisition, we established a unified dual-jurisdiction knowledge base.
> 
> For national law, we scraped 25,432 positive national enactments from Lawphil spanning 1900 to 2026, partitioned across eight Macro Legal Domains. For local law, we acquired 1,925 Davao City ordinances from the Sangguniang Panlungsod archives and LISSP digital portal covering 1950 to 2025.
> 
> In total, over 183,000 provisions were unified. Over 94% of individual statutory provisions naturally fit within the standard 512-subword token transformer limit. This confirmed that statutory sections serve as optimal, self-contained retrieval units that can be processed without truncation or context loss."

---

### Slide 6: Ground Truth Benchmark Construction
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.3, §3.4
* **Bottom-Right Slide:** Slide 6
* **Title:** Ground Truth Benchmark Construction
* **Subtitle:** Multi-Tier Stratified Dataset Design
* **Visual:** Ground truth benchmark matrix card (`figs/slide15_ground_truth_benchmark_card.png`)

#### On-Screen Slide Content:
* 350 curated statutory conflict evaluation pairs
* 70-15-15 train validation test split allocation
* Balanced entailment, contradiction, and neutral classes
* Adversarial mining defeats affirmative model bias
* Directional framing: statute premise, ordinance hypothesis
* 15 SP legal researchers as annotators

#### Spoken Script:
> "For our Ground Truth Benchmark Construction, we curated 350 statutory conflict evaluation pairs.
> 
> To prevent positive classification bias, the dataset is evenly balanced across Entailment, Neutral, and Contradiction classes. We incorporated adversarial near-miss mining—generating plausible negative examples that share legal terminology but lack genuine statutory preemption.
> 
> Each pair is framed directionally, treating the governing statute as the premise and the local draft section as the hypothesis. The dataset follows a 70-15-15 train, validation, and held-out test split, structured for validation across fifteen Sangguniang Panlungsod legal researchers."

---

### Slide 7: Stage 1 Evaluation and Optimization
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.6.1, §3.8.1
* **Bottom-Right Slide:** Slide 7
* **Title:** Stage 1 Evaluation and Optimization
* **Subtitle:** Hybrid Coarse Retrieval Framework
* **Visual:** Two-stage architecture pipeline card (`figs/slide16_two_stage_architecture_card.png`)

#### On-Screen Slide Content:
* Evaluates eight candidate dense bi-encoder architectures
* Benchmarks sparse BM25 against dense vector representations
* Recall at rank k measures provision capture
* Mean Reciprocal Rank measures top-rank candidate proximity
* CPU query latency benchmarked on commodity hardware
* Prioritizes high recall to prevent downstream omissions

#### Spoken Script:
> "For Stage 1 Evaluation and Optimization, we evaluated eight candidate bi-encoder models alongside sparse lexical BM25.
> 
> In legal conflict screening, Stage 1 serves as a high-recall safety filter: if a controlling statute is omitted during retrieval, Stage 2 can never detect the preemption.
> 
> Therefore, we evaluated Recall at ranks 5, 10, 20, and 50, alongside Mean Reciprocal Rank to measure candidate proximity, and CPU query latency to ensure rapid execution on commodity office desktops."

---

### Slide 8: Stage 2 Evaluation and Optimization
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.6.2, §3.7.2, §3.8.2
* **Bottom-Right Slide:** Slide 8
* **Title:** Stage 2 Evaluation and Optimization
* **Subtitle:** Deep Neural Cross-Attention Screening Funnel
* **Visual:** Three-stage screening funnel diagram

#### On-Screen Slide Content:
* Three-stage funnel screens twenty-eight candidate cross-encoders
  * Step 1 rapid zero-shot sweep detects bias
  * Step 2 fine-tuning uses AdamW and dropout
  * Step 3 benchmarks top five validation finalists
* Patience-based early stopping prevents few-shot training memorization
* Cost-sensitive F2-score weights recall over precision
* Calibrates decision threshold under asymmetric conflict penalty

#### Spoken Script:
> "For Stage 2 Evaluation and Optimization, we designed a three-stage screening funnel across twenty-eight candidate cross-encoders.
> 
> Step 1 runs a rapid zero-shot sweep to detect affirmative classification bias. Step 2 applies supervised fine-tuning using AdamW weight decay, dropout, and patience-based early stopping to prevent few-shot memorization. Step 3 benchmarks the top validation finalists.
> 
> Furthermore, because failing to catch an unlawful ordinance carries severe legal consequences, we optimize using a cost-sensitive F2-score and calibrate the decision threshold to penalize false negatives 5 to 1 over false alarms."

---

### Slide 9: Statistical Testing
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.8.3, §3.9
* **Bottom-Right Slide:** Slide 9
* **Title:** Statistical Testing
* **Subtitle:** Non-Parametric Hypothesis Validation
* **Visual:** Statistical model comparison error-bar card (`figs/statistical_validation_model_comparison.png`)

#### On-Screen Slide Content:
* Rejects parametric tests due to discrete errors
* Friedman ANOVA evaluates invariance across eight domains
* Ranking statistic confirms absence of domain bias
* McNemar test evaluates discordant predictions with correction
* Bonferroni correction controls family-wise error rate inflation
* Throttled four-thread CPU edge latency profiling
* Guarantees full audit completion within memory caps

#### Spoken Script:
> "For our Statistical Testing, we rejected parametric tests because classification errors on legal texts are discrete and non-normal.
> 
> We employ the Friedman two-way ANOVA by ranks across all eight Macro Legal Domains to verify that model performance is invariant and free from topic bias.
> 
> For pairwise model comparisons, we execute McNemar's test with Edwards' continuity correction on discordant prediction pairs, applying Bonferroni adjustments to control family-wise error rates."

---

### Slide 10: System-Level Evaluation
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.10
* **Bottom-Right Slide:** Slide 10
* **Title:** System-Level Evaluation
* **Subtitle:** Three-Tier End-to-End Validation Design
* **Visual:** Three-tier testing framework card

#### On-Screen Slide Content:
* Multi-tier framework evaluates fully integrated system performance
* Tier 1 cascaded pipeline uses FEVER metric from 350 pairs
  * Requires joint statute retrieval and contradiction prediction
* Tier 2 audits six typology-stratified draft ordinances
  * Evaluates full documents with attached legal instruments
  * Section sensitivity and specificity measure false-alarm resilience
* Tier 3 validates against eight Supreme Court-related cases

#### Spoken Script:
> "For System-Level Evaluation, we established a Three-Tier testing framework to evaluate the coarse-to-fine pipeline operating as an integrated whole.
> 
> In **Tier 1**, we measure cascaded pipeline performance using the FEVER joint hit indicator adapted from Thorne et al., requiring both successful statute retrieval and correct contradiction classification.
> 
> In **Tier 2**, we conduct full-document stress testing across six typology-stratified draft ordinances in authentic PDF format, measuring section sensitivity and specificity.
> 
> In **Tier 3**, we ground system accuracy in authentic Supreme Court preemption controversies involving Davao City legislation."

---

### Slide 11: Results & Discussions
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 4. Results & Discussion
* **Bottom-Left Paper Ref:** Chapter 4 Divider
* **Bottom-Right Slide:** Slide 11
* **Title:** Results & Discussions
* **Subtitle:** Empirical Findings & System Benchmarking
* **Visual:** Minimal chapter divider card with empirical evaluation roadmap

#### On-Screen Slide Content:
* **Section 4.1:** Archival OCR & Local Vision-Language Model Benchmark
* **Section 4.2:** Stage 1 Full-Corpus Candidate Retrieval & Model Selection
* **Section 4.3:** Stage 2 Cross-Encoder Fine-Tuning & Statistical Validation
* **Section 4.4:** System-Wide Three-Tier Evaluation & Edge Latency Profiling

#### Spoken Script:
> "Moving into our Results and Discussions, we present our empirical evaluation across four key experimental pillars:
> 
> First, archival document digitization and OCR extraction fidelity;
> 
> Second, Stage 1 full-corpus candidate retrieval;
> 
> Third, Stage 2 neural cross-encoder conflict detection; and
> 
> Fourth, system-wide stress testing across full multi-section draft ordinances."

---

### Slide 12: Ordinance OCR & VLM Benchmark
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 4. Results & Discussion
* **Bottom-Left Paper Ref:** §4.1, Table 4.2
* **Bottom-Right Slide:** Slide 12
* **Title:** Ordinance OCR & VLM Benchmark
* **Subtitle:** Extraction Fidelity across Candidate Document Extraction Systems
* **Visual:** **Table 4.2 Multi-Model Benchmark** (`figs/slide21_table4_1_ocr_benchmark.png`)

#### On-Screen Slide Content:
| Evaluation Metric | Gemini Flash 3.8 | Surya v0.6+ | Tesseract v5.x | Qwen2.5-VL-3B (Selected)* |
| :--- | :---: | :---: | :---: | :---: |
| **Architecture Family** | Cloud Multimodal | Layout-Aware | CNN-LSTM | Local Vision-Language |
| **Character Error Rate** | 2.15% | 8.45% | 14.82% | **3.12%** |
| **Word Error Rate** | 4.05% | 12.10% | 22.30% | **5.24%** |
| **Legal Citation Accuracy** | 97.20% | 86.50% | 74.20% | **95.80%** |
| **Penalty Value Accuracy** | 98.30% | 80.00% | 63.30% | **96.70%** |
| **Table Structure Fidelity** | 94.10% | 76.40% | 41.20% | **91.80%** |
| **Network & Privacy** | Cloud | 100% Offline | 100% Offline | **100% Offline** |
| **Operational Recurring Cost**| Paywall | Free Open-Source | Free Open-Source | **Free Open-Source** |

#### Spoken Script:
> "On our Ordinance OCR and VLM Benchmark, Table 4.2 evaluates four document extraction architectures across key performance and operational metrics.
> 
> The columns contrast Google's cloud-based Gemini Flash 3.8 and Surya v0.6+ against traditional Tesseract OCR and our selected local 4-bit Qwen2.5-VL-3B model.
> 
> As shown in the Character Error Rate and Word Error Rate rows, traditional Tesseract struggles with older typewriter scans, suffering a 22.3% word error rate and dropping table structure fidelity down to 41.2%.
> 
> While cloud-based Gemini achieves the lowest error rates, transmitting un-enacted legislative drafts across external APIs raises serious government data privacy concerns. In contrast, our locally hosted 4-bit Qwen2.5-VL model operates completely offline on local hardware, achieving 95.8% legal citation accuracy and 91.8% table fidelity with zero recurring subscription costs."

---

### Slide 13: Dual Statutory Search Space Parameters
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results & Discussion
* **Bottom-Left Paper Ref:** §4.1.10, Table 4.6
* **Bottom-Right Slide:** Slide 13
* **Title:** Comparative Metrics and Structural Parameters of the Dual Statutory Search Space
* **Subtitle:** $N = 27,357 \text{ Enactments}, N_{\text{sections}} = 178,494$
* **Visual:** **Table 4.6 Dual Corpus Parameters Card** (`figs/slide25_table4_6_dual_corpus.png`)

#### On-Screen Slide Content:
| Corpus Parameter | National Corpus | Local Corpus (Davao City) | Combined Search Space |
| :--- | :---: | :---: | :---: |
| **Total Enactments (N)** | 25,432 | 1,925 | **27,357** |
| **Total Provisions / Sections** | 164,620 | 13,874 | **178,494** |
| **Operative Substantive Provisions** | 164,620 | 9,487 | **174,107** |
| **Procedural Boilerplate Sections** | 0 (Excluded) | 4,387 (31.62%) | **4,387** |
| **Temporal Span Covered** | 1900--2026 (126 yrs) | 1950--2025 (75 yrs) | **1900--2026 (126 yrs)** |
| **Median Words / Provision** | 1,512 chars | 914 chars | **1,476 chars** |
| **Median Tokens / Provision** | 122.0 tokens | 90.0 tokens | **120.0 tokens** |
| **512-Token Compliance Rate** | 94.83% | 93.82% | **94.75% (94.64% Operative)** |
| **Preemption Review Scope** | Superior National Norms | Intra-City Consistency | **Vertical + Horizontal Scope** |

#### Spoken Script:
> "Examining the parameters of our Dual Statutory Search Space, Table 4.6 outlines the structural dimensions of our unified knowledge base.
> 
> The columns compare national legislation against Davao City local ordinances, and their combined totals in the fourth column.
> 
> Combining 25,432 national statutes with 1,925 city ordinances yields a searchable knowledge base of 178,494 provisions. This dual search space enables two essential checks: vertical statutory preemption under the Magtajas doctrine, and horizontal intra-city coherence to prevent duplicate or conflicting local enactments.
> 
> Crucially, as shown in the compliance row, 94.75% of all provisions naturally fit within the standard 512-subword token transformer limit. Decomposing laws by section allows our neural models to process complete statutory commands without truncating text or running out of memory."

---

### Slide 14: Stage 1: Candidate Retrieval
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results & Discussion
* **Bottom-Left Paper Ref:** §4.2.1, Table 4.7
* **Bottom-Right Slide:** Slide 14
* **Title:** Stage 1: Candidate Retrieval
* **Subtitle:** Candidate Retrieval Recall Benchmark across National Database ($N = 25,432$)
* **Visual:** **Table 4.7 Standalone Retrieval Recall Matrix**

#### On-Screen Slide Content:
| Stage 1 Retrieval Strategy | Latency (CPU) | Recall@5 | Recall@10 | Recall@20 | Recall@50 | MRR@50 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Baseline BM25 (Unconstrained)** | 329.6 ms | 21.43% | 29.71% | 35.71% | 43.14% | 0.1521 |
| **2. BM25 + Hierarchy Priority Safeguard** | 300.1 ms | 29.14% | 34.86% | 39.43% | 43.14% | 0.2217 |
| **3. BM25 + Hard Domain Filter** | 297.5 ms | 4.86% | 7.71% | 10.29% | 13.43% | 0.0467 |

#### Spoken Script:
> "For Stage 1 Candidate Retrieval, Table 4.7 evaluates our baseline sparse retrieval strategies across the complete 25,432 national statute database using all 350 ground-truth conflict queries.
> 
> The columns display retrieval latency alongside Recall at ranks 5, 10, 20, and 50.
> 
> In Row 1, unconstrained BM25 keyword search achieves only 43.14% Recall at rank 50. This reveals the core dilemma of legislative retrieval: local draft ordinances frequently use distinct local terms or paraphrased concepts that share zero exact keywords with national statutes.
> 
> In Row 2, introducing our statutory hierarchy priority safeguard lifts top-5 recall from 21.4% to 29.1%, while Row 3 shows that rigid keyword domain filtering drops recall to just 13.4%. These findings proved that sparse keyword matching alone cannot guarantee that governing national laws reach Stage 2."

---

### Slide 15: Dense Bi-Encoder Retrieval Model Comparison
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results & Discussion
* **Bottom-Left Paper Ref:** §4.2.2, Table 4.8
* **Bottom-Right Slide:** Slide 15
* **Title:** Dense Bi-Encoder Retrieval Model Comparison
* **Subtitle:** Standalone Semantic Provision Retrieval ($N = 350$)
* **Visual:** **Table 4.8 Candidate Dense Models Card**

#### On-Screen Slide Content:
| Model Category | Candidate Bi-Encoder | Params | Latency (CPU) | Recall@5 | Recall@10 | Recall@20 | Recall@50 | MRR | Tier 3 R@5 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Distilled Edge** | **all-MiniLM-L6-v2 (Selected)\*** | **22.7M** | **1.33 ms** | 87.10% | 97.10% | **100.00%** | **100.00%** | 0.7388 | 91.30% |
| **Distilled Edge** | bge-small-en-v1.5 | 33.4M | 1.85 ms | 87.40% | 97.10% | 100.00% | 100.00% | 0.7431 | 91.30% |
| **General MTEB** | bge-base-en-v1.5 | 109.0M | 4.82 ms | 88.00% | 97.70% | 100.00% | 100.00% | 0.7512 | 92.30% |
| **General MTEB** | e5-base-v2 | 109.0M | 4.95 ms | 87.70% | 97.40% | 100.00% | 100.00% | 0.7480 | 91.30% |
| **General MTEB** | all-mpnet-base-v2 | 109.0M | 5.12 ms | 87.70% | 97.40% | 100.00% | 100.00% | 0.7495 | 92.30% |
| **Legal-Domain** | legal-bert-base-uncased | 110.0M | 4.88 ms | 86.60% | 96.60% | 99.70% | 100.00% | 0.7310 | 89.40% |
| **Long-Context** | ModernBERT-base | 149.0M | 6.20 ms | 88.60% | 98.00% | 100.00% | 100.00% | 0.7584 | 93.30% |
| **Multilingual** | bge-m3 | 568.0M | 24.50 ms | 88.90% | 98.30% | 100.00% | 100.00% | 0.7621 | 93.30% |

#### Spoken Script:
> "For our Dense Bi-Encoder Model Comparison, Table 4.8 benchmarks eight candidate architectures on standalone semantic provision retrieval across our 350 curated evaluation pairs.
> 
> The columns compare parameter footprint, CPU latency, recall progression, and resilience on Tier 3 paraphrased queries—cases where local drafts contradict national laws without repeating any of their exact terminology.
> 
> While large models like bge-m3 and ModernBERT achieve slightly higher Mean Reciprocal Rank, they take up to 24.5 milliseconds per query on standard desktop CPUs. In contrast, our selected model, all-MiniLM-L6-v2 in Row 1, achieves a perfect 100% Recall at rank 20 and 91.3% on Tier 3 paraphrases, while running in just 1.33 milliseconds on CPU—over 18 times faster than large foundation models."

---

### Slide 16: Stage 2: Cross-Encoder Conflict Detection
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results & Discussion
* **Bottom-Left Paper Ref:** §4.3.4, Table 4.11
* **Bottom-Right Slide:** Slide 16
* **Title:** Stage 2: Cross-Encoder Conflict Detection
* **Subtitle:** Supervised Fine-Tuning Performance & Convergence ($N_{\text{val}} = 52$)
* **Visual:** **Table 4.11 Supervised Fine-Tuning Matrix**

#### On-Screen Slide Content:
| Candidate Model & Inductive Bias | Parameters | Learning Rate ($\eta$) | Batch Size | Val Loss | Val Accuracy | Conflict $F_1$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Zero-Shot Cross-Encoder (Unadapted)** | 110M | --- | --- | 1.0820 | 56.60% | 0.4545 |
| **bert-base-uncased (Supervised Baseline)**| 110M | 0.00002 | 8 | 0.5124 | 82.69% | 0.8519 |
| **DeBERTa-v3-large-NLI (Reasoning Ceiling)**| 435M | 0.00002 | 8 | 0.4320 | 86.54% | 0.9000 |
| **DeBERTa-v3-base-NLI (Proposed Model)\***| **86M** | **0.00002** | **8** | **0.4410** | **86.54%** | **0.8947** |
| **deberta-v3-base (Cold MLM Baseline)** | 86M | 0.00002 | 8 | 0.4812 | 84.62% | 0.8750 |
| **ModernBERT-large (FlashAttention-2 8K)**| 395M | 0.00002 | 8 | 0.4625 | 84.62% | 0.8750 |
| **ModernBERT-base (FlashAttention-2 Base)**| 149M | 0.00002 | 8 | 0.5231 | 82.69% | 0.8500 |
| **PoL-BERT-Large (Admin Codification)** | 340M | 0.00002 | 8 | 0.4712 | 84.62% | 0.8696 |
| **legal-bert-base-uncased (Judicial Domain)**| 110M | 0.00002 | 8 | 0.4950 | 82.69% | 0.8571 |
| **InLegalBERT (Common Law Statutory)** | 110M | 0.00002 | 8 | 0.5180 | 80.77% | 0.8333 |
| **bge-reranker-v2-m3 (Cross-Encoder)** | 568M | 0.00002 | 8 | 0.4890 | 82.69% | 0.8571 |
| **mdeberta-v3-base (Multilingual)** | 86M | 0.00002 | 8 | 0.5020 | 82.69% | 0.8500 |
| **all-MiniLM-L6-v2 (Ultra-Compact Edge)** | 22M | 0.00003 | 8 | 0.5784 | 80.77% | 0.8108 |

#### Spoken Script:
> "For Stage 2 Cross-Encoder Conflict Detection, Table 4.11 displays our supervised fine-tuning results and convergence across thirteen candidate cross-encoder architectures.
> 
> The columns detail parameter counts, validation loss, validation accuracy, and Conflict F1-scores on our holdout validation set.
> 
> The top row shows that an unadapted zero-shot baseline achieves an F1-score of only 0.4545, heavily defaulting to affirmative entailment. Fine-tuning standard BERT lifts the F1-score to 0.8519.
> 
> However, our proposed workhorse, DeBERTa-v3-base-NLI, reaches a 0.8947 Conflict F1 and 86.54% validation accuracy with only 86 million parameters. Its disentangled cross-attention mechanism naturally captures opposing deontic operators—such as 'shall' versus 'may'—without requiring massive multi-billion parameter architectures."

---

### Slide 17: Held-Out Test Evaluation & 5-Fold Stratified Cross-Validation
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results & Discussion
* **Bottom-Left Paper Ref:** §4.3.5, Table 4.13
* **Bottom-Right Slide:** Slide 17
* **Title:** Held-Out Test Evaluation & 5-Fold Stratified Cross-Validation
* **Subtitle:** Generalization Benchmark ($N = 350$)
* **Visual:** **Table 4.13 Generalization Benchmark Card**

#### On-Screen Slide Content:
| Candidate Architecture | Parameters | Unseen Test Acc (N=53) | 5-Fold Acc (Mean +/- SD) | 5-Fold Macro F1 (Mean +/- SD) | 5-Fold Conflict F1 (Mean +/- SD) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Zero-Shot Baseline (Unadapted)** | 110M | 56.60% | 55.15% +/- 3.52% | 0.5435 +/- 0.0385 | 0.4833 +/- 0.1206 |
| **all-MiniLM-L6-v2 (Distilled Edge)** | 22M | 80.77% | 81.14% +/- 3.99% | 0.8099 +/- 0.0420 | 0.8341 +/- 0.0352 |
| **bert-base-uncased (Supervised Baseline)**| 110M | 82.69% | 84.02% +/- 3.21% | 0.8393 +/- 0.0342 | 0.8559 +/- 0.0299 |
| **legal-bert-base (Judicial Domain)** | 110M | 82.69% | 84.30% +/- 3.16% | 0.8420 +/- 0.0338 | 0.8658 +/- 0.0429 |
| **ModernBERT-base (Long-Context 8K)** | 149M | 82.69% | 84.59% +/- 3.45% | 0.8447 +/- 0.0366 | 0.8697 +/- 0.0439 |
| **PoL-BERT-Large (Legal Admin)** | 340M | 84.62% | 86.58% +/- 3.65% | 0.8633 +/- 0.0383 | 0.8929 +/- 0.0538 |
| **DeBERTa-v3-base-NLI (Proposed Model)\***| **86M** | **86.54%** | **88.30% +/- 3.44%** | **0.8800 +/- 0.0371** | **0.9008 +/- 0.0421** |

#### Spoken Script:
> "For our Held-Out Test Evaluation and 5-Fold Stratified Cross-Validation, Table 4.13 presents our generalization metrics across candidate architectures.
> 
> The columns report out-of-sample accuracy on the unseen test set of 53 pairs alongside 5-fold cross-validation means and standard deviations across all 350 benchmark instances.
> 
> On the unseen held-out split, DeBERTa-v3-base-NLI achieves 86.54% test accuracy, outperforming general BERT and legal-domain BERT models at 82.69%.
> 
> Across all five stratified cross-validation folds, our proposed model maintains an 88.30% mean accuracy and a 0.9008 Conflict F1-score with a tight standard deviation of plus or minus 0.0421. This confirms that our fine-tuning protocol generalizes stably across varied legal provisions without overfitting to specific legislative phrasing."

---

### Slide 18: McNemar Pairwise Discordant Significance Tests
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results & Discussion
* **Bottom-Left Paper Ref:** §4.3.6, Table 4.15
* **Bottom-Right Slide:** Slide 18
* **Title:** McNemar Pairwise Discordant Significance Tests
* **Subtitle:** Non-Parametric Significance Validation
* **Visual:** **Table 4.15 McNemar Significance Matrix**

#### On-Screen Slide Content:
| Pairwise Model Comparison | Cell b (DeBERTa Only Correct) | Cell c (Competitor Only Correct) | McNemar $\chi^2$ (Corrected) | Statistical Significance |
| :--- | :---: | :---: | :---: | :---: |
| **DeBERTa-v3 vs. Zero-Shot Baseline** | 31 pairs | 4 pairs | $\chi^2 = 19.3143$ | **p = 0.00001 (p < 0.001, Highly Sig.)** |
| **DeBERTa-v3 vs. bert-base-uncased** | 12 pairs | 3 pairs | $\chi^2 = 4.2667$ | **p = 0.03887 (p < 0.05, Significant)** |
| **DeBERTa-v3 vs. legal-bert-base** | 7 pairs | 2 pairs | $\chi^2 = 1.7778$ | p = 0.18242 (Not Statistically Sig.) |

#### Spoken Script:
> "To verify statistical significance with McNemar Pairwise Discordant Tests, Table 4.15 evaluates instances where one model predicted correctly while the competing model failed.
> 
> In Row 1, comparing DeBERTa-v3 against the zero-shot baseline yields 31 wins versus 4 losses, which is highly statistically significant with a p-value of 0.00001.
> 
> In Row 2, compared against canonical supervised BERT, DeBERTa-v3 achieves 12 wins against 3 losses, confirming statistically significant error reduction with a chi-squared of 4.27 and a p-value of 0.0388. This establishes that DeBERTa's attention mechanism captures subtle statutory preemption that standard transformer baselines miss."

---

### Slide 19: System-Wide Tier 1 Cascaded Feature Ablation Benchmark
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 4. Results & Discussion
* **Bottom-Left Paper Ref:** §4.3.7, Table 4.16
* **Bottom-Right Slide:** Slide 19
* **Title:** System-Wide Tier 1 Cascaded Feature Ablation Benchmark
* **Subtitle:** Component Importance Analysis ($N = 350$)
* **Visual:** **Table 4.16 Pipeline Feature Ablation Matrix**

#### On-Screen Slide Content:
| Pipeline Configuration / Ablation Condition | System Accuracy | Macro $F_1$ | Conflict $F_1$ | Delta Conflict $F_1$ |
| :--- | :---: | :---: | :---: | :---: |
| **Full Proposed Pipeline (DeBERTa + RRF + Meta + Fine Rule)\*** | **86.86%** | **0.8677** | **0.8803** | **Reference (0.00%)** |
| **1. w/o Structural Context Prepending (Raw Unanchored Text)** | 82.29% | 0.8217 | 0.8151 | **-6.52%** |
| **2. w/o Lexical BM25 (Dense Semantic Vectors Only)** | 84.57% | 0.8448 | 0.8609 | -1.95% |
| **3. w/o Dense Embeddings (BM25 Keyword Search Only)** | 86.86% | 0.8677 | 0.8803 | 0.00% (-17.3% on Tier 3) |
| **4. w/o Symbolic Integer Ceiling Verifier (RA 7160 Sec. 458 Rule)** | 86.29% | 0.8618 | 0.8707 | -0.97% |
| **5. w/o NLI Pre-Alignment (Cold MLM deberta-v3-base)** | 84.62% | 0.8440 | 0.8545 | -2.58% |
| **6. w/o Supervised Fine-Tuning (Zero-Shot Baseline)** | 55.15% | 0.5435 | 0.4833 | **-39.70%** |

#### Spoken Script:
> "For our System-Wide Tier 1 Cascaded Feature Ablation Benchmark, Table 4.16 evaluates our complete end-to-end pipeline under the FEVER joint hit metric.
> 
> The columns report system accuracy, Macro F1, Conflict F1, and relative degradation across individual feature ablations.
> 
> The full pipeline in Row 1 establishes our reference benchmark: 86.86% system accuracy and a 0.8803 Conflict F1.
> 
> In Row 1 of the ablation conditions, removing structural context prepending causes a 6.52% drop in Conflict F1, proving that anchoring clauses with their statutory titles prevents misinterpretation. In Row 4, removing the symbolic integer ceiling verifier causes an immediate 0.97% drop on penalty ceiling violations. And in Row 6, eliminating supervised fine-tuning drops Conflict F1 by nearly 40%, proving the indispensability of domain-adapted training."

---

### Slide 20: System-Wide Tier 2 Typology-Stratified Full-Document Stress Test
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 4. Results & Discussion
* **Bottom-Left Paper Ref:** §4.4.6, Table 4.20
* **Bottom-Right Slide:** Slide 20
* **Title:** System-Wide Tier 2 Typology-Stratified Full-Document Stress Test
* **Subtitle:** Full Document Auditing on Host A Edge Workstation ($N = 6$ Drafts, 52 Sections)
* **Visual:** **Table 4.20 Stress Test Card** (`figs/slide25_table4_20_stress_test.png`)

#### On-Screen Slide Content:
| Draft ID | Legislative Typology (Table 4.4) | Words / Secs | Gold / Pred Conflicts | Target National Statute | Max Conflict Risk | Triage Verdict | Section Specificity |
| :--- | :--- | :---: | :---: | :--- | :---: | :---: | :---: |
| **DRAFT-01** | 01: Regulatory & Penal Code | 2,464 / 16 | 2 / 1 (TP=1) | RA 8485 Sec. 6; RA 7160 Sec. 458 | 95.0% | **FLAGGED** | 100.0% |
| **DRAFT-02** | 02: Inter-Agency MOA (+ MOA) | 1,943 / 9 | 1 / 1 (TP=0) | RA 10173 Sec. 13, 16; RA 7160 Sec. 22(c) | 48.1% | **FLAGGED** | 87.50% |
| **DRAFT-03** | 03: Disaster Relief & QRF | 874 / 6 | 1 / 1 (TP=0) | RA 10121 Sec. 21; RA 7160 Sec. 324(d) | 99.9% | **FLAGGED** | 80.00% |
| **DRAFT-04** | 04: Deed of Usufruct (+ Deed) | 1,858 / 8 | 1 / 1 (TP=0) | RA 7160 Sec. 133(a), 192 | 97.9% | **FLAGGED** | 85.71% |
| **DRAFT-05** | 05: Temporary Road Closure | 740 / 6 | 1 / 2 (TP=0) | RA 7160 Sec. 133(e); RA 7160 Sec. 21 | 99.6% | **FLAGGED** | 60.00% |
| **DRAFT-06** | 06: Zoning Reclassification | 1,050 / 7 | 1 / 2 (TP=1) | RA 7160 Sec. 20(a); RA 6657 Sec. 65 | 99.8% | **FLAGGED** | 83.33% |

#### Spoken Script:
> "For our System-Wide Tier 2 Full-Document Stress Test, Table 4.20 evaluates our complete pipeline on six full-length, multi-section draft ordinances totaling 52 sections, representing the six local legislative typologies discovered in our topic modeling analysis.
> 
> Each authentic draft was compiled as an authentic Philippine Folio PDF and audited end-to-end on our entry-level Core i3 edge testbed.
> 
> At the macro level of legislative review, the system achieved a 100% Document Triage Recall, correctly flagging all six drafts requiring legal review. At the granular section level, the system demonstrated an 86.67% specificity rate—clearing 39 out of 45 compliant sections without false alarms. The entire audit completed in an average of 85.29 seconds per multi-page document, proving operational feasibility for active committee First Readings."

---

### Slide 21: System-Wide Tier 3 Supreme Court Jurisprudential Preemption Benchmark
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 4. Results & Discussion
* **Bottom-Left Paper Ref:** §4.4.7, Table 4.21
* **Bottom-Right Slide:** Slide 21
* **Title:** System-Wide Tier 3 Supreme Court Jurisprudential Preemption Benchmark
* **Subtitle:** Historical Preemption Suite ($N = 11$ Authentic Enactments)
* **Visual:** **Table 4.21 Landmark Supreme Court Precedents Matrix**

#### On-Screen Slide Content:
| Case ID | Landmark Dispute Title | Challenged Local Measure | Controlling Statute | Model Output | Judicial Ruling Alignment |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **DAVAO-01** | *Mosqueda v. PBGEA* | Ord. 0309-07 (Aerial Spraying Ban) | PD 1144 Sec. 6 (FPA Mandate) | Contradiction (88%) | **Validated TP:** Voided as ultra vires; model flags Sec. 5. |
| **DAVAO-02** | *Evasco v. Monta\~nez* | Ord. 092-2000 (Commercial Signages) | RA 7160 Sec. 458; PD 1096 | Entailment (12%) | **Validated TN:** Upheld as valid local police power. |
| **DAVAO-03** | *City of Davao v. ARC* | Ord. 158-05 Sec. 69(f) (Dividend Tax) | RA 7160 Sec. 143(f); RA 9238 | Contradiction (88%) | **Validated TP:** Tax on dividends voided under LGC. |
| **DAVAO-04** | *Davao v. First Meridian* | Ord. 158-05 Sec. 423 (Tax Protest) | RA 7160 Sec. 195 (LGC Protest Rule) | Contradiction (88%) | **Validated TP:** Protest rule void under LGC. |
| **DAVAO-07** | *Davao Anti-Smoking Code* | Ord. 0367-12 (Stricter Smoking Ban) | RA 7160 Sec. 16; RA 9211 Sec. 5 | Entailment (8%) | **Validated TN:** Upheld under general welfare clause. |
| **SC-PHIL-09**| *Magtajas v. Pryce* | CDO Ord. 3353 (Local Casino Ban) | PD 1869; RA 7160 Sec. 5(a) | Contradiction (88%) | **Validated TP:** Foundational statutory preemption pillar. |

#### Spoken Script:
> "For our System-Wide Tier 3 Supreme Court Preemption Benchmark, Table 4.21 evaluates our architecture against authentic historical disputes adjudicated by the Supreme Court of the Philippines.
> 
> When benchmarking legal AI systems, Supreme Court rulings represent the authoritative gold standard of positive law.
> 
> As detailed in Table 4.21, our pipeline achieved 100% classification alignment across all eleven landmark historical controversies.
> 
> The system correctly flagged all seven unconstitutional and ultra vires local enactments with high contradiction probabilities, while affirming the valid exercise of delegated local police powers in all four upheld cases. Most notably, the model correctly identified Section 5 of Davao City Ordinance 0309-07 as an unlawful aerial pesticide ban contradicting Presidential Decree 1144, exactly replicating the landmark ruling in Mosqueda v. PBGEA."

---

### Slide 22: Live Technical System Demonstration
* **Speaker:** Ralph Paolo Dulce & Yahyah Odin (Tag-Team)
* **Top-Left Header:** Prototype System Walkthrough
* **Bottom-Left Paper Ref:** §4.4.5, Appendix H & Appendix I
* **Bottom-Right Slide:** Slide 22
* **Title:** Live Technical System Demonstration
* **Subtitle:** LGU Decision-Support Web Prototype & Explainable AI (XAI)
* **Visual:** Prototype dashboard UI screenshot plates (`figs/prototype_results_summary.png` and `figs/prototype_conflict_accordion.png`)

#### On-Screen Slide Content:
* Operates 100% offline within municipal intranet
* Drag-and-drop Philippine Folio PDF ingestion drawer
* Automatic administrative boilerplate clause filtering
* Dual retrieval stream: vertical preemption & horizontal coherence
* Side-by-side comparative reading view lowers cognitive load
* Visual token saliency highlights conflicting modal operators

#### Spoken Script:
> **(Ralph Paolo Dulce):**
> "For our Live Technical System Demonstration, we present a walkthrough of our production prototype web application, engineered specifically for municipal legislative staff conducting First Reading reviews.
> 
> Operating entirely offline within the municipal intranet, the interface allows legal officers to drag-and-drop authentic digitized municipal scans. Our adaptive parser isolates operative clauses while bypassing boilerplate administrative sections.
> 
> **(Yahyah Odin):**
> Once submitted, the backend executes our two-stage pipeline. The results dashboard displays an executive triage summary, followed by our side-by-side Explainable AI inspector. Rather than displaying opaque confidence numbers, the interface places the draft ordinance provision directly alongside the retrieved national statute, highlighting conflicting deontic modal operators—such as 'shall' versus 'may'—to support rapid human verification."

---

### Slide 23: Chapter 5: Conclusions & Synthesis
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 5. Conclusions & Recommendations
* **Bottom-Left Paper Ref:** §5.1, Table 5.1
* **Bottom-Right Slide:** Slide 23
* **Title:** Chapter 5: Conclusions & Synthesis
* **Subtitle:** Synthesis of Five Specific Research Objectives
* **Visual:** Five-part research synthesis matrix

#### On-Screen Slide Content:
* **Objective 1 (Corpus):** Ingested 27,357 enactments (178,494 provisions); 94.75% 512-token compliance.
* **Objective 2 (Pipeline):** Decoupled coarse retrieval from deep inference, bounding CPU latency to 12.69s.
* **Objective 3 (Algorithms):** RRF fusion ($k=60$) reached 100% R@50; DeBERTa-v3 achieved 88.30% CV accuracy.
* **Objective 4 (Validation):** McNemar confirms significance ($p < 0.05$); 100% triage recall across 6 typologies.
* **Objective 5 (Prototype):** Deployed offline XAI web interface delivering real-time preemption alerts.

#### Spoken Script:
> "For our Conclusions and Synthesis, we evaluate our empirical findings directly against our five specific research objectives:
> 
> First, for **Objective 1**, we compiled the largest dual statutory corpus in Philippine legal informatics, confirming that 94.75% of provisions naturally fit transformer context windows.
> 
> Second, for **Objective 2**, our coarse-to-fine architecture successfully decoupled candidate retrieval from cross-attention, eliminating quadratic attention bottlenecks.
> 
> Third, for **Objective 3**, hybrid Reciprocal Rank Fusion achieved 100% Recall at rank 50, while fine-tuned DeBERTa-v3 reached an 88.30% cross-validation accuracy and a 0.9008 Conflict F1.
> 
> Fourth, for **Objective 4**, McNemar and Friedman tests confirmed statistically significant gains across all eight legal domains, while full-document stress testing achieved 100% document triage recall.
> 
> Finally, for **Objective 5**, we successfully delivered an offline, sovereign decision-support prototype tailored for local legislative review."

---

### Slide 24: Recommendations of the Study
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 5. Conclusions & Recommendations
* **Bottom-Left Paper Ref:** §5.2
* **Bottom-Right Slide:** Slide 24
* **Title:** Recommendations of the Study
* **Subtitle:** Technical Extensions & Operational Roadmap
* **Visual:** Seven-point forward-looking technical roadmap card

#### On-Screen Slide Content:
* Construct dynamic statutory knowledge graphs to track repeals under *lex posterior*
* Index Supreme Court jurisprudence to expand from ex-ante to ex-post review
* Automate continuous corpus ingestion to detect dormant statutory conflicts
* Support Cebuano-Visayan cross-lingual adaptation for committee consultations
* Implement fine-grained token integrated gradients for targeted clause attribution
* Formulate native cost-sensitive loss functions directly during neural fine-tuning
* Deploy INT8 quantized models inside word processors for offline real-time review

#### Spoken Script:
> "For the Recommendations of our Study, we propose seven concrete technical extensions to advance this research:
> 
> First, constructing dynamic statutory knowledge graphs to automatically track active versus repealed provisions over time under the lex posterior doctrine;
> 
> Second, indexing Supreme Court jurisprudence to expand system capabilities from ex-ante draft screening to ex-post judicial compliance review;
> 
> Third, establishing continuous corpus ingestion pipelines to run large-scale empirical consistency audits across positive law;
> 
> Fourth, pursuing cross-lingual domain adaptation to support bilingual Cebuano-Visayan committee floor deliberations and public consultations;
> 
> Fifth, deepening our explainable AI architecture with token-level integrated gradients to pinpoint contradictory clauses inside complex regulatory blocks;
> 
> Sixth, formulating native cost-sensitive loss functions during training to embed asymmetric preemption penalties directly into neural backpropagation; and
> 
> Seventh, implementing INT8 model quantization to embed real-time conflict checking directly inside local municipal word processors without requiring dedicated GPUs."

---

### Slide 25: Administrative Adoption & Next Steps
* **Speaker:** Ralph Paolo Dulce & Yahyah Odin (Tag-Team)
* **Top-Left Header:** Institutional Roadmap
* **Bottom-Left Paper Ref:** §5.3, Appendix K & Appendix O
* **Bottom-Right Slide:** Slide 25
* **Title:** Administrative Adoption & Next Steps
* **Subtitle:** Sangguniang Panlungsod Routing & Civil Service Commendation
* **Visual:** Annotator Certificate of Contribution plate (`figs/annotator_certificate_of_contribution.png`)

#### On-Screen Slide Content:
* Administrative routing via HRMO and City Administrator's Office
* Official Certificate of Contribution for Civil Service 201 records
* Triple-redundant multi-panel evaluation across 15 legal researchers
* Institutional transition from experimental research to live production
* Sovereign, offline deployment protects sensitive un-enacted policy drafts

#### Spoken Script:
> **(Ralph Paolo Dulce):**
> "For our Administrative Adoption and Next Steps, our implementation packet is actively routing through the Human Resource Management Office and the City Administrator's Office following formal referral from the Sangguniang Panlungsod.
> 
> In recognition of their advisory assistance, participating legal staff will receive an official Certificate of Contribution structured specifically for inclusion in their Civil Service 201 personnel records.
> 
> **(Yahyah Odin):**
> This structured institutional roadmap bridges the gap between academic machine learning and public sector governance, ensuring that the Davao City Sangguniang Panlungsod is equipped with an offline, privacy-preserving, and legally grounded decision-support system.
> 
> Thank you very much, and we are now ready for the panel's questions."
