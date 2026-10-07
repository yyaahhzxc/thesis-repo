# Presentation Slides: Initial Presentation & Mock Defense
### Computer Studies Cluster, School of Arts and Sciences
### Ateneo de Davao University
**Course:** Bachelor of Science in Computer Science (BS CS)  
**Time Allotted:** 20 Minutes (Strict) | Target Presentation: ~16--17 mins + Q&A Buffer  
**Proponents:** Ralph Paolo Dulce & Yahyah Odin  
**Thesis Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao  

---

## Presentation Flow & Speaking Split

| Slide | Topic | Primary Speaker | Slide Visual Type | Est. Time |
| :---: | :--- | :---: | :---: | :---: |
| **1** | Title & Introduction | Ralph | Metadata Banner | 1.0 min |
| **2** | Background: Legislative Inflation & Archival Noise | Ralph | **Figure Alone** (`sample_davao_city_ordinance_scan.png`) | 1.5 mins |
| **3** | Legal Foundation: Magtajas Doctrine & Ex-Ante Auditing | Ralph | Text Bullet Layout | 1.5 mins |
| **4** | Statement of the Problem | Ralph | Text Bullet Layout | 1.5 mins |
| **5** | Objectives of the Study | Ralph | Text Bullet Layout | 1.5 mins |
| **6** | Conceptual Framework: Retrieve-Then-Entail Pipeline | Ralph | **Figure Alone** (`conceptual_framework_flowchart.png`) | 1.5 mins |
| — | *Speaker Transition Handoff* | Ralph $\rightarrow$ Yah | Handoff | 10 secs |
| **7** | Chapter 3 Results: Dual Corpus & Token Compliance | Yah | **Figure Alone** (`dual_corpus_transformer_compliance.png`) | 1.5 mins |
| **8** | Proposed Methodology: Coarse-to-Fine Architecture Plan | Yah | **Figure Alone** (`JNLP_Framework_BW.png`) | 1.5 mins |
| **9** | Proposed Methodology: Stage 1 Hybrid Retrieval Plan | Yah | **Figure Alone** (`Phase_1_Retrieval_BW.png`) | 1.5 mins |
| **10** | Proposed Methodology: Stage 2 Cross-Encoder & XAI Plan | Yah | **Figure Alone** (`Phase_2_Entailment_BW.png`) | 1.5 mins |
| **11** | Proposed Methodology: Evaluation & Human Annotation Plan | Yah | Text / Matrix Layout | 1.5 mins |
| **12** | **Live Technical System Demonstration** | Yah | Live Screen Share | 3.5 mins |
| **13** | Project Status, Administrative Routing & Next Steps | Ralph & Yah | Text / Flow Layout | 1.5 mins |

---

## Slide-by-Slide Presentation Content

---

### Slide 1: Title Slide
* **Speaker:** Ralph Paolo Dulce
* **Header:** Computer Studies Cluster, School of Arts and Sciences | Ateneo de Davao University
* **Title:** A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances
* **Subtitle:** Using Information Retrieval and Natural Language Inference
* **Visual:** Ateneo de Davao University seal, thesis title banner, author credentials, adviser name

#### On-Screen Slide Content:
* Automated statutory conflict detection for local legislation
* Powered by hybrid information retrieval and cross-encoders
* Proactive **ex-ante evaluation** prior to formal enactment
* **Proponents:** Ralph Paolo Dulce & Yahyah Odin (BS Computer Science)
* **Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao

#### Spoken Script:
> "Good morning to the members of the evaluation panel, our thesis adviser Mr. Adrian Ablazo, and our course professor Ma'am Grace Tacadao. I am Ralph Paolo Dulce, and together with my co-author Yahyah Odin, we present our thesis proposal entitled: *'A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference.'*
> 
> In this presentation, we will walk you through our legal motivation, core research objectives, conceptual framework, exploratory data analysis results from Chapter 3, our proposed system methodology, and a live demonstration of our working prototype."

---

### Slide 2: Background: Legislative Inflation & Archival Noise
* **Speaker:** Ralph Paolo Dulce
* **Header:** Chapter 1: Introduction | Background of the Study
* **Title:** Statutory Growth & Fragmented Local Archives
* **Visual:** Authentic archival typewriter scan of a historical Davao City ordinance (`CS_Undergraduate_Thesis_Template/figs/sample_davao_city_ordinance_scan.png`)

