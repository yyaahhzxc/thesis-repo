---
trigger: model_decision
description: Apply alongside ALL other paper-*.md rules when writing or auditing LaTeX syntax, tables, figures, equations, algorithms, or visual-prose bridging in CS_Undergraduate_Thesis_Template/. Covers TeX Live 2026 formatting, margin/hbox hygiene, booktabs tables, Setup-Visual-Exposition bridging, and equation/algorithm grounding.
---

# **Paper LaTeX Engineering, Tables & Visual Exposition Standards**

**Scope:** LaTeX formatting, tables, equations, algorithms, and visual-prose integration for `CS_Undergraduate_Thesis_Template/` (compiled under **TeX Live 2026** via `pdflatex` + `bibtex`). Enforce alongside all four `paper-*.md` rules during drafting and sweeps.

---

## **1. Typographical Hygiene & Margin Discipline**

1. **Strict Margin & Overfull `\hbox` Prevention:** No paragraph, formula, or table cell may protrude past page margins.
   * Write model identifiers in standard roman text in body prose (`DeBERTa-v3-base-NLI`, `ModernBERT-base`, `PoL-BERT-Large`) so LaTeX hyphenates naturally at hyphens. Reserve `\texttt{...}` for table cells, code blocks, or literal filenames.
2. **Strict LaTeX Quotation Marks:** Never use straight typewriter quotes (`"word"`). Use `` ``double quotes'' `` and `` `single quotes' ``.
3. **Non-Breaking Reference Ties (`~`):** Always bind labels and citations with `~`: `Figure~\ref{fig:...}`, `Table~\ref{tab:...}`, `Section~\ref{sec:...}`, `Appendix~\ref{app:...}`, `Equation~\eqref{eq:...}`.
4. **Lists & Structural Elements:** For formal research questions/objectives, use `itemize` with semicolon-separated items ending in a period. Use `description` lists sparingly and never as artificial inline headings for body prose.
5. **Standardized Editorial Search Flags:** Use `[TODO: ...]`, `[CITE: ...]`, and `[DATA: ...]` when marking unresolved items so they remain globally searchable.

---

## **2. Compact, Value-Only Publication Tables**

1. **`booktabs` Rules Only:** Use `\toprule`, `\midrule`, and `\bottomrule`. **NEVER** use vertical lines (`|`). Place `\caption[Short]{Full}` **above** the table with a unique `\label{tab:...}`.
2. **Value-Only Cells (No Prose or Footnote Notes):** Table cells must contain only numerical metrics, identifiers, and concise outcome tags (`Caught (TP)`, `Cleared (TN)`, `Missed (FN)`)—never multi-sentence prose or legal commentary.
   * **NEVER include `\textit{Note:}` blocks underneath tables.** Put all sample sizes, hardware context, abbreviations, and interpretation in the surrounding body text.
3. **Unbiased Model Naming:** **NEVER** tag candidate models with `(Proposed)` or `Proposed`, and strip descriptive nicknames (e.g., omit `(WANLI Scaled Reasoning Ceiling)` or `(Distilled Edge)`). Retain suffixes only when identifying genuine architecture versions or parameter sizes.
4. **Full-Width Expansion & Column Proportions:**
   * Reserve **35%–45%** of table width for substantive text/description columns using `>{\RaggedRight\arraybackslash}X` (in `tabularx` or `xltabular` for multi-page appendix tables).
   * Keep numeric/metric columns compact (`p{1.4cm}`–`1.9cm`, `c`, or `r`) and label columns tight to their longest label (`p{3.2cm}`–`3.6cm`).
   * Use `\renewcommand{\arraystretch}{0.88}` to `0.95`, `\footnotesize` or `\scriptsize`, and `\setlength{\tabcolsep}{2.5pt}` to `4.0pt`; use `pdflscape` (`\begin{landscape}`) when wide multi-column tables would otherwise overflow portrait margins.

---

## **3. Proximity & "Setup $\rightarrow$ Visual $\rightarrow$ Dedicated Exposition" Pattern**

1. **Proximity & Anti-Stacking:** Place every figure, table, equation, and listing immediately following the paragraph where it is first cited. **Avoid back-to-back float walls** (multiple visuals stacked without intervening analytical prose).
2. **Brief Descriptive Captions:** Captions state strictly *what* the visual depicts (subject, source, scope, sample size $N$). **NEVER** pack analytical conclusions or takeaway arguments into captions.
3. **The 3-Step Pattern (Chapters 1–5):**
   * **Setup:** Preceding paragraph introduces the visual and cites it explicitly (`Table~\ref{...}` / `Figure~\ref{...}`).
   * **Visual:** Clean floating environment (`figure`, `table`, `algorithm`).
   * **Dedicated Exposition (4–6 Sentences):** Immediately below the visual, explain: (i) *what it contains* (columns, rows, axes, modules), (ii) *why those metrics/columns are there*, (iii) *what is happening* (trends, trade-offs, outliers), and (iv) *what it means* (substantive conclusion or baseline margin). *(Note: Appendices display artifacts + brief factual captions only, without exposition paragraphs.)*

---

## **4. Equations & Code-Grounded Algorithms**

1. **Implemented Algorithms Only:** Only present algorithms, pseudocode listings, and workflows that are actually implemented and executed in `src/` or `scripts/`. Never include speculative or unimplemented textbook algorithms.
2. **Equation-Algorithm Non-Redundancy:** Do not duplicate display equations that are already embedded inside an algorithm listing.
3. **Equation Formatting & List of Equations:**
   * Use `amsmath` (`equation`, `align*`, `aligned`) and math mode for variables (`$N$`, `$k$`, `$\kappa$`).
   * Title and caption every formal display equation with `\eqcaption{<Title>}` inside `equation` to populate `\listofequations`. Do not bold equation titles inside `description` items.
   * Suppress post-equation indentation using `\noindent Where ...` with no blank line between `\end{equation}` and `Where ...`, and insert a blank line after `\end{description}` to restore normal 0.5-inch indentation for the following paragraph:

```latex
\begin{description}
    \item[Fleiss' Generalized Multi-Rater Kappa Reliability Metric ($\kappa$)] \leavevmode
    \begin{equation}
        \kappa = \frac{\bar{P} - \bar{P}_e}{1 - \bar{P}_e}
        \label{eq:fleiss_kappa}
        \eqcaption{Fleiss' Generalized Multi-Rater Kappa Reliability Metric ($\kappa$)}
    \end{equation}
    \noindent Where $\bar{P}$ is the mean observed agreement across pairs, and $\bar{P}_e$ is the chance-expected agreement.
\end{description}

The resulting inter-rater reliability score evaluates consistency...
```
