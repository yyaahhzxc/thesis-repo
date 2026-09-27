# **End-User System Usability, Practical Utility & Technology Acceptance Survey Specification**

**Institution:** Ateneo de Davao University, Department of Computer Science  
**Project:** *A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference*  
**Authors:** Ralph Paolo Dulce & Yahyah Odin  
**Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao  
**Target Respondents:** 15 Legal Researchers, Sangguniang Panlungsod of Davao City  
**Document Status:** Complete Specification for Google Forms Deployment & Thesis Integration  

---

## **1. Background, Motivation & Panel Caucus Grounding**

During the Thesis 1 defense caucus, the evaluation panel highlighted an essential distinction in evaluating applied legal artificial intelligence systems:
* **Algorithmic Evaluation (Offline Metrics):** Measures technical retrieval and inference accuracy (Recall@$k$, Mean Reciprocal Rank, Macro $F_1$, McNemar $\chi^2$) against historical ground-truth pairs.
* **End-User Usability & Practical Utility Evaluation (Human-in-the-Loop):** Measures whether qualified institutional stakeholders—specifically, the legal researchers of the Davao City Sangguniang Panlungsod—find the software **genuinely useful, understandable, and viable for adoption** in their daily legislative review workflow.

This specification provides the complete questionnaire design, psychometric grounding, and deployment plan for the post-interaction end-user survey.

### **Theoretical & Psychometric Foundations**
1. **Technology Acceptance Model (TAM; Davis, 1989):** Measures *Perceived Usefulness (PU)* and *Perceived Ease of Use (PEOU)* to evaluate institutional adoption willingness.
2. **Task-Technology Fit (TTF; Goodhue & Thompson, 1995):** Measures how well the two-stage coarse-to-fine pipeline aligns with the statutory audit tasks mandated during the First Reading referral window under RA 7160 §54.
3. **System Usability Scale (SUS; Brooke, 1996):** Provides a standardized, 10-item industry benchmark yielding a normalized 0–100 score for comparative software usability.
4. **Human-Centered Explainable AI (XAI; Doshi-Velez & Kim, 2017; Rudin, 2019):** Evaluates diagnostic transparency (verbatim statutory context, highlighted conflicting deontic markers, and alert tier separation) while assessing tolerance to alert fatigue.

---

## **2. Administration Protocol & Participant Journey**

1. **Target Population:** The 15 Sangguniang Panlungsod legal researchers participating in the study.
2. **Timing of Administration:** Administered immediately following a structured 30–45 minute interactive user testing session with the working prototype dashboard.
3. **Testing Scenario:** Each researcher tests the prototype using realistic sample draft ordinances, observing both:
   * Vertical Preemption Alerts against superior national statutes (RA 7160, national penal and regulatory codes).
   * Horizontal Coherence Notices against existing Davao City local ordinances.
   * Highlighted conflicting tokens and side-by-side legal text comparisons.
4. **Estimated Completion Time:** 8 to 10 minutes.
5. **Platform:** Google Forms (administered digitally, mobile- and desktop-friendly, with anonymous token tracking to preserve confidentiality while enabling multi-rater correlation analysis).

---

## **3. Questionnaire Instrument Specification (Google Forms Blueprint)**

### **Header & Informed Consent (Data Privacy Act of 2012 / RA 10173)**

```text
FORM TITLE:
Sangguniang Panlungsod Legal Researchers End-User System Evaluation Survey

FORM DESCRIPTION:
Dear Legal Researcher,

Thank you for participating in the interactive demonstration of our prototype conflict detection system. 

This survey evaluates the overall practical usefulness, ease of use, diagnostic transparency, and institutional workflow fit of the system as an assistive screening tool for draft Davao City ordinances. Your expert feedback will directly inform the final design of the system and our undergraduate thesis at the Department of Computer Science, Ateneo de Davao University.

PRIVACY & ETHICAL DISCLOSURE:
In compliance with Republic Act No. 10173 (Data Privacy Act of 2012), all responses gathered through this form will remain strictly confidential and will be analyzed in aggregate form. No personally identifiable information will be published. Participation is voluntary, and you may decline to answer any question.

By proceeding to the next section, you confirm that you have read this disclosure and consent to the use of your anonymized responses for academic research purposes.
```

---

### **Section 1: Respondent Demographic & Experience Profile**

*Objective: Establish the professional qualification baseline of the evaluator cohort.*

* **D1. Assigned Participant ID / Panel Token:**  
  *Short answer text* (e.g., `SP-R01` to `SP-R15`)

