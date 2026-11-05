# **Stage 2 Candidate Models Research & Selection Report**

**Thesis Title:** *A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference*  
**Authors:** Ralph Paolo Dulce & Yahyah Odin  
**Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao  
**Institution:** Department of Computer Science, Ateneo de Davao University  
**Date:** September 23, 2026  
**Status:** Comprehensive Architecture & Benchmark Audit for Stage 2 (Fine NLI / Cross-Encoder Semantic Conflict Detection)

---

## **Executive Summary**

In this thesis, **Stage 2 (Fine Natural Language Inference / Cross-Encoder Semantic Conflict Detection)** is responsible for deep logical reasoning. Given an asymmetric input sequence consisting of a retrieved national statutory provision (Premise, $P$) and a draft Davao City municipal ordinance clause (Hypothesis, $H$), Stage 2 performs calibrated sequence classification across three formal classes:
$$\mathcal{Y} = \{\text{Entailment}, \text{Contradiction}, \text{Neutral}\}$$
with a primary optimization focus on **$\text{Contradiction}$** to detect statutory preemption under the *Magtajas v. Pryce Properties* doctrine and RA 7160 §5(a).

While our initial experimental baseline evaluated three architectures:
1. `all-MiniLM-L6-v2` (22M parameters) — Compact, distilled edge baseline.
2. `deberta-v3-base` (86M parameters) — Disentangled attention workhorse.
3. `ModernBERT-base` (149M parameters) — 8,192-token modern architecture with FlashAttention-2 and RoPE.

This report conducts an exhaustive evaluation across contemporary NLP leaderboards—specifically **LexGLUE**, **Hugging Face NLI / Zero-Shot benchmarks (MNLI, FEVER, ANLI, WANLI)**, **COLIEE Task 4 (Statutory Legal Textual Entailment)**, and **MTEB Reranking**—to compile a comprehensive **28-Model Master Long List** and select the **Top 10 Official Candidate Models** for empirical ablation on our Philippine statutory ground truth benchmark ($N = 350$, static 70/15/15 split).

---

## **1. Design Requirements & Operational Constraints**

All candidate models must satisfy five strict operational criteria grounded in the realistic capacity of Philippine Local Government Units (LGUs):

| Criterion | Operational Requirement | Thesis Justification |
| :--- | :--- | :--- |
| **Deterministic Classification** | Encoder-only or lightweight seq2seq classification head; softmax probabilities over $\{\text{Ent}, \text{Cont}, \text{Neu}\}$. | **Absolute exclusion of autoregressive generative LLMs** (GPT-4, LLaMA, Mistral) to eliminate legal hallucinations, ungrounded rewriting, and non-deterministic outputs. |
| **Hardware & VRAM Budget** | $\le 600\text{M}$ parameters; fp16 training footprint $\le 6.5\text{GB}$ VRAM; fp16/int8 inference $\le 2\text{GB}$ VRAM. | Fits within **Workstation A (AMD Radeon RX 6600, 8GB VRAM)** simulating LGU IT infrastructure, and trainable on **Workstation B (Lenovo Legion 5 RTX 5050 Laptop GPU / Google Colab T4)**. |
| **Edge Throughput & Latency** | Parallel batch inference of $k=50$ retrieved candidate pairs in $\le 5\text{ seconds}$ on GPU, or $\le 15\text{ seconds}$ on CPU. | Real-time First Reading and Second Reading legislative review during active Sangguniang Panlungsod sessions cannot endure minute-long queuing latency. |
| **Negation & Deontic Sensitivity** | Robustness against superficial lexical overlap; capacity to distinguish permissions (*may*) from prohibitions (*shall not*). | Addresses **affirmative bias**—the tendency of general-domain language models to presume pairs are harmonious unless prompted by superficial lexical negation markers. |
| **Few-Shot Domain Transfer** | High sample efficiency on $N_{\text{train}} = 245$ training pairs without catastrophic forgetting of general syntactic logic. | Curated legal ground truth datasets are inherently low-resource due to the extreme cognitive cost of expert attorney annotation. |

---

## **2. Master Long List of Candidate Models (28 Architectures)**

The candidate space is organized into seven distinct architectural and domain families:

### **Family 1: Legal-Domain Pretrained Encoders (LexGLUE & Legal NLP Specialists)**
1. **`nlpaueb/legal-bert-base-uncased` (LEGAL-BERT)**: 110M params, 512 tokens. Pretrained from scratch on 12GB of diverse English legal text (EU/UK legislation, ECHR/ECJ cases, US contracts, US court cases) with a custom legal vocabulary (Chalkidis et al., 2020). Top-ranked base model in LexGLUE (Mean F1: 79.8%).
2. **`pile-of-law/legalbert-large-1.7M-2` (PoL-BERT-Large)**: 340M params, 512 tokens. Pretrained on the 256GB "Pile of Law" dataset (Henderson et al., NeurIPS 2022) encompassing Federal Register, US Code, state codes, municipal regulations, and court filings. Directly matches municipal regulatory syntax.
3. **`law-ai/InLegalBERT`**: 110M params, 512 tokens. Pretrained on Indian Supreme Court/High Court cases and statutes (Paul et al., 2022). Tests transfer from common-law hierarchical statutory jurisdictions.
4. **`zlucia/custom-legalbert` (CaseLaw-BERT)**: 110M params, 512 tokens. Pretrained on Harvard Caselaw Access Project (37GB US case law) (Zheng et al., 2021). Ranked #2 in LexGLUE (Mean F1: 79.4%).
5. **`thunlp/Lawformer`**: 110M params, 4,096 tokens. Longformer-based legal model designed for long legal documents (Xiao et al., 2021).

### **Family 2: Pre-Trained NLI / Cross-Encoder Specialists (Hugging Face & SuperGLUE Leaders)**
6. **`MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli`**: 86M params, 512 tokens. Pre-aligned specifically on MNLI, FEVER-NLI, and Adversarial NLI (ANLI). Provides a warm NLI initialization where the model already understands directional contradiction before seeing Philippine data.
7. **`MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli`**: 435M params, 512 tokens. Pre-aligned on MNLI, FEVER, ANLI (R1-R3), LingNLI, and WANLI. Ranked among the #1 best sub-1B parameter zero-shot NLI models on Hugging Face.
8. **`cross-encoder/nli-deberta-v3-base`**: 86M params, 512 tokens. Sentence-Transformers native cross-encoder fine-tuned on SNLI + MultiNLI (AllNLI).
9. **`FacebookAI/roberta-large-mnli`**: 355M params, 512 tokens. Meta AI's classic NLI model. Canonical baseline established by Rabelo et al. (2022) for COLIEE Task 4.
10. **`facebook/bart-large-mnli`**: 406M params, 1,024 tokens. Sequence-to-sequence zero-shot sequence classification gold standard (Lewis et al., 2019).
11. **`google/electra-large-discriminator`**: 335M params, 512 tokens. Trained via Replaced Token Detection (RTD), optimizing 100% of tokens during pretraining. Outperformed RoBERTa-large on SuperGLUE with superior sample efficiency.
12. **`google/electra-base-discriminator`**: 110M params, 512 tokens. Compact RTD architecture for efficient few-shot transfer.

### **Family 3: Long-Context & Modern Architecture Scalers (>2K / 8K Tokens)**
13. **`answerdotai/ModernBERT-large`**: 395M params, **8,192 tokens**. Modernized encoder featuring FlashAttention-2, Rotary Positional Embeddings (RoPE), GeGLU activations, and unpadding (Warner et al., 2024). Direct scale ablation for ModernBERT-base.
14. **`allenai/longformer-base-4096`**: 149M params, **4,096 tokens**. Local sliding window attention combined with global attention on `[CLS]` (Beltagy et al., 2020). Top long-context model in LexGLUE (Mean F1: 78.5%).
15. **`google/bigbird-roberta-base`**: 128M params, **4,096 tokens**. Block sparse attention ($O(n)$ complexity) combining random, window, and global attention (Zaheer et al., 2020).
16. **`nomic-ai/nomic-bert-2048`**: 137M params, **2,048 tokens**. BERT modernized with RoPE, SwiGLU, and FlashAttention (Nussbaum et al., 2024).

