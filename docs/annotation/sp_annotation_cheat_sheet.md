# Sangguniang Panlungsod Legal Annotation Quick Reference Guide
**Ex-Ante Municipal Ordinance Consistency Auditing System**  
*Ateneo de Davao University — Department of Computer Science, in collaboration with the Sangguniang Panlungsod of Davao City*

---

### Core Objective
As a legal researcher or legislative officer, your task is to evaluate whether a proposed **Municipal Ordinance Draft Clause (Hypothesis)** logically and legally aligns with an existing **Philippine National Statute (Premise)**.

> [!IMPORTANT]
> **Evaluation Scope (Strictly Pairwise / Single Premise)**:
> Evaluate **only** the single national statute clause provided in the row. Do **not** attempt multi-statute synthesis (i.e., do not combine multiple unlisted laws in your head). Ask yourself: *Based strictly on this specific national provision, does the local ordinance draft contradict, entail, or remain neutral?*

---

### The Three Logical States

| Decision | Legal Standard (*Magtajas Doctrine*) | Key Syntactic & Jurisprudential Triggers | Example |
| :--- | :--- | :--- | :--- |
| **Contradiction** | The draft ordinance **prohibits what statute permits**, **permits what statute prohibits**, or **exceeds delegated statutory ceilings** (RA 7160 Sec. 458). | • Penalty exceeds ₱5,000 fine or 1-year imprisonment.<br>• Usurps exclusive national regulatory jurisdiction (LTO, NTC, ERC, DOH, PNP).<br>• Erases national statutory exemptions (senior citizens, emergency responders, minors).<br>• Mandatory obligation (*shall*) converted to local discretionary act (*may*). | **Statute**: Caps city penalties at ₱5,000.<br>**Ordinance**: Imposes ₱15,000 fine or 2 years imprisonment for dumping. |
| **Entailment** | The draft ordinance **directly executes, implements, or complies with** the national statute within delegated powers without conflict. | • Adopts prescribed statutory quotas (e.g., 20% development fund, 5% calamity fund).<br>• Enforces devolved local regulatory powers adhering to national guidelines.<br>• Compliant administrative procedures (e.g., e-BOSS, designated non-smoking areas). | **Statute**: Mandates 20% local development fund.<br>**Ordinance**: Appropriates 21% of NTA to public drainage and health clinics. |
| **Neutral** | Both texts share the same broad legal category, but **govern independent legal obligations** with no mutual conflict or direct derivation. | • Topical co-occurrence without deontic clash.<br>• Regulates distinct administrative subject matter (e.g., streetlamps vs. driver licensing).<br>• Neither authorizes nor restricts the specific activity governed by the statute. | **Statute**: National highway speed limits.<br>**Ordinance**: Solar street lighting maintenance along city avenues. |

---

### The Three Difficulty Tiers

* **Tier 1: Surface & Quantitative (30%)**
  * *How to spot*: Look for direct numeric ceiling violations (fines > ₱5,000, imprisonment > 1 year, processing deadlines, percentage caps) or direct modal polarity flips (*shall* vs *may*).
* **Tier 2: Preemption & Carve-Outs (40%)**
  * *How to spot*: Look for jurisdictional encroachment on national agencies (LTO, LTFRB, NTC, ERC, DOH) or blanket local prohibitions that fail to respect statutory exemptions (e.g., emergency medical transport, student discounts on holidays, non-custodial youth diversion).
* **Tier 3: Latent & Paraphrastic (30%)**
  * *How to spot*: The ordinance draft uses different wording, administrative euphemisms, or avoids citing the national law, but creates an irreconcilable conflict in practice (e.g., reclassifying youth status offenders into locked holding rooms overnight under a "peacekeeping" label).

---

### Step-by-Step Evaluation Workflow in Google Sheets

1. **Read Column F (`National_Statute_Premise_Text`)**: Identify the exact legal command, ceiling, or exemption.
2. **Read Column H (`Municipal_Ordinance_Hypothesis_Text`)**: Identify the proposed local rule, obligation, or penalty.
3. **Select Decision in Column I**: Choose **Contradiction**, **Entailment**, or **Neutral** from the dropdown menu.
4. **Select Confidence Score in Column J**: `1` (Low / Edge Case), `2` (Moderate Confidence), `3` (High / Clear-Cut).
5. **Add Notes in Column K (Optional but Helpful)**: Briefly note the legal basis (e.g., *"Exceeds ₱5k penalty ceiling under RA 7160 Sec. 458"*).

---

### Consensus and Adjudication Protocol
* Each block is evaluated independently by three researchers in your panel.
* A label is accepted into the final benchmark if **at least 2 out of 3 evaluators agree**.
* Three-way split disagreements (1 Contradiction, 1 Entailment, 1 Neutral) are escalated to the **Senior Legal Researcher** for final binding adjudication.

*Thank you for contributing your legal expertise to modernizing municipal legislative review in Davao City!*