#### On-Screen Slide Content:
`[FIGURE ALONE — NO ON-SCREEN TEXT]`  
*(Full-slide display of `sample_davao_city_ordinance_scan.png` showcasing historical typewriter noise, faded ink, bleed-through, and municipal seal stamps)*

#### Spoken Script:
> "Every functional legal system requires statutory consistency so that citizens clearly understand their obligations. However, the volume of modern legislation has grown so rapidly that human legal staff can no longer manually track every active rule.
> 
> In local government units like Davao City, this challenge is intensified. As you can see on screen, historical ordinances dating back to 1950 are preserved primarily as physical typewriter scans. These documents suffer from severe archival noise—faded ink, bleed-through, handwritten corrections, and overlapping official seals. These optical imperfections cause significant character degradation that breaks traditional keyword search engines. When council researchers are forced to rely on manual cross-referencing across multi-volume legal digests, latent conflicts can easily slip through into enacted law."

---

### Slide 3: Legal Foundation: Magtajas Doctrine & Ex-Ante Auditing
* **Speaker:** Ralph Paolo Dulce
* **Header:** Chapter 1: Introduction | Legal Motivation
* **Title:** The Magtajas Doctrine & Ex-Ante Auditing
* **Visual:** Conceptual layout of the Philippine statutory hierarchy

#### On-Screen Slide Content:
* Local governments hold strictly delegated legislative powers
* *Magtajas Doctrine* voids ordinances that contradict national statutes
* An ordinance cannot prohibit what a statute permits, or vice versa
* **Ex-ante auditing** identifies normative conflicts prior to enactment
* Aligns directly with **RA 11032** preventative regulatory review mandates

#### Spoken Script:
> "Under the Philippine legal system, local government units operate under delegated legislative authority governed by the Local Government Code. The foundational doctrine established in *Magtajas v. Pryce Properties* dictates that a local ordinance cannot permit what a statute forbids, nor forbid what a statute permits. Any local ordinance that contravenes a national statute is ultra vires and legally void from the beginning.
> 
> Passing an invalid ordinance triggers jurisdictional deadlocks, taxpayer lawsuits, and substantial administrative waste. To prevent this, our study introduces an **ex-ante audit**—an evaluation conducted 'before the event.' By auditing draft ordinances during committee review before their Second Reading, council legal staff can catch and reconcile conflicts while the text is still easily editable, fulfilling the preventative mandates of Republic Act 11032."

---

### Slide 4: Statement of the Problem
* **Speaker:** Ralph Paolo Dulce
* **Header:** Chapter 1: Introduction | Problem Statement
* **Title:** Statement of the Problem
* **Visual:** Structured problem statement layout

#### On-Screen Slide Content:
* **Q1:** What linguistic parameters define semantic conflicts in local drafts?
* **Q2:** How can Coarse-to-Fine retrieval scale over 176,000+ provisions on LGU hardware?
* **Q3:** Which hybrid IR and NLI combination maximizes conflict detection accuracy?
* **Q4:** What is the empirical performance on legal ground-truth conflict pairs?
* **Q5:** How usable is the decision-support tool for SP legal researchers?

#### Spoken Script:
> "To address these operational challenges, our research answers five specific questions:
> 
> First, what linguistic parameters and deontic modal verbs define a true legal conflict? Second, how can a decoupled Coarse-to-Fine architecture retrieve relevant candidate laws from tens of thousands of provisions on budget-constrained office hardware? Third, which combination of hybrid retrieval and natural language inference models delivers the highest accuracy? Fourth, what is the system's empirical performance when tested against verified legal ground-truth pairs? And fifth, how usable is the final decision-support tool for the legal staff of the Davao City Sangguniang Panlungsod?"

---

### Slide 5: Objectives of the Study
* **Speaker:** Ralph Paolo Dulce
* **Header:** Chapter 1: Introduction | Objectives of the Study
* **Title:** Research Objectives
* **Visual:** Objective matrix aligned with problem statements

#### On-Screen Slide Content:
* **Obj 1:** Characterize legislative archive degradation and text noise
* **Obj 2:** Design a decoupled two-stage Coarse-to-Fine architecture
* **Obj 3:** Implement a hybrid IR and NLI system for Philippine law
* **Obj 4:** Evaluate conflict detection accuracy against ground truth
* **Obj 5:** Deploy an interactive decision-support web application