### **Family 4: Native Cross-Encoder Rerankers (Retrieval-to-Inference Bridges)**
17. **`BAAI/bge-reranker-v2-m3`**: 568M params, **8,192 tokens**. Multilingual cross-encoder trained on multi-stage contrastive and hard negative pairs. Extensively deployed in COLIEE 2025/2026 pipelines.
18. **`BAAI/bge-reranker-base`**: 278M params, 512 tokens. XLM-RoBERTa-based cross-encoder for semantic relevance and pairwise entailment.
19. **`cross-encoder/ms-marco-MiniLM-L-12-v2`**: 33M params, 512 tokens. 12-layer distilled cross-encoder; 50% deeper than L6.

### **Family 5: Multilingual & Local/Regional Language Transfer (Philippine Context)**
20. **`microsoft/mdeberta-v3-base`**: 86M params, 512 tokens. Multilingual DeBERTa-v3 across 100+ languages with disentangled attention. Resilient to Philippine loanwords, administrative Spanish terms (*ultra vires*, *ex-officio*), and English-Tagalog code-switching.
21. **`FacebookAI/xlm-roberta-base`**: 270M params, 512 tokens. Multilingual RoBERTa trained on 2.5TB CommonCrawl text in 100 languages (Conneau et al., 2020).
22. **`FacebookAI/xlm-roberta-large`**: 550M params, 512 tokens. Scaled cross-lingual representation for complex multilingual statutory parsing.
23. **`jcblaise/roberta-tagalog-base`**: 110M params, 512 tokens. Pretrained exclusively on Philippine text (Tagalog Wikipedia, News, CommonCrawl) by Cruz & Cheng (2020).

### **Family 6: Ultra-Lightweight & Compressed Edge Models (<100M Params, CPU Edge Viability)**
24. **`distilbert/distilbert-base-uncased`**: 66M params, 512 tokens. 40% smaller and 60% faster than BERT; retains 97% of language comprehension (Sanh et al., 2019).
25. **`cross-encoder/nli-distilroberta-base`**: 82M params, 512 tokens. Distilled RoBERTa specifically fine-tuned for fast NLI inference.
26. **`albert/albert-base-v2`**: 12M params, 512 tokens. Cross-layer parameter sharing; occupies only ~45MB of RAM (Lan et al., 2020).
27. **`microsoft/deberta-v3-xsmall`**: 22M params, 512 tokens. Ultra-compact disentangled attention model; direct structural competitor to `all-MiniLM-L6-v2`.

### **Family 7: Instruction-Tuned & Specialized Legal Reasoners (Encoder-Decoder & SLMs)**
28. **`law-instruct/FLawN-T5` / `google/flan-t5-base`**: 250M params, 2,048 tokens. Instruction-tuned seq2seq model fine-tuned on the LawInstruct dataset (Niklaus et al., 2024); demonstrates +50% improvement on LegalBench.

---

## **3. The Top 10 Recommended Candidate Models (Beyond the Initial 3)**

From the master list of 28 architectures, the following **Top 10 Official Candidates** are recommended to add alongside `MiniLM-L6-v2`, `DeBERTa-v3-base`, and `ModernBERT-base`. They are specifically selected to test distinct, complementary hypotheses across parameter scale, domain pretraining, context length, and sample efficiency:

```
                                  TOP 10 CANDIDATE SELECTION TAXONOMY
                                  
   Domain Pretraining          NLI Pre-Alignment          Long-Context Scaling       Multilingual / Edge
 ┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
 │ 1. LEGAL-BERT        │   │ 3. DeBERTa-v3-NLI    │   │ 5. ModernBERT-large  │   │ 8. mDeBERTa-v3-base  │
 │    (Chalkidis, 110M) │   │    (Laurer, 86M)     │   │    (Answer.AI, 395M) │   │    (Microsoft, 86M)  │
 │                      │   │                      │   │                      │   │                      │
 │ 2. PoL-BERT-Large    │   │ 4. DeBERTa-v3-L-NLI  │   │ 6. BGE-Reranker-v2-m3│   │ 9. ELECTRA-large     │
 │    (Henderson, 340M) │   │    (Laurer, 435M)    │   │    (BAAI, 568M, 8K)  │   │    (Google RTD, 335M)│
 └──────────────────────┘   │                      │   │                      │   │                      │
                            │ 7. RoBERTa-large-mnli│   └──────────────────────┘   │ 10. nli-distilroberta│
                            │   (COLIEE Base, 355M)│                              │    (Edge CPU, 82M)   │
                            └──────────────────────┘                              └──────────────────────┘
```

