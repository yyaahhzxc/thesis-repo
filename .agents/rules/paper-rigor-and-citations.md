---
trigger: model_decision
description: Apply alongside ALL other paper-*.md rules when verifying citations, BibTeX entries, numerical claims, legal doctrines, statistical tests, or running forensic audits on CS_Undergraduate_Thesis_Template/. Covers DOI/PDF verification, zero editorial pollution, statistical rigor, and domain scope boundaries.
---

# **Paper Scientific Rigor, Citations & Forensic Audit Standards**

**Scope:** Citation verification, legal-text integrity, statistical rigor, and adversarial auditing for `CS_Undergraduate_Thesis_Template/`. Enforce alongside all four `paper-*.md` rules during drafting and manuscript sweeps.

---

## **1. Web-Verified Sourcing, Local PDF Verification & `references.bib`**

1. **Web & Academic Database Verification:** Verify every cited paper against actual indexed metadata (ACM, IEEE, ScienceDirect, Springer, ACL Anthology, Lawphil, or verified arXiv):
   * Registered DOI & direct URL, exact published year, complete author spelling, and official journal/conference venue.
2. **Strict Local PDF Verification (Zero Phantom Attribution):** Every factual assertion, formula, baseline, or numerical threshold attributed to `\cite{...}` must be verified directly against the authentic source text and its local PDF in `docs/references/`.
   * **NEVER** invent or misattribute numerical target thresholds (e.g., *"target of 80%–85%"*), prescriptive quality ceilings, or partition rules unless the cited publication literally states that exact figure or rule.
   * Where no literature source prescribes a numerical target, use formal mathematical/empirical baselines (e.g., Morrison proportional chance criterion, unclustered silhouette <= 0.0000, DBI > 4.0000) and report the exact margin over baseline.
3. **No Citation Laundering & Zero Hallucination:** Verify the cited work directly tests or concludes the exact claim made. If a claim cannot be matched to a verifiable DOI or authenticated publication, **omit the claim completely**.
4. **Continuous Grounding Sweeps:** Ensure every empirical threshold, sample allocation ($N = 350$, $70/15/15$ split), hyperparameter, and legal rule is backed by literature (e.g., SQuAD, FEVER, ANLI, Cohen, Card et al. MDE, Ablazo 2019), jurisprudence (*Magtajas*, RA 7160, EO 292), or hardware limits.
5. **BibTeX Standards (`references.bib`):**
   * Include all relevant fields (`author`, `title`, `journal`/`booktitle`, `year`, `volume`, `number`, `pages`, `publisher`, `doi`, `url`).
   * Protect acronyms/proper nouns with braces (`{P}hilippine`, `{BERT}`, `{NLI}`, `{COLIEE}`, `{BM25}`, `{Davao City}`).
   * Use clean lowercase keys: `surnameYearKeyword` (e.g., `ablazo2019designing`, `wu2025aiir`).
   * In prose, tie citations with non-breaking spaces (`~`): `algorithm~\cite{wu2025aiir}`, `Doctrine~\cite{scp1994magtajasvpryce}`. Use `\cite{key}` for parenthetical and `\citeauthor{key}~\cite{key}` for narrative citations.

---

## **2. Zero Editorial Pollution & Statutory Completeness**

1. **100% Verbatim Legal Text Integrity:** Statutory provisions, ordinance sections, benchmark premises, and UI/manuscript example boxes MUST contain **100% verbatim authentic text** directly from Lawphil or Sangguniang Panlungsod archives (`data/unified_dual_statutory_provisions.jsonl`).
   * **NEVER** rewrite, paraphrase, or inject explanatory commentary/doctrine warnings into statutory text strings (`statutory_text`, `statute_text`, `ordinance_text`, `premise`).
   * Keep all legal rationales, preemption doctrines, and *ratios decidendi* strictly in dedicated explanation prose or metadata fields (`legal_rationale`, `verdict_desc`, `ratio_decidendi`).
2. **Full-Text Completeness:** System-level evaluations and full-PDF benchmarks ingest complete enactments top-to-bottom (session metadata, attendance, `WHEREAS` recitals, enacting clause, operative sections, framework clauses, signature blocks), never synthetic 1-page stubs.

---

## **3. Autonomous Adversarial Forensic Audit Loop**

During drafting and manuscript sweeps, proactively run peer-review forensic checks:

1. **Contingency Table & McNemar Arithmetic:** Verify every $2 \times 2$ table satisfies marginal identities (`(a + b) - (a + c) = b - c`) and that McNemar $\chi^2$, Edwards' continuity corrections, and $p$-values match their exact denominators ($N = 53$ held-out test split, $N = 198$ unique instances, or $N = 350$ multi-panel pairs).
2. **Omnibus vs. Pairwise Statistical Harmony:** Always clarify the relationship between discrete pairwise McNemar tests on the 53-item split and omnibus domain-wide rankings (Friedman ANOVA $\chi_F^2 = 40.0000, p < 0.001$ across all 8 macro domains; paired Wilcoxon signed-rank $W = 0.0, p = 0.0078$).
3. **Bayesian Low-Prevalence PPV Framing:** Frame screening performance under realistic base rates ($p \le 0.01$), distinguishing open-corpus PPV (`2.12%`), controlled benchmark (`6.57%`), and high-specificity operation (`32.58%`).
4. **Conflict Count Disambiguation:** Always separate **Actual Substantive Legal Conflicts** (ground-truth preemption under *Magtajas*, statutory fine caps, or explicit statutory permission vs. prohibition) from **System-Found Conflicts / Alarms** (raw candidate pairs crossing $\tau^*$—including true preemption, stricter police-power friction, and false positives such as historical charter leakage).
5. **Tone Calibration:** Report operational limitations and false-positive inspection burdens transparently without undercutting verified empirical gains.

---

## **4. Canonical Domain & Technical Boundaries**

Ensure every chapter aligns with these fixed factual boundaries:
* **Legal Framework:** *Magtajas v. Pryce* (G.R. No. 111097, 1994), RA 7160 (Local Government Code of 1991, including §458(a)(1)(iii) P5,000 fine cap), RA 11032 (Ease of Doing Business). Strictly **ex-ante** pre-enactment screening (vertical preemption + horizontal coherence), not ex-post judicial adjudication.
* **Two-Stage Architecture:** Fixed paradigm (Stage 1 coarse IR over dual corpus $\rightarrow$ Stage 2 fine NLI + white-box intrinsic Layer-12 cross-attention XAI); specific model backbones are framed as competing experimental candidates evaluated via ablation. **NO generative LLM authorship** of legal text; **NO cross-statute multi-hop $N$-vs-$N$ reasoning**; **asymmetric span-level pairing** ($N$-sentence draft clause vs. 1 statutory provision) on **consumer-grade local CPU/GPU hardware**.
* **Canonical Corpus & Annotation Parameters:** `25,432` national statutes + `1,816` deduplicated Davao City ordinances = **`27,248` unique enactments** and **`177,423` unique provisions** (note: live demo index `src/demo/app.py` operates on the `176,421`-provision serialized index where specified). Ground truth = `350` curated pairs (`70/15/15` split: `245` train / `52` val / `53` test; `198` unique instances in premise-grouped 5-fold CV) annotated by 15 SP legal researchers in 5 sub-panels of 3 (`70` pairs each, Fleiss' $\kappa$, SNLI ceiling `~0.70` per Bowman et al.).
