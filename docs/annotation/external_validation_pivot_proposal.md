# External Legal Validation & Usability Evaluation Pivot Proposal


## 1. Background & Empirical Trigger

Our original Chapter 3 plan targeted 15 Davao City Sangguniang Panlungsod (SP) legal researchers across five 70-pair panels (`W = 350 x 3 = 1,050` annotations) plus a 14-item SUS/TAM usability survey. Following HRMO/City Administrator routing delays, only **2 SP responses** were returned on the 350-pair Google Form:

| Respondent | Assigned Panel | Items | Confidence Variance | Agreement vs. Gold | Cohen's Kappa | QC Verdict |
| :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| `SP-ANN-13` | Panel E (`GT-281`–`350`) | 70 | **Zero** (`2.0` on all 70/70) | 28.6% (55/70 Neutral) | `-0.0234` | **Exclude** (objective straightlining outlier) |
| `SP-ANN-10` | Panel D (`GT-211`–`280`) | 70 | Full scale (`1`: 23, `2`: 31, `3`: 16) | 68.6% (48/70) | `+0.5092` | **Valid**, engaged response (non-lawyer staffer; `5/18` Contradiction recall) |

At the same time, auditing the existing `ground_truth_350.jsonl` highlighted two practical weaknesses for human evaluation:
1. **Length fatigue:** Median `96` words (premise) + `76` words (hypothesis) = **~172 words per pair**, making 70+ pairs heavy for busy evaluators.
2. **AI-sounding hypotheses:** Several synthetic draft clauses carry formulaic preambles (e.g., *"Pursuant to Section 16 of Republic Act No. 7160 and in the exercise of executive administrative authority..."*), contributing to the `58.00%` hypothesis-only baseline.

**Precedent from Peer Study:** Corpuz, Lamsin, & Nuril successfully recruited **4 legal-expert reviewers** (including 2 Bar-licensed attorneys, Atty. Lina Matilac and Atty. Rommel Jay Ugay) on a voluntary basis using snacks as tokens of appreciation rather than monetary fees.

---

## 2. Recommended Plan: Option C — External Bar-Validated Challenge Test Set + Targeted SP Usability Follow-Up

### Core Design (Single-Visit Protocol for 3 Licensed Lawyers)

Instead of discarding our panel-approved training/validation splits and re-running every post-defense experiment (Stage 1, 28 zero-shot + 13 fine-tuned models, Tier 2 drafts, and the 2.5-hour Tier 3 Revenue Code sweep), we **keep all defended results 100% intact** as our *Internal Development Benchmark* (`245 / 52 / 53`) and add a **brand-new, unseen, Bar-validated External Test Set**:

1. **Curate `N = 72` or `80` Crisp, Non-AI-Sounding Pairs:**
   - **Coverage:** `9–10` pairs per domain across **all 8 macro-domains**, balanced across **all 3 difficulty tiers** (Surface/Quantitative, Preemption/Carve-Outs, Latent/Paraphrastic) and **all 3 NLI classes** (`Contradiction`, `Entailment`, `Neutral`).
   - **Text Hygiene:** Select naturally concise, **100% verbatim** Lawphil national statutory premises; write short (`~30–50` words), authentic Davao City ordinance hypotheses modeled directly on `cleaned_transcriptions/` with zero templated AI lead-ins.
   - **Pre-Lock Sanity Check (Zero Extra Lawyer Visits):** Have Sir Ogs skim a sample of the *ordinance-only* sections (national statutes hidden) before locking the Google Form so the 3 lawyers stay 100% blind on first read.

2. **Recruit 3 Independent Licensed Philippine Lawyers (`k = 3`, snacks as tokens, ONE single visit):**
   - **Part A — Blind NLI + Legislative Realism Form (~1–1.5 hours):** Each pair requires only **3 quick clicks**:
     1. *Legal Consistency Decision:* `Contradiction` / `Entailment` / `Neutral`
     2. *Confidence Rating:* `1–3`
     3. *Legislative Realism Check:* `1–3` (or `1–5`) rating on whether the draft ordinance section reads like an authentic Sangguniang Panlungsod provision (establishing formal **face validity** without requiring a second visit).
   - **Part B — Live Prototype Demo + 14-Item SUS/TAM Usability Survey (~10 minutes, same visit):** Immediately after the form, each lawyer tests 1–2 real Davao City ordinances on the finished prototype and completes the existing 14-item SUS/TAM usability survey.