### **1. `nlpaueb/legal-bert-base-uncased` (LexGLUE Gold Standard Legal Encoder)**
* **Hugging Face Hub:** `nlpaueb/legal-bert-base-uncased` | **Parameters:** 110M | **Context:** 512 tokens
* **Pretraining Domain:** 12GB of specialized English legal text (legislation, court cases, contracts) with custom legal vocabulary.
* **Why Official Candidate:** Authoritative benchmark model from Chalkidis et al. (2020) and LexGLUE. Directly tests the hypothesis: *"Does domain-specific legal vocabulary pretraining outperform general-domain language models on Philippine statutory conflict detection?"*

### **2. `pile-of-law/legalbert-large-1.7M-2` (PoL-BERT-Large — Administrative & Statutory Corpus)**
* **Hugging Face Hub:** `pile-of-law/legalbert-large-1.7M-2` | **Parameters:** 340M | **Context:** 512 tokens
* **Pretraining Domain:** 256GB "Pile of Law" dataset (Henderson et al., NeurIPS 2022) heavily weighted toward statutory codifications and administrative regulations.
* **Why Official Candidate:** Perfectly mirrors the legislative hierarchy of our problem setting. Evaluates whether massive statutory pretraining at the 340M parameter scale improves the capture of subtle preemption exceptions.

### **3. `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli` (Pre-Aligned NLI Champion — Base Scale)**
* **Hugging Face Hub:** `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli` | **Parameters:** 86M | **Context:** 512 tokens
* **Pretraining Domain:** Fine-tuned on MNLI + FEVER-NLI + Adversarial NLI (ANLI).
* **Why Official Candidate:** In our few-shot fine-tuning regime ($N_{\text{train}} = 245$), starting from a raw Masked Language Model (like raw `microsoft/deberta-v3-base`) requires the classification head to learn the concept of logical contradiction from scratch. Starting from an already NLI-aligned checkpoint allows the model to retain adversarial negation sensitivity while adapting purely to statutory semantics, mitigating affirmative bias.

### **4. `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` (Performance Ceiling Upper Bound)**
* **Hugging Face Hub:** `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` | **Parameters:** 435M | **Context:** 512 tokens
* **Pretraining Domain:** Pre-aligned on MNLI, FEVER, ANLI (R1-R3), LingNLI, and WANLI.
* **Why Official Candidate:** Widely acknowledged as the highest-performing sub-1B parameter NLI model on Hugging Face. Serves as our empirical "quality ceiling" to evaluate how close lightweight edge models approach the maximum achievable NLI reasoning accuracy.

### **5. `answerdotai/ModernBERT-large` (Modern 8,192-Token Long-Context Scaler)**
* **Hugging Face Hub:** `answerdotai/ModernBERT-large` | **Parameters:** 395M | **Context:** **8,192 tokens**
* **Pretraining Domain:** 2 Trillion tokens; FlashAttention-2, RoPE, GeGLU, unpadding.
* **Why Official Candidate:** Direct scaling companion to `ModernBERT-base` (149M $\rightarrow$ 395M). Tests whether scaling modern encoder parameters improves conflict detection across long statutory codifications (the 5.17% of statutory sections exceeding 512 tokens) without requiring sliding window chunking.

### **6. `BAAI/bge-reranker-v2-m3` (Native Cross-Encoder, 8,192 Context, Multilingual)**
* **Hugging Face Hub:** `BAAI/bge-reranker-v2-m3` | **Parameters:** 568M | **Context:** **8,192 tokens**
* **Pretraining Domain:** Multilingual (100+ languages) cross-encoder trained on dense contrastive pairs and hard negatives.
* **Why Official Candidate:** Evaluated in recent COLIEE 2025/2026 winning systems. Combines native cross-attention, full 8,192-token context, and multilingual robustness in a single architecture. Serves as the natural logical counterpart to our Stage 1 `bge-m3` bi-encoder.