#### Spoken Script:
> "Our research objectives map directly to these five questions:
> 
> First, we identify and characterize the structural noise across the digitized local archive. Second, we design an efficient Coarse-to-Fine pipeline that decouples broad candidate retrieval from compute-heavy cross-encoder inference. Third, we implement and calibrate a hybrid retrieval and NLI system tailored to Philippine statutory language. Fourth, we evaluate detection accuracy against verified legal ground-truth pairs. And fifth, we deploy an interactive, user-friendly web interface that alerts legal researchers to potential conflicts in real time."

---

### Slide 6: Conceptual Framework: Retrieve-Then-Entail Pipeline
* **Speaker:** Ralph Paolo Dulce
* **Header:** Chapter 2: Conceptual Framework
* **Title:** Conceptual Framework: Retrieve-Then-Entail Pipeline
* **Visual:** Complete Conceptual Framework flowchart (`CS_Undergraduate_Thesis_Template/figs/conceptual_framework_flowchart.png`)

#### On-Screen Slide Content:
`[FIGURE ALONE — NO ON-SCREEN TEXT]`  
*(Full-slide display of `conceptual_framework_flowchart.png` showing the end-to-end pipeline: Draft Ordinance Input $\rightarrow$ Provision Segmentation $\rightarrow$ Dual Statutory Knowledge Base $\rightarrow$ Stage 1 Coarse Retrieval $\rightarrow$ Stage 2 Fine Cross-Encoder NLI $\rightarrow$ Explainability Heatmaps $\rightarrow$ Ex-Ante Decision Advisory)*

#### Spoken Script:
> "Our conceptual framework adapts the proven 'Retrieve-Then-Entail' paradigm from the international Competition on Legal Information Extraction and Entailment (COLIEE).
> 
> As visualized in our framework diagram, the process begins when a proposed draft ordinance is uploaded. The text is preprocessed and parsed into discrete provisions. In Stage 1, the system performs high-throughput coarse retrieval against our Dual Statutory Knowledge Base—covering both superior national laws and existing city ordinances—to surface a compact candidate shortlist. In Stage 2, those shortlisted candidate pairs undergo deep pairwise Natural Language Inference, where the governing statute serves as the Premise and the draft provision serves as the Hypothesis. Finally, the system extracts token-level attention heatmaps to deliver an explainable advisory report for committee drafters.
> 
> I now hand the floor to my co-author Yahyah Odin to present our Chapter 3 exploratory data results, our proposed system methodology, and a live demonstration of our working prototype."

---

### Slide 7: Chapter 3 Results: Dual Statutory Corpus & Token Compliance
* **Speaker:** Yahyah Odin
* **Header:** Chapter 3: Methodology & Preliminary Results | Corpus Characterization
* **Title:** Dual Statutory Knowledge Base & Transformer Token Compliance
* **Visual:** Empirical token length compliance distribution curve (`CS_Undergraduate_Thesis_Template/figs/dual_corpus_transformer_compliance.png`)

#### On-Screen Slide Content:
`[FIGURE ALONE — NO ON-SCREEN TEXT]`  
*(Full-slide display of `dual_corpus_transformer_compliance.png` showing the token length distribution across national statutes and Davao City ordinances against the 512-token transformer boundary)*

#### Spoken Script:
> "Thank you, Ralph. Turning to our completed empirical work in Chapter 3, to evaluate proposed drafts against the full body of governing law, we constructed the first Unified Dual Statutory Knowledge Base. This repository integrates 27,096 enactments comprising 176,421 searchable provisions in standardized JSONL format—combining 25,432 national statutes from 1901 to 2026 with 1,664 digitized Davao City local ordinances across four legislative eras.
> 
> As demonstrated in our empirical distribution figure on screen, exactly 94.69% of all provisions across both corpora naturally fall within the standard 512-token transformer limit, with a median length of 84 tokens and a mean of 127 tokens. This empirical result is critical: it validates our core methodological assumption that statutory provisions can be directly ingested by standard transformer models without aggressive chunking or splitting, preserving the full normative context and penalty clauses intact."

---