* **D2. Highest Educational Attainment in Law / Public Administration:**  
  *(Multiple Choice)*
  - [ ] Bachelor of Laws (LL.B.) / Juris Doctor (J.D.)
  - [ ] Master of Laws (LL.M.) / Master in Public Administration (MPA)
  - [ ] Pre-Law Degree (e.g., Legal Management, Political Science, Philosophy)
  - [ ] Member of the Philippine Bar (Admitted)
  - [ ] Other: [Write-in]

* **D3. Years of Experience in Legal Research, Statutory Review, or Legislative Drafting:**  
  *(Multiple Choice)*
  - [ ] Less than 1 year
  - [ ] 1 to 3 years
  - [ ] 4 to 6 years
  - [ ] 7 to 10 years
  - [ ] More than 10 years

* **D4. Primary Sangguniang Panlungsod Committee Assignment(s):**  
  *(Checkboxes - Select all that apply)*
  - [ ] Committee on Laws, Rules and Privileges
  - [ ] Committee on Finance, Budget and Appropriations
  - [ ] Committee on Public Safety and Security
  - [ ] Committee on Transportation and Communications
  - [ ] Committee on Health and Social Services
  - [ ] Sangguniang Panlungsod Secretariat / Research Division
  - [ ] Other: [Write-in]

* **D5. Estimated Average Hours Spent Per Week Conducting Manual Legal Searches (Lawphil, Supreme Court E-Library, Archival Local Ordinances):**  
  *(Multiple Choice)*
  - [ ] Less than 3 hours per week
  - [ ] 3 to 6 hours per week
  - [ ] 7 to 10 hours per week
  - [ ] More than 10 hours per week

---

### **Section 2: Perceived Usefulness (PU) & Task-Technology Fit (TTF)**

*Instructions: Please rate your level of agreement with each statement based on your experience using the conflict detection dashboard.*  
*Scale: 1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree*

* **PU1 (Search Burden Reduction):**  
  "The system significantly reduces the time and effort required to find relevant national statutes and fellow city ordinances compared to manual searching."  
  *(Linear scale: 1 to 5)*

* **PU2 (Preemption Risk Detection):**  
  "The system effectively surfaces subtle legal contradictions and preemption risks (e.g., unauthorized penalties, conflicting regulatory mandates) that might be overlooked during initial reading."  
  *(Linear scale: 1 to 5)*

* **PU3 (Drafting Confidence):**  
  "Screening a draft ordinance through the system gives me greater confidence that the proposed text complies with national statutes prior to committee filing."  
  *(Linear scale: 1 to 5)*

* **PU4 (Workflow Expediency):**  
  "If integrated into the Sangguniang Panlungsod review process, this system would meaningfully expedite the review turnaround of draft ordinances during the First Reading referral period."  
  *(Linear scale: 1 to 5)*

---

### **Section 3: Standard System Usability Scale (SUS; Brooke, 1996)**

*Instructions: For each of the following 10 statements, please select the response that best reflects your immediate reaction. Please do not spend too much time on any single statement.*  
*Scale: 1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree*

* **SUS1:** "I think that I would like to use this system frequently for draft ordinance review."  
  *(Linear scale: 1 to 5)*
* **SUS2:** "I found the system unnecessarily complex."  
  *(Linear scale: 1 to 5)*
* **SUS3:** "I thought the system was easy to use."  
  *(Linear scale: 1 to 5)*
* **SUS4:** "I think that I would need the support of a technical person to be able to use this system."  
  *(Linear scale: 1 to 5)*
* **SUS5:** "I found the various functions in this system were well integrated."  
  *(Linear scale: 1 to 5)*
* **SUS6:** "I thought there was too much inconsistency in this system."  
  *(Linear scale: 1 to 5)*
* **SUS7:** "I would imagine that most legal researchers would learn to use this system very quickly."  
  *(Linear scale: 1 to 5)*
* **SUS8:** "I found the system very cumbersome to use."  
  *(Linear scale: 1 to 5)*
* **SUS9:** "I felt very confident using the system."  
  *(Linear scale: 1 to 5)*
* **SUS10:** "I needed to learn a lot of things before I could get going with this system."  
  *(Linear scale: 1 to 5)*

---

### **Section 4: Diagnostic Explainability, Transparency & Saliency (XAI)**

*Instructions: Rate the clarity and transparency of the system's legal explanations and alerts.*  
*Scale: 1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree*

* **XAI1 (Statutory Context Clarity):**  
  "The system presents sufficient statutory context (act title, enactment year, section numbers, and verbatim text excerpts) to allow me to verify why an alert was triggered without having to leave the screen."  
  *(Linear scale: 1 to 5)*