### **7. `FacebookAI/roberta-large-mnli` (Canonical Literature Baseline)**
* **Hugging Face Hub:** `FacebookAI/roberta-large-mnli` | **Parameters:** 355M | **Context:** 512 tokens
* **Pretraining Domain:** Pretrained on 160GB text + fine-tuned on MNLI (392k pairs).
* **Why Official Candidate:** Mandatory baseline cited in Rabelo et al. (2022) for COLIEE Task 4, Williams et al. (2022), and extensively across Chapter 3 (§3.6). Evaluating this model empirically validates our hypothesis that unadapted zero-shot general models fail at legal preemption due to affirmative bias.

### **8. `microsoft/mdeberta-v3-base` (Multilingual Disentangled Logic for Local Context)**
* **Hugging Face Hub:** `microsoft/mdeberta-v3-base` | **Parameters:** 86M | **Context:** 512 tokens
* **Pretraining Domain:** Multilingual pretraining across 100+ languages with disentangled attention.
* **Why Official Candidate:** Directly tests resilience against localized administrative Taglish, Spanish legal loanwords (*ex-officio*, *ultra vires*, *in rem*), and Cebuano translation mandates under LGC §469 and the *Batas sa Sariling Wika Act*, while preserving DeBERTa's superior disentangled syntactic attention.

### **9. `google/electra-large-discriminator` (Replaced-Token Sample Efficiency Specialist)**
* **Hugging Face Hub:** `google/electra-large-discriminator` | **Parameters:** 335M | **Context:** 512 tokens
* **Pretraining Domain:** Replaced Token Detection (RTD) over all sequence tokens.
* **Why Official Candidate:** RTD provides loss feedback across 100% of input tokens rather than just the 15% masked in standard BERT. Clark et al. (2020) proved this achieves unmatched sample efficiency on small datasets like RTE and MNLI, making it ideal for our 245-pair training split.

### **10. `cross-encoder/nli-distilroberta-base` (Extreme Edge LGU Efficiency Baseline)**
* **Hugging Face Hub:** `cross-encoder/nli-distilroberta-base` | **Parameters:** 82M | **Context:** 512 tokens
* **Pretraining Domain:** Knowledge-distilled RoBERTa fine-tuned on SNLI + MNLI.
* **Why Official Candidate:** Provides a dedicated, low-latency CPU baseline for municipal desktop PCs operating without dedicated GPUs. Tests the lower boundary of edge computational feasibility.

---

## **4. Comparative Technical Matrix: 13 Total Candidate Models**

The following table presents the complete evaluation matrix comparing our 3 initial architectures alongside the Top 10 recommended candidates:

| # | Candidate Model Identifier | Parameter Count | Context Window | Architectural Paradigm | Target Evaluation Role in Thesis | Est. fp16 VRAM | Edge Hardware Feasibility (RX 6600 / CPU) |
| :---: | :--- | :---: | :---: | :--- | :--- | :---: | :--- |
| *0a* | `sentence-transformers/all-MiniLM-L6-v2` *(Current)* | 22M | 512 | Distilled Transformer | Lightweight Distillation Baseline | ~0.2 GB | **Optimal**: Sub-second CPU/GPU inference |
| *0b* | `microsoft/deberta-v3-base` *(Current)* | 86M | 512 | Disentangled Attention | Core Disentangled Workhorse | ~0.5 GB | **High**: ~4s batch inference on GPU |
| *0c* | `answerdotai/ModernBERT-base` *(Current)* | 149M | **8,192** | FlashAttention-2 / RoPE | Native Long-Context Baseline | ~0.8 GB | **High**: Fast FlashAttention on GPU |
| **1** | `nlpaueb/legal-bert-base-uncased` | 110M | 512 | Legal Domain Pretrained | LexGLUE Legal Pretraining Benchmark | ~0.6 GB | **High**: Fast edge deployment |
| **2** | `pile-of-law/legalbert-large-1.7M-2` | 340M | 512 | Large Administrative Domain | Statutory Preemption Corpus Benchmark | ~1.4 GB | **Moderate**: Smooth GPU inference (~1.4GB) |
| **3** | `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli` | 86M | 512 | Pre-Aligned NLI (ANLI+FEVER) | Transfer Learning / NLI Pre-Alignment | ~0.5 GB | **High**: Identical footprint to DeBERTa-base |
| **4** | `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` | 435M | 512 | Scaled Pre-Aligned NLI (WANLI) | Empirical Reasoning Quality Ceiling | ~1.8 GB | **Moderate**: Fits comfortably in 8GB VRAM |
| **5** | `answerdotai/ModernBERT-large` | 395M | **8,192** | Modern Long-Context Scaled | Long-Context Scale Ablation (vs Base) | ~1.6 GB | **Moderate**: FlashAttention-2 optimized |
| **6** | `BAAI/bge-reranker-v2-m3` | 568M | **8,192** | Multilingual Cross-Encoder | End-to-End Multilingual & Long Context | ~2.3 GB | **Moderate**: Fits in 8GB VRAM; heavy on CPU |
| **7** | `FacebookAI/roberta-large-mnli` | 355M | 512 | Unadapted Pretrained NLI | Mandatory COLIEE Task 4 Zero-Shot Baseline | ~1.5 GB | **Moderate**: Benchmark reference standard |
| **8** | `microsoft/mdeberta-v3-base` | 86M | 512 | Multilingual Disentangled | Taglish & Regional Translation Robustness | ~0.5 GB | **High**: Efficient edge execution |
| **9** | `google/electra-large-discriminator` | 335M | 512 | Replaced Token Detection (RTD) | Few-Shot Sample Efficiency Specialist | ~1.4 GB | **Moderate**: Highly stable training dynamics |
| **10** | `cross-encoder/nli-distilroberta-base` | 82M | 512 | Distilled NLI Cross-Encoder | Edge CPU Latency / Resource Baseline | ~0.4 GB | **Optimal**: Sub-second on standard LGU CPU |