### Slide 8: Proposed Methodology: Coarse-to-Fine Architecture Plan
* **Speaker:** Yahyah Odin
* **Header:** Chapter 3: Methodology | System Architecture Plan
* **Title:** Planned Coarse-to-Fine Computational Pipeline
* **Visual:** System architecture blueprint (`CS_Undergraduate_Thesis_Template/figs/JNLP_Framework_BW.png`)

#### On-Screen Slide Content:
`[FIGURE ALONE — NO ON-SCREEN TEXT]`  
*(Full-slide display of `JNLP_Framework_BW.png` illustrating the two-stage decoupled pipeline from draft input to top-50 candidate filtering and cross-encoder inference)*

#### Spoken Script:
> "Moving to our proposed methodology, evaluating a multi-section draft ordinance against 176,421 statutory provisions pairwise using deep neural transformers would require millions of comparisons, crashing standard office hardware and taking hours per audit.
> 
> To make automated conflict detection feasible on consumer LGU computers, we propose a decoupled Coarse-to-Fine architecture. As shown in our architectural diagram, Stage 1 acts as a rapid, high-throughput coarse filter: it searches the entire 176,000-provision corpus and shortlists the top-50 most relevant candidate provisions in milliseconds. Stage 2 is our fine-grained inference engine: a dedicated cross-encoder evaluates only those 50 shortlisted pairs, performing deep bidirectional attention to classify the relationship as Entailment, Neutral, or Contradiction. This proposed decoupling combines sub-second response speeds with deep neural classification accuracy."

---

### Slide 9: Proposed Methodology: Stage 1 Hybrid Retrieval Plan
* **Speaker:** Yahyah Odin
* **Header:** Chapter 3: Methodology | Retrieval Engine Plan
* **Title:** Planned Hybrid Search & Rank Fusion Algorithm
* **Visual:** Stage 1 retrieval flow diagram (`CS_Undergraduate_Thesis_Template/figs/Phase_1_Retrieval_BW.png`)

#### On-Screen Slide Content:
`[FIGURE ALONE — NO ON-SCREEN TEXT]`  
*(Full-slide display of `Phase_1_Retrieval_BW.png` showing parallel sparse BM25 and dense bi-encoder indexing, Reciprocal Rank Fusion ($k=60$), and the Hierarchy Priority Safeguard)*

#### Spoken Script:
> "In our proposed Stage 1 retrieval engine, relying solely on keyword matching fails when a draft paraphrases legal concepts, while relying solely on dense vector embeddings can miss explicit Republic Act citations.
> 
> We propose a hybrid architecture that executes two parallel search pipelines: a sparse BM25 retriever for exact legal citations and statutory titles, and a lightweight dense bi-encoder, `all-MiniLM-L6-v2`, for capturing semantic paraphrasing. Rather than attempting fragile raw score normalization across disparate models, our pipeline merges the candidate lists using Reciprocal Rank Fusion with constant $k=60$. Furthermore, we incorporate a Hierarchy Priority Safeguard that automatically elevates primary Republic Acts during preemption checks, guaranteeing that governing national laws are never dropped from the candidate pool."

---

### Slide 10: Proposed Methodology: Stage 2 Cross-Encoder & XAI Plan
* **Speaker:** Yahyah Odin
* **Header:** Chapter 3: Methodology | Inference & Explainability Plan
* **Title:** Planned Cross-Encoder NLI & Self-Attention Explainability
* **Visual:** Stage 2 cross-encoder architecture and attention matrix (`CS_Undergraduate_Thesis_Template/figs/Phase_2_Entailment_BW.png`)

#### On-Screen Slide Content:
`[FIGURE ALONE — NO ON-SCREEN TEXT]`  
*(Full-slide display of `Phase_2_Entailment_BW.png` showing concatenated Premise-Hypothesis ingestion, single-tower cross-attention layers, 3-class classification head, and attention attribution matrix)*

#### Spoken Script:
> "For Stage 2, candidate pairs pass into a single-tower Cross-Encoder. Unlike bi-encoders that process sentences separately, our cross-encoder architecture concatenates the statutory premise and draft hypothesis into a single sequence, allowing every token in the ordinance to directly cross-attend to every token in the national statute.
> 
> We plan to adapt candidate models such as DeBERTa-v3 using supervised fine-tuning on legal premise-hypothesis pairs to overcome the affirmative entailment bias common in general language models. Crucially, to make the system transparent and trustworthy for council legal officers, the pipeline extracts self-attention weights to generate token-level attribution heatmaps. This directly pinpoints the conflicting clauses—such as an unauthorized penalty ceiling or a preempted regulatory standard—providing legal staff with an immediate, verifiable audit trail."