* **XAI2 (Token Salience Highlighting):**  
  "The visual highlighting of conflicting keywords (e.g., prohibitions, mandatory conditions, conflicting limits) clearly illustrates the specific phrases causing the detected tension."  
  *(Linear scale: 1 to 5)*

* **XAI3 (Alert Tier Separation):**  
  "The distinction between Critical Preemption Alerts (vertical conflicts with national statutes) and Informational Coherence Notices (horizontal relationships with existing Davao City ordinances) is intuitive and logically sound."  
  *(Linear scale: 1 to 5)*

---

### **Section 5: Practical Workflow Fit, Alert Fatigue & Adoption Willingness**

*Instructions: Rate how well the tool fits into the institutional environment of the Davao City Council.*  
*Scale: 1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree*

* **WF1 (Routine Adoption Willingness):**  
  "I would actively recommend and utilize this tool in my regular legislative research duties if it were officially adopted by the Sangguniang Panlungsod."  
  *(Linear scale: 1 to 5)*

* **WF2 (Alert Fatigue & False Alarm Tolerance):**  
  "The number of warnings generated on standard municipal boilerplate clauses (e.g., title, repealing clause, effectivity clause) is manageable and does not distract from substantive legal analysis."  
  *(Linear scale: 1 to 5)*

* **WF3 (Decision-Support Role Perception):**  
  "The tool appropriately functions as an assistive screening aid that supports—rather than attempts to replace—the expert judgment and legal discretion of the researcher."  
  *(Linear scale: 1 to 5)*

---

### **Section 6: Qualitative Feedback & Recommendations**

*Objective: Capture nuanced qualitative insights, edge cases, and feature requests directly from practitioners.*

* **Q1 (Strengths):**  
  "What specific features, outputs, or aspects of the system did you find most helpful during your review of draft ordinances?"  
  *(Paragraph text)*

* **Q2 (Weaknesses & Edge Cases):**  
  "What specific legal nuances, exceptions, or local ordinance provisions did the system appear to struggle with or misinterpret during testing?"  
  *(Paragraph text)*

* **Q3 (Future Enhancements):**  
  "What improvements or additional capabilities (e.g., exportable PDF compliance reports, automated legislative routing, Cebuano/vernacular language support) would make this tool more effective for the Sangguniang Panlungsod?"  
  *(Paragraph text)*

---

## **4. Data Analysis & Statistical Reporting Plan**

Upon completion of survey collection from the 15 respondents:

### **1. Quantitative Analysis**
* **Descriptive Statistics:** Calculate Mean, Standard Deviation ($SD$), and Median for each Likert item across PU, XAI, and WF dimensions.
* **Composite SUS Score Calculation:**
  $$\text{SUS} = 2.5 \times \left( \sum_{i \in \text{odd}} (R_i - 1) + \sum_{j \in \text{even}} (5 - R_j) \right)$$
  The composite SUS score will be reported as $\text{Mean} \pm SD$, plotted against Sauro & Lewis (2016) percentile curves, and assigned a standardized usability grade (e.g., Grade A: $\ge 80.3$; Grade B: $68.0 - 80.2$).
* **Cross-Tabulation:** Examine whether perceived usefulness correlates with prior manual search hours or legal experience tenure.

### **2. Qualitative Thematic Analysis**
* Thematic categorization of open-ended responses into:
  1. *Key Institutional Strengths* (e.g., rapid discovery of obscure pre-war Commonwealth Acts or Presidential Decrees).
  2. *Observed Limitations & Edge Cases* (e.g., distinguishing delegated local fee-setting authority under RA 7160 §143 from prohibited taxation under §133).
  3. *Actionable Roadmap Recommendations* for production LISSP integration.

### **3. Manuscript Integration**
* **Chapter 4 (§4.4):** Create dedicated section titled *"End-User Usability, Diagnostic Transparency, and Technology Acceptance"*, incorporating:
  * Table 4.6: *Quantitative Usability and Acceptance Scores across 15 SP Legal Researchers (TAM & SUS)*.
  * Figure 4.8: *Diverging Likert Scale Distribution for Perceived Usefulness, Transparency, and Workflow Fit*.
  * Figure 4.9: *System Usability Scale (SUS) Score Distribution against Industry Benchmarks*.
* **Chapter 5 (§5.1 & §5.3):** Synthesize findings under the third specific objective, grounding the practical contributions of the work in verified practitioner feedback.