---

## **5. Recommended Experimental Strategy for Chapter 4 Ablation**

To ensure maximum scientific rigor during Milestone 3 (Results & Discussion) while conserving compute hours, we recommend a **Two-Tier Experimental Evaluation Protocol**:

### **Tier A: Zero-Shot Out-of-the-Box Screening ($N_{\text{test}} = 53$)**
* Run all 13 candidate models zero-shot (without fine-tuning) on the held-out test set $\mathcal{D}_{\text{test}}$.
* Evaluates intrinsic pre-alignment and confirms the extent of **affirmative bias** in unadapted models versus legal-pretrained and NLI-prealigned models.
* Generates zero-shot baseline metrics for Table 4.2 in Chapter 4.

### **Tier B: Supervised Fine-Tuning Sweep ($N_{\text{train}} = 245$, $N_{\text{val}} = 52$, $N_{\text{test}} = 53$)**
* Fine-tune the candidate models using the standardized grid search protocol ($\eta \in \{1\times 10^{-5}, 2\times 10^{-5}, 3\times 10^{-5}\}$, $B = 8$, AdamW, linear decay, early stopping patience = 4).
* Track training and validation loss curves across 10 epochs.
* Sweep cost-sensitive threshold $\tau \in [0.25, 0.50]$ to maximize $F_2$-score for conflict recall.
* Perform statistical significance testing:
  - **Friedman Test** across all fine-tuned candidates on test set predictions.
  - **McNemar's Test** ($p < 0.05$) between the top-performing candidate and the baseline (`roberta-large-mnli` / `MiniLM`).

---

## **6. Summary of Key Recommendations for Yah**

1. **Adopt the Top 10 Selection:** Include these 10 candidate models in Chapter 3 (§3.6) and Chapter 4 (§4.2) as the expanded evaluation suite alongside `MiniLM`, `DeBERTa-v3-base`, and `ModernBERT-base`.
2. **Prioritize `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli`:** This model is hypothesized to achieve the highest empirical score among base models because its pretraining already resolved adversarial negation.
3. **Compare `ModernBERT-base` vs `ModernBERT-large`:** Provides a clean, publication-grade ablation demonstrating the exact effect of parameter scaling under 8,192-token context windows.
4. **Benchmark `PoL-BERT-Large` vs `LEGAL-BERT`:** Directly answers whether administrative/regulatory pretraining (Pile of Law) outperforms judicial/case-law pretraining (European/UK law).
5. **Retain `FacebookAI/roberta-large-mnli` as the Formal Baseline:** Confirms alignment with COLIEE Task 4 literature (Rabelo et al., 2022).