3. **Run Inference Only on Existing Saved Models (Zero Retraining):**
   - Compute **3-lawyer Fleiss' Kappa** (inter-rater reliability), **Mean Realism Score**, and a **Hypothesis-Only baseline check** (verifying that rewriting the hypotheses eliminated lexical shortcuts).
   - Take our **already-saved frozen model checkpoints** (fine-tuned DeBERTa-v3 with `tau* = 0.45`, Legal-BERT, and Zero-Shot baseline) and run `.predict()` on the `72–80` lawyer-consensus pairs.
   - Add a dedicated **External Bar-Validated Generalization & IRR** subsection to Chapter 4 alongside our internal `N = 53` test results, and update Chapter 3 (§3.7) and Chapter 5 (§5.2.1).

---

## 3. Honest Assessment of the Key Trade-Off: Practicing Lawyers vs. SP Personnel

| Dimension | Practicing Lawyers (`n = 3`) | Sangguniang Panlungsod Staff | Assessment |
| :--- | :--- | :--- | :--- |
| **Ground Truth NLI & Realism Validation** | **Stronger** — Bar-licensed lawyers have higher doctrinal authority on *Magtajas* preemption and RA 7160 statutory conflict. | Mixed — `SP-ANN-10` (non-lawyer staffer) had `5/18` recall on Contradiction. | **No flaw here:** external lawyers actually *strengthen* ground truth credibility. |
| **End-User Usability Survey (SUS/TAM)** | **Weaker ecological validity** — lawyers can judge legal research utility and XAI clarity, but they are **not** daily SP First Reading committee users. | **True target end-users** — directly evaluate real legislative committee workflow fit (`TAM-04`). | **Real limitation:** Lawyer-only SUS/TAM must be framed strictly as a **Domain-Expert Pilot Evaluation**, not an institutional SP deployment study. |

### Mitigation: Separate, Low-Friction SP Usability Follow-Up
To address the role-fit gap directly, we **will still revisit / follow up with the Davao City Sangguniang Panlungsod office specifically for the usability survey**, decoupled from the exhausting 70-pair ground-truth form:
- **Why this has much higher odds of engagement:** Asking busy SP staff to answer 70 dense legal pairs feels like a 1.5-hour exam; asking them to spend **10 minutes trying a live Davao City ordinance-checking tool + answering a 14-item Likert survey** is fast, practical, and directly relevant to their daily work.
- **Target outcome:** Even if only **2–5 SP staffers** (starting with `SP-ANN-10` and colleagues) complete the demo + SUS/TAM form, combining them with the **3 lawyers** yields **`n = 5–8` total evaluators** spanning *both* Bar-licensed legal experts and actual SP legislative staff—hitting Nielsen's classic 5–8 user usability benchmark while transparently reporting subgroup scores (Lawyers vs. SP Staff).

---

## 4. Alternatives Compared (For Adviser Discussion)

| Option | Summary | Lawyer Load | Re-run Cost | Trade-Off |
| :--- | :--- | :--- | :--- | :--- |
| **Option A (Fast Fallback)** | Keep existing Set D (`70` pairs, 2/8 domains); recruit 2 lawyers to pair with `SP-ANN-10`. | Low (`70` pairs, 2 lawyers) | Zero | Only covers 2/8 domains; retains AI-sounding hypotheses. |
| **Option B (Full Revamp)** | Replace the 350-pair benchmark entirely (`150–180` pairs), have 3 lawyers label all, and retrain/re-run everything. | Heavy (`150–180` pairs, 3–4 hrs) | Full (Stage 1, Stage 2, Tier 2, Tier 3 + RevCode + App. Q) | High dropout risk and invalidates all panel-approved post-defense tables. |
| **Option C (Recommended)** | Keep defended results intact; create `72–80` crisp, non-AI pairs across all 8 domains & 3 tiers for 3 lawyers (single visit: NLI + Realism + pilot SUS/TAM) + separate low-friction SP usability follow-up. | Low & safe (`72–80` short pairs, ~1–1.5 hrs, 3 lawyers) | Minimal (inference only on frozen checkpoints) | Strongest generalization proof, closes `kappa` + face validity + pilot SUS/TAM with zero risk to defended results. |

---

## 5. Decisions Needed from Ralph & Sir Ogs

1. **Approval of Option C** (vs. Option A fallback) and confirmation that keeping defended internal benchmark tables intact alongside the new External Bar-Validated Test Set satisfies post-defense Minor Revisions.
2. **External Test Set Parameters:** Confirm `N = 72` (`9` pairs × 8 domains) vs. `N = 80` (`10` pairs × 8 domains) and Realism rating scale (`1–3` vs. `1–5`).
3. **Lawyer Recruitment:** Follow up with Nazz for attorney contact details and confirm availability of **3 licensed lawyers** (snacks as tokens, single visit).
4. **SP Usability Revisit:** Confirm wording/timing of a short, low-friction follow-up to the SP office pitching *only* the 10-minute live demo + 14-item SUS/TAM usability survey.
