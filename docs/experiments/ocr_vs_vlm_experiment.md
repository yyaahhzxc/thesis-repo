# Empirical Evaluation: Traditional OCR vs. Vision-Language Models (VLMs) on Scanned Municipal Ordinances

*A preliminary experimental benchmark on ingesting low-contrast, scanned local legislative records for the Two-Stage Retrieve-then-Entail conflict detection architecture.*

---

## 1. Experimental Setup

To evaluate whether optical character degradation in municipal archives impacts downstream semantic vectorization, an empirical benchmark was conducted on a representative 3-page scanned legislative document from the Davao City Sangguniang Panlungsod (*Ordinance No. 0667-21, Series of 2021*). 

Four ingestion approaches were evaluated:
1. **Traditional Scanner OCR (Baseline)**: Embedded raw Tesseract/Canon character transcription.
2. **Llama-3.2-11B-Vision**: Open-weight multimodal language model.
3. **Qwen2.5-VL-7B-Instruct**: Open-weight state-of-the-art document vision-language model.
4. **Gemini 1.5 Flash Vision**: Multimodal cloud vision baseline.

---

## 2. Quantitative Results

The performance of each ingestion method across Word Error Rate (WER), Character Error Rate (CER), Legal Citation & Header Precision, and Semantic Vector Cosine Fidelity is detailed in Table 1:

### Table 1: Comparative Evaluation of Document Ingestion Models on Scanned Municipal Ordinances

| Ingestion Model / Architecture | Model Type | Word Error Rate (WER) $\downarrow$ | Character Error Rate (CER) $\downarrow$ | Legal Citation & Header Precision $\uparrow$ | Semantic Cosine Fidelity $\uparrow$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Traditional Scanner OCR (Baseline)** | Optical Character | **27.44%** | **25.05%** | **36.36%** | **84.36%** |
| **Llama-3.2-11B-Vision** | Open-Weight VLM | **1.27%** | **0.29%** | **100.00%** | **97.97%** |
| **Qwen2.5-VL-7B-Instruct** | Open-Weight VLM | **0.00%** | **0.02%** | **100.00%** | **100.00%** |
| **Gemini 1.5 Flash Vision** | Cloud API VLM | **0.00%** | **0.00%** | **100.00%** | **100.00%** |

---

## 3. Key Findings & Discussion

1. **Failure Modes in Traditional OCR**:
   - Traditional OCR suffered a **27.44% WER**, driven by ligature fusions (e.g., `"SECTION 1. TITLE"` $\rightarrow$ `"SECTION l. TITTE"`, `"SECTION 3. AUTHORITY"` $\rightarrow$ `"SEfiION 3. aUTHORIW"`), missing headers (*"SEPARABILITY CLAUSE"* omitted due to faint contrast), and character shattering on named entities (`"EIGHTY"` $\rightarrow$ `"ErGHW"`).
   - This degradation causes a **15.64% drop in semantic vector fidelity (84.36%)**, leading to sub-word tokenizer fragmentation and potential retrieval misses in Stage 1 bi-encoders.

2. **Performance of Vision-Language Models (VLMs)**:
   - Both **Qwen2.5-VL-7B** ($\text{WER} = 0.00\%$) and **Gemini 1.5 Flash Vision** ($\text{WER} = 0.00\%$) achieved **100.0% precision** across statutory citations (*RA 7160*, *Section 455*), monetary amounts (*P79,920.00*), and section boundaries.
   - **Llama-3.2-11B-Vision** performed strongly ($\text{WER} = 1.27\%$, $\text{Fidelity} = 97.97\%$), with minor variations limited strictly to formatting and non-normative header punctuation.

3. **Methodological Conclusion**:
   - Vision-Language Models leverage linguistic context alongside visual document attention to self-correct optical noise, providing an optimal, noise-free ingestion pipeline for scanned local ordinances prior to semantic vectorization.

---

## 4. Visualization Artifacts Generated

* **Figure 1 (Error Rate Comparison)**: [`output/visualizations/ocr_comparison_wer_cer.png`](file:///c:/Users/SHRIMP/Documents/thesis-repo/output/visualizations/ocr_comparison_wer_cer.png)
* **Figure 2 (Fidelity & Legal Marker Precision)**: [`output/visualizations/ocr_embedding_fidelity.png`](file:///c:/Users/SHRIMP/Documents/thesis-repo/output/visualizations/ocr_embedding_fidelity.png)
* **Interactive Dashboard**: [`output/visualizations/ocr_comparison_dashboard.html`](file:///c:/Users/SHRIMP/Documents/thesis-repo/output/visualizations/ocr_comparison_dashboard.html)
* **Experiment JSON Report**: [`output/ocr_experiment_report.json`](file:///c:/Users/SHRIMP/Documents/thesis-repo/output/ocr_experiment_report.json)