---

### Slide 11: Proposed Methodology: Evaluation & Human Annotation Plan
* **Speaker:** Yahyah Odin
* **Header:** Chapter 3: Methodology | Experimental & Human Evaluation Plan
* **Title:** Planned Evaluation Benchmark & Human Study Protocol
* **Visual:** Evaluation matrix showing ground-truth benchmark tiers and human evaluation design

#### On-Screen Slide Content:
* **Ground-Truth Benchmark Plan:** 350 statutory pairs stratified across 3 difficulty tiers
  * Tier 1 (Direct Lexical Overlap), Tier 2 (Semantic Paraphrasing), Tier 3 (Cross-Domain Conflict)
* **Stage 1 IR Metrics:** Recall@K ($K \in \{10, 20, 50\}$) and Mean Reciprocal Rank (MRR)
* **Stage 2 NLI Metrics:** Macro $F_1$, Conflict Class $F_1$, Precision, Recall, and Accuracy
* **Human Subject Evaluation:** 15 Sangguniang Panlungsod legal researchers evaluating 70 pairs each
* **User Usability & Reliability Metrics:** Inter-Annotator Agreement (Cohen's $\kappa$), System Usability Scale (SUS), and PSSUQ

#### Spoken Script:
> "To validate our system under Research Objectives 4 and 5, our methodology establishes a two-tiered evaluation protocol.
> 
> First, for automated model benchmarking, we plan to evaluate across a curated ground-truth dataset of 350 statutory pairs stratified across three difficulty tiers: direct lexical overlap, semantic paraphrasing, and subtle cross-domain conflicts. We will measure retrieval completeness using Recall@K and MRR, and classification performance using Macro F1 and Conflict Class F1.
> 
> Second, for human evaluation under Objective 5, we have designed a formal user study protocol involving 15 legal researchers from the Davao City Sangguniang Panlungsod. Each evaluator will review 70 pairs through structured Google Forms. We will measure inter-annotator agreement using Cohen's kappa, and evaluate overall software usability using the System Usability Scale and Post-Study System Usability Questionnaire."

---

### Slide 12: Live Technical System Demonstration
* **Speaker:** Yahyah Odin
* **Header:** Prototype Demonstration | Interactive Decision-Support Tool
* **Title:** Live System Demonstration
* **Visual:** **LIVE SCREEN SHARE** of the interactive web prototype (Draft upload, Reddit-style hierarchical tree, real-time audit, and XAI heatmap)

#### On-Screen Slide Content:
* Interactive decision-support web application for local LGU deployment
* Parses draft ordinances into **Reddit-style hierarchical section trees**
* Sub-second dual-corpus retrieval surfaces relevant candidate laws
* Real-time cross-encoder classifies normative conflicts
* Visualizes **token-level attention heatmaps** and exports audit reports

#### Live Demo Walkthrough Script:
> 1. **(Upload & Document Parsing - 0:45):**  
>    "Now, we transition directly to our working technical prototype. What you see on screen is our interactive decision-support application, designed for local deployment within the city council network. We begin by uploading a draft ordinance—here, a proposed measure regulating public utility tricycles."
> 
> 2. **(Hierarchical Section View - 0:45):**  
>    "The application immediately parses the draft into a structured, Reddit-style hierarchical tree. Legal researchers can collapse, expand, and inspect individual sections, clauses, and penalty provisions, making multi-page legislation effortless to navigate."
> 
> 3. **(Real-Time Audit & Conflict Detection - 1:00):**  
>    "When we initiate the statutory audit, Stage 1 searches across the 176,421 provisions in milliseconds, surfacing relevant sections from Republic Act 4136 and related city ordinances. Stage 2 immediately evaluates the pairs. Notice Section 5: the draft ordinance imposes an absolute municipal fine of 15,000 pesos. The system immediately flags a High-Confidence Contradiction!"
> 
> 4. **(Explainable Attention Heatmap & Export - 1:00):**  
>    "When we click 'Inspect Rationales,' the system displays the token-level cross-attention heatmap. It highlights the exact conflict: the draft's 15,000-peso fine directly violates Section 458 of Republic Act 7160, which caps municipal ordinance penalties at 5,000 pesos. Drafters can immediately export this finding into a formal Legislative Audit Report for committee review."

---

### Slide 13: Project Status, Administrative Routing & Next Steps
* **Speaker:** Ralph Paolo Dulce & Yahyah Odin
* **Header:** Project Status & Roadmap | Sangguniang Panlungsod Evaluation
* **Title:** Current Progress Summary & Next Steps
* **Visual:** Administrative routing workflow (Sangguniang Panlungsod $\rightarrow$ HRMO / City Administrator $\rightarrow$ 15 Legal Researchers $\rightarrow$ Civil Service 201 Commendation)

#### On-Screen Slide Content:
* Chapters 1 to 3 fully drafted; dual statutory knowledge base compiled
* 176,421 provisions indexed and validated for transformer compliance
* Two-stage Coarse-to-Fine architecture and hybrid algorithms formally defined
* Functional web application prototype completed with live demonstration
* SP endorsement received; routing via HRMO and City Administrator for 15 annotators
* Preparing human evaluation with Civil Service 201 Commendation certificates

#### Spoken Script:
> **(Ralph):**  
> "To summarize our progress: we have completed the full manuscript draft for Chapters 1 through 3, compiled and verified our dual statutory knowledge base of 27,096 enactments, formally defined our two-stage architecture, and developed a fully functioning interactive web prototype.
> 
> **(Yah):**  
> Regarding our immediate next steps: following the favorable endorsement from Sangguniang Panlungsod Acting Department Head Ma. Theresa Reyes, our formal approval packet is currently routing through the City Administrator's Office via HRMO. Once cleared, we will execute our human evaluation with the 15 city legal researchers, measuring usability and inter-annotator agreement, with official commendations awarded for their Civil Service 201 records.
> 
> That concludes our proposal defense presentation. Thank you very much, and we welcome the comments and guidance of our evaluation panel."

---

## Panel Q&A Quick Reference (Common Inquiries)

### 1. "What is your main technical and practical contribution?"
* **Answer:** "Technically, we designed a computationally efficient Coarse-to-Fine pipeline that combines hybrid retrieval with fine-tuned cross-encoders to run deep conflict detection on consumer LGU computers without cloud dependencies. Practically, we built an ex-ante decision-support tool that helps local governments prevent legally void ordinances and protect citizens' constitutional rights before laws are enacted."

### 2. "Why not just use ChatGPT or a commercial cloud API?"
* **Answer:** "In a local government setting, cloud APIs have three major drawbacks: First, data privacy—uploading unapproved government drafts to commercial cloud servers raises compliance concerns under Republic Act 10173. Second, cost—recurring per-page API fees are unsustainable for municipal budgets. Third, reliability—cloud LLMs often suffer from affirmative bias and hallucination. Our open-weight models run 100% offline, cost nothing to operate, and provide transparent attention heatmaps."

### 3. "Why are you presenting preliminary corpus exploratory results rather than full model evaluation in this proposal defense?"
* **Answer:** "In accordance with our thesis proposal guidelines covering Chapters 1 through 3, our primary completed empirical milestone is the comprehensive assembly, archival digitization, and exploratory data analysis of our 27,096-enactment dual knowledge base, including the validation of the 94.69% transformer compliance rate. The deep neural cross-encoder training and benchmark experiments represent our planned methodology in Chapter 3, which we will fully execute and report upon defending our methodology."

### 4. "What is the status of your data and testing with actual legal staff?"
* **Answer:** "We have already compiled and structured 27,096 laws and 1,664 local ordinances. For the human evaluation, the Sangguniang Panlungsod has endorsed our study and referred it to the City Administrator through HRMO. We have prepared the testing packets and Google Forms, and we are ready to deploy the evaluation with 15 legal researchers as soon as administrative clearance is finalized."

### 5. "Why decouple coarse retrieval and fine NLI cross-encoders?"
* **Answer:** "Comparing a multi-provision draft ordinance pairwise against all 176,421 statutory provisions using a cross-encoder would require millions of deep transformer passes, taking hours and exceeding the memory limits of office computers. Decoupling allows Stage 1 to filter the entire corpus down to 50 candidates in milliseconds using lightweight hybrid search, allowing Stage 2 to apply deep bidirectional attention strictly where it matters."
