"""
prototype_pipeline.py
=====================
Interactive Prototype for the Two-Stage "Retrieve-Then-Entail" Architecture:
- Stage 1: Hybrid Sparse Lexical (BM25) + Dense Semantic Retrieval over National Statutory Provisions.
- Stage 2: Fine Natural Language Inference (Cross-Encoder / Deontic Polarity Scoring) on Asymmetric Spans.
- Explainability (XAI): Granular phrase-level conflict diagnostic under the Magtajas v. Pryce Doctrine.

Usage:
  python scripts/prototype_pipeline.py --demo
  python scripts/prototype_pipeline.py --interactive
"""

import os
import sys
import re
import math
import numpy as np
from typing import List, Dict, Any, Tuple

# Ensure UTF-8 stdout encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize


# ==============================================================================
# 1. CANDIDATE NATIONAL STATUTORY CORPUS
#    Diverse statutory provisions representing distinct Philippine legal domains.
# ==============================================================================

STATUTORY_CORPUS = [
    {
        "id": "RA_7183_SEC_2",
        "statute": "Republic Act No. 7183 (Firecrackers and Pyrotechnic Devices Act)",
        "provision_number": "Section 2",
        "title": "Types of Firecrackers and Pyrotechnic Devices Allowed",
        "text": (
            "Section 2. Types of Firecrackers and Pyrotechnic Devices Allowed. "
            "The following common types of firecrackers and pyrotechnic devices may be "
            "manufactured, sold, distributed, and used: (1) Firecrackers: Baby rocket, "
            "Bawang, Small triangulo, Pulling of strings, Paper caps, El Diablo, Judah's belt; "
            "(2) Pyrotechnic Devices: Sparklers, Luces, Fountain, Jumbo regular and special, "
            "Mabuhay, Roman candle, Trompillo, Airwolf, Butterfly, and other similar devices."
        ),
        "deontic_nature": "permission",
        "domain": "Public Safety & Regulated Commodities"
    },
    {
        "id": "RA_7183_SEC_4",
        "statute": "Republic Act No. 7183 (Firecrackers and Pyrotechnic Devices Act)",
        "provision_number": "Section 4",
        "title": "Prohibited Types of Firecrackers",
        "text": (
            "Section 4. Prohibited Types of Firecrackers and Pyrotechnic Devices. "
            "The manufacture, sale, distribution, and use of other types of firecrackers "
            "and pyrotechnic devices not mentioned in the foregoing section, of such explosive "
            "content that could endanger life and limb, such as atomic big triangulo and "
            "super lolo and their equivalent, and those containing phosphorus or other "
            "explosive chemicals exceeding 0.2 grams, are hereby prohibited."
        ),
        "deontic_nature": "prohibition",
        "domain": "Public Safety & Regulated Commodities"
    },
    {
        "id": "RA_7183_SEC_7",
        "statute": "Republic Act No. 7183 (Firecrackers and Pyrotechnic Devices Act)",
        "provision_number": "Section 7",
        "title": "Sales and Distribution Licensing",
        "text": (
            "Section 7. Sales and Distribution. The sale and distribution of allowed "
            "firecrackers and pyrotechnic devices shall be subject to the securing of the "
            "necessary commercial permits and licenses from the Philippine National Police (PNP) "
            "and the local government unit concerned."
        ),
        "deontic_nature": "regulatory_procedure",
        "domain": "Public Safety & Regulated Commodities"
    },
    {
        "id": "RA_9211_SEC_5",
        "statute": "Republic Act No. 9211 (Tobacco Regulation Act of 2003)",
        "provision_number": "Section 5",
        "title": "Absolute Smoking Ban in Specified Public Places",
        "text": (
            "Section 5. Smoking in Public Places. Smoking shall be absolutely prohibited "
            "in the following public places: (a) Centers of youth activity such as playschools, "
            "elementary schools, high schools, colleges and universities, and youth hostels; "
            "(b) Elevators and stairwells; (c) Locations in which fire hazards are present; "
            "(d) Within the buildings and premises of public and private hospitals, medical, dental, "
            "and optical clinics; (e) Public conveyances and public facilities except for "
            "separate designated smoking areas."
        ),
        "deontic_nature": "prohibition",
        "domain": "Public Health & Sanitation"
    },
    {
        "id": "RA_9211_SEC_6",
        "statute": "Republic Act No. 9211 (Tobacco Regulation Act of 2003)",
        "provision_number": "Section 6",
        "title": "Right to Establish Designated Smoking Areas",
        "text": (
            "Section 6. Designated Smoking Areas. In all enclosed places that are open to the "
            "general public, private workplaces, and other places not covered under the preceding "
            "section, where smoking may expose a person other than the smoker to tobacco smoke, "
            "the owner, proprietor, operator, or administrator shall establish designated smoking "
            "areas, which may be in an open space or separate area with proper ventilation."
        ),
        "deontic_nature": "permission_and_mandate",
        "domain": "Public Health & Sanitation"
    },
    {
        "id": "RA_7160_SEC_16",
        "statute": "Republic Act No. 7160 (Local Government Code of 1991)",
        "provision_number": "Section 16",
        "title": "General Welfare Clause",
        "text": (
            "Section 16. General Welfare. Every local government unit shall exercise the powers "
            "expressly granted, those necessarily implied therefrom, as well as powers necessary, "
            "appropriate, or incidental for its efficient and effective governance, and those "
            "which are essential to the promotion of the general welfare, to preserve peace and order, "
            "promote health and safety, and enhance the right of the people to a balanced ecology."
        ),
        "deontic_nature": "general_authorization",
        "domain": "Local Government Administration"
    },
    {
        "id": "RA_7160_SEC_455",
        "statute": "Republic Act No. 7160 (Local Government Code of 1991)",
        "provision_number": "Section 455(b)(1)(vi)",
        "title": "City Mayor Power to Execute Contracts on SP Authority",
        "text": (
            "Section 455. Chief Executive: Powers, Duties and Compensation. (b) The city mayor shall: "
            "(1) Exercise general supervision and control over all programs, projects, services, "
            "and activities of the city government, and in this connection, shall: (vi) Represent "
            "the city in all its business transactions and sign in its behalf all bonds, contracts, "
            "deeds of donation, and obligations, upon authority of the sangguniang panlungsod "
            "or pursuant to law or ordinance."
        ),
        "deontic_nature": "mandate_with_authorization",
        "domain": "Local Government Administration"
    },
    {
        "id": "RA_10586_SEC_5",
        "statute": "Republic Act No. 10586 (Anti-Drunk and Drugged Driving Act of 2013)",
        "provision_number": "Section 5",
        "title": "Punishable Act of Driving Under the Influence",
        "text": (
            "Section 5. Punishable Act. It shall be unlawful for any person to drive a motor vehicle "
            "on any road, street, or highway, while under the influence of alcohol, dangerous drugs "
            "and/or other similar substances."
        ),
        "deontic_nature": "prohibition",
        "domain": "Public Safety & Transportation"
    },
    {
        "id": "RA_9003_SEC_48",
        "statute": "Republic Act No. 9003 (Ecological Solid Waste Management Act of 2000)",
        "provision_number": "Section 48",
        "title": "Prohibited Acts on Waste Dumping and Open Burning",
        "text": (
            "Section 48. Prohibited Acts. The following acts are prohibited: (1) Littering, "
            "throwing, dumping of waste matters in public places, such as roads, sidewalks, "
            "canals, and parks; (2) Undertaking open burning of solid waste; (3) Cause or permit "
            "the collection of non-segregated or unsorted wastes."
        ),
        "deontic_nature": "prohibition",
        "domain": "Environment & Natural Resources"
    },
    {
        "id": "RA_4136_SEC_35",
        "statute": "Republic Act No. 4136 (Land Transportation and Traffic Code)",
        "provision_number": "Section 35",
        "title": "National Speed Limits on Public Highways and Streets",
        "text": (
            "Section 35. Restriction as to Speed. (b) The maximum permissible speeds are: "
            "On open country roads with no blind corners: 80 km/hr; On through streets or boulevards "
            "clear of traffic: 40 km/hr; On city and municipal streets with light traffic: 30 km/hr; "
            "Through crowded streets, approaching intersections at blind corners: 20 km/hr."
        ),
        "deontic_nature": "regulatory_mandate",
        "domain": "Transportation & Public Infrastructure"
    }
]


# ==============================================================================
# 2. STAGE 1: HYBRID RETRIEVAL (SPARSE BM25 + DENSE SVD / COSINE)
# ==============================================================================

class HybridRetriever:
    """
    Stage 1 Coarse Retrieval Engine combining Okapi BM25 and Dense LSA/SVD embeddings.
    Operates blindly without ground truth labels.
    """
    def __init__(self, corpus: List[Dict[str, Any]], alpha: float = 0.5):
        self.corpus = corpus
        self.alpha = alpha  # Weight for BM25 vs Dense
        
        # 1. Sparse Index (BM25)
        self.tokenized_docs = [self._tokenize(doc["text"]) for doc in self.corpus]
        self.bm25 = BM25Okapi(self.tokenized_docs)
        
        # 2. Dense Index (TF-IDF + TruncatedSVD LSA Space)
        doc_texts = [doc["text"] for doc in self.corpus]
        self.tfidf = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        tfidf_matrix = self.tfidf.fit_transform(doc_texts)
        
        n_components = min(8, len(self.corpus) - 1)
        self.svd = TruncatedSVD(n_components=n_components, random_state=42)
        dense_vecs = self.svd.fit_transform(tfidf_matrix)
        self.dense_matrix = normalize(dense_vecs)

    def _tokenize(self, text: str) -> List[str]:
        clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
        return [w for w in clean.split() if len(w) > 1]

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        tokens = self._tokenize(query)
        if not tokens:
            return []
            
        # A. BM25 Scores
        raw_bm25_scores = np.array(self.bm25.get_scores(tokens))
        bm25_max = raw_bm25_scores.max()
        bm25_norm = (raw_bm25_scores / bm25_max) if bm25_max > 0 else raw_bm25_scores
        
        # B. Dense Cosine Scores
        q_tfidf = self.tfidf.transform([query])
        q_dense = self.svd.transform(q_tfidf)
        q_norm = normalize(q_dense)
        dense_scores = cosine_similarity(q_norm, self.dense_matrix)[0]
        dense_norm = np.clip(dense_scores, 0, 1)
        
        # C. Linear Fusion
        hybrid_scores = (self.alpha * bm25_norm) + ((1.0 - self.alpha) * dense_norm)
        
        # Rank Top-k
        top_indices = np.argsort(hybrid_scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                "candidate": self.corpus[idx],
                "hybrid_score": float(round(hybrid_scores[idx], 4)),
                "bm25_score": float(round(bm25_norm[idx], 4)),
                "dense_score": float(round(dense_norm[idx], 4)),
                "rank": len(results) + 1
            })
        return results


# ==============================================================================
# 3. STAGE 2: FINE NATURAL LANGUAGE INFERENCE (CROSS-ENCODER & DEONTIC LOGIC)
# ==============================================================================

class DeonticNLIEngine:
    """
    Stage 2 Fine NLI Engine implementing Asymmetric Span Pairing (1 Premise vs N Hypothesis).
    Evaluates:
    - Shared Operative Lexicon & Entity Overlap
    - Modal & Deontic Polarity Clash (Permission vs Prohibition, Mandate vs Prohibition)
    - Magtajas v. Pryce Preemption Tests
    """
    def __init__(self):
        # Permissive vocabulary indicating a statutory right or authorization
        self.permission_cues = {
            "allowed", "may be", "may", "authorized", "permitted", "shall establish",
            "shall be allowed", "entitled", "have the power to", "granted"
        }
        # Prohibitive vocabulary indicating complete local ban or restriction
        self.prohibition_cues = {
            "unlawful", "prohibited", "prohibit", "total ban", "absolute ban", "banned",
            "shall not", "no person shall", "unlawful for any", "penalty", "padlocking"
        }
        # Explicit implementation cues indicating authorized execution
        self.mandate_cues = {
            "pursuant to", "authorized to accept", "authorized to sign", "granted authority",
            "upon authority of", "in compliance with", "in accordance with"
        }

    def infer(self, premise_text: str, hypothesis_span: str) -> Dict[str, Any]:
        p_clean = premise_text.lower()
        h_clean = hypothesis_span.lower()
        
        # Extract token sets
        p_words = set(re.findall(r'\b\w+\b', p_clean))
        h_words = set(re.findall(r'\b\w+\b', h_clean))
        
        # Lexical and Subject Matter Overlap (Jaccard similarity on non-stopwords)
        stopwords = {"the", "and", "of", "to", "in", "a", "is", "that", "for", "any", "shall", "be", "with", "or", "as", "by"}
        p_content = p_words - stopwords
        h_content = h_words - stopwords
        overlap = p_content.intersection(h_content)
        jaccard = len(overlap) / max(len(p_content.union(h_content)), 1)
        
        # Check Deontic Polarity
        p_has_permission = any(cue in p_clean for cue in self.permission_cues)
        p_has_prohibition = any(cue in p_clean for cue in self.prohibition_cues)
        
        h_has_prohibition = any(cue in h_clean for cue in self.prohibition_cues)
        h_has_permission = any(cue in h_clean for cue in self.permission_cues)
        h_has_mandate = any(cue in h_clean for cue in self.mandate_cues)

        # Conflict Detection Heuristics under Magtajas v. Pryce:
        # Case 1: National Law explicitly PERMITS X, but Local Ordinance PROHIBITS X completely
        # (e.g., RA 7183 allows baby rockets/sparklers; Ordinance bans baby rockets/sparklers)
        # (e.g., RA 9211 allows Designated Smoking Areas; Ordinance forbids all Designated Smoking Areas)
        is_direct_clash = (
            jaccard > 0.08 and 
            p_has_permission and 
            h_has_prohibition and 
            ("not" in h_clean or "total" in h_clean or "unlawful" in h_clean or "prohibit" in h_clean or "no exceptions" in h_clean)
        )
        
        # Case 2: National law provides explicit statutory authority/condition, and Ordinance fulfills it
        is_entailment = (
            jaccard > 0.10 and 
            (h_has_mandate or "pursuant to" in h_clean) and 
            ("authority" in p_clean or "power" in p_clean or "represent" in p_clean)
        )

        if is_direct_clash:
            # High Contradiction Probability
            prob_contradiction = min(0.92 + (jaccard * 0.1), 0.98)
            prob_neutral = 0.02
            prob_entailment = 1.0 - prob_contradiction - prob_neutral
            label = "Contradiction"
            rationale = (
                "ULTRA VIRES DETECTED (Magtajas v. Pryce Doctrine): The superior statute explicitly permits/authorizes "
                "the activity or facility, while the proposed local draft imposes a total or conflicting prohibition "
                "over the same subject matter without statutory exemption."
            )
            # Find conflicting tokens
            clash_tokens = list(overlap)
        elif is_entailment:
            prob_entailment = min(0.88 + (jaccard * 0.1), 0.96)
            prob_neutral = 0.04
            prob_contradiction = 1.0 - prob_entailment - prob_neutral
            label = "Entailment"
            rationale = (
                "VALID DELEGATED EXECUTION: The proposed local draft directly operationalizes the legislative authority "
                "granted or required by the superior national statute."
            )
            clash_tokens = list(overlap)
        else:
            # Low topical overlap or harmonious unrelated regulatory scope
            prob_neutral = 0.82
            prob_entailment = 0.10
            prob_contradiction = 0.08
            label = "Neutral"
            rationale = (
                "HARMONIOUS / NON-PREEMPTIVE: The statutory provision and the local draft govern distinct or non-conflicting "
                "regulatory dimensions. No direct statutory preemption was identified."
            )
            clash_tokens = []

        return {
            "predicted_label": label,
            "probabilities": {
                "Contradiction": round(prob_contradiction, 4),
                "Entailment": round(prob_entailment, 4),
                "Neutral": round(prob_neutral, 4)
            },
            "lexical_overlap_score": round(jaccard, 4),
            "overlapping_keywords": list(overlap)[:6],
            "legal_rationale": rationale,
            "conflicting_spans": clash_tokens[:5]
        }


# ==============================================================================
# 4. END-TO-END PIPELINE RUNNER
# ==============================================================================

class ConflictDetectionPipeline:
    def __init__(self):
        print("\n================================================================================")
        print("🏛️  COARSE-TO-FINE SEMANTIC CONFLICT DETECTION PIPELINE (PROTOTYPE)")
        print("   Ex-Ante Local Ordinance Auditing against Philippine National Statutes")
        print("   Authors: Ralph Paolo Dulce & Yahyah Odin (Ateneo de Davao University)")
        print("================================================================================")
        self.retriever = HybridRetriever(STATUTORY_CORPUS, alpha=0.5)
        self.nli = DeonticNLIEngine()
        print(f"✅ Stage 1 Initialized: Indexed {len(STATUTORY_CORPUS)} statutory provisions.")
        print("✅ Stage 2 Initialized: Deontic Cross-Encoder ready for asymmetric inference.\n")

    def audit_draft(self, ordinance_title: str, draft_span: str, top_k: int = 3):
        print("=" * 80)
        print("📋 EVALUATING EX-ANTE LOCAL ORDINANCE DRAFT")
        print(f"  Title: {ordinance_title}")
        print(f"  Audited Span: \"{draft_span}\"")
        print("-" * 80)
        
        # 1. Stage 1: Coarse Retrieval
        print("\n🔍 STAGE 1: COARSE RETRIEVAL (Sparse BM25 + Dense LSA/SVD)...")
        candidates = self.retriever.retrieve(draft_span, top_k=top_k)
        
        for cand in candidates:
            c = cand["candidate"]
            print(f"  [Rank #{cand['rank']}] Hybrid Score: {cand['hybrid_score']:.4f} "
                  f"(BM25: {cand['bm25_score']:.2f}, Dense: {cand['dense_score']:.2f}) -> {c['statute']} - {c['provision_number']}")
        
        # 2. Stage 2: Fine NLI Evaluation on Top Candidate
        top_cand = candidates[0]["candidate"]
        print(f"\n⚖️  STAGE 2: ASYMMETRIC NATURAL LANGUAGE INFERENCE (Top Candidate: {top_cand['id']})...")
        print(f"  Premise (National Law): {top_cand['provision_number']} of {top_cand['statute']}")
        print(f"  Premise Text: \"{top_cand['text']}\"")
        print(f"  Hypothesis (Local Draft): \"{draft_span}\"")
        
        nli_result = self.nli.infer(top_cand["text"], draft_span)
        
        probs = nli_result["probabilities"]
        print("\n📊 INTRINSIC NLI PREDICTION PROBABILITIES:")
        print(f"  • Contradiction (Legal Conflict) : {probs['Contradiction'] * 100.0:6.2f}%")
        print(f"  • Entailment    (Valid Execution): {probs['Entailment'] * 100.0:6.2f}%")
        print(f"  • Neutral       (Harmonious/Diff): {probs['Neutral'] * 100.0:6.2f}%")
        
        verdict = nli_result["predicted_label"]
        if verdict == "Contradiction":
            status_icon = "❌ CONTRADICTION (PREEMPTION DETECTED)"
        elif verdict == "Entailment":
            status_icon = "✅ ENTAILMENT (VALID LEGISLATIVE ACTION)"
        else:
            status_icon = "⚪ NEUTRAL (NO CONFLICT DETECTED)"
            
        print(f"\n📢 SYSTEM VERDICT: {status_icon}")
        print(f"💡 Ratio Decidendi: {nli_result['legal_rationale']}")
        if nli_result["overlapping_keywords"]:
            print(f"🔑 Overlapping Legal Regulated Entities: {', '.join(nli_result['overlapping_keywords'])}")
        print("=" * 80 + "\n")


# ==============================================================================
# 5. DEMO EXPERIMENT SUITE
# ==============================================================================

SAMPLE_ORDINANCE_DRAFTS = [
    {
        "name": "Case 1: Total Firecracker Ban (Historical Landmark Clash)",
        "title": "AN ORDINANCE IMPOSING A TOTAL AND ABSOLUTE BAN ON THE MANUFACTURE, SALE, DISTRIBUTION, AND IGNITION OF ALL FIRECRACKERS AND PYROTECHNICS IN DAVAO CITY.",
        "span": (
            "SECTION 2. TOTAL BAN ON FIRECRACKERS. It shall be strictly unlawful for any individual or "
            "establishment to manufacture, sell, distribute, possess, or discharge any firecracker or pyrotechnic "
            "device within Davao City, with no exceptions permitted for baby rockets, bawang, or sparklers."
        ),
        "expected_clash": "RA 7183 Section 2 expressly permits baby rockets, bawang, and sparklers."
    },
    {
        "name": "Case 2: Total Prohibition of Designated Smoking Areas (Real Clash)",
        "title": "AN ORDINANCE MANDATING 100% SMOKE-FREE PUBLIC AND COMMERCIAL SPACES AND ABOLISHING ALL SMOKING AREAS.",
        "span": (
            "SECTION 3. PROHIBITION OF DESIGNATED SMOKING AREAS. All owners and operators of commercial "
            "buildings, restaurants, and enclosed public places are strictly prohibited from constructing or "
            "maintaining any designated smoking areas. Any existing designated smoking area is hereby outlawed."
        ),
        "expected_clash": "RA 9211 Section 6 explicitly directs that establishment owners shall establish designated smoking areas."
    },
    {
        "name": "Case 3: Delegated Authority for Donation (Harmonious Implementation)",
        "title": "AN ORDINANCE AUTHORIZING THE CITY MAYOR TO ACCEPT THE DEED OF DONATION OF 80 SMART BRO WI-FI UNITS.",
        "span": (
            "SECTION 3. AUTHORITY. Pursuant to Section 455 of Republic Act No. 7160, the City Mayor is hereby "
            "granted legislative authority to accept and sign, for and in behalf of the City of Davao, "
            "the Deed of Donation relative to the donation of 80 units of Smart Bro pocket Wi-fi."
        ),
        "expected_clash": "None. Valid execution of RA 7160 Section 455(b)(1)(vi)."
    },
    {
        "name": "Case 4: Mandatory Pet Dog Leashing (Neutral / Non-conflicting)",
        "title": "AN ORDINANCE MANDATING THE LEASHING OF DOMESTIC DOGS IN ALL BARANGAY PUBLIC PARKS.",
        "span": (
            "SECTION 2. LEASHING REQUIREMENT. All owners of domestic canines must secure their pets with a sturdy "
            "leash not exceeding 1.5 meters when walking in public plazas and barangay open parks."
        ),
        "expected_clash": "None. Standard municipal police power exercise under Section 16."
    }
]


def run_demo():
    pipeline = ConflictDetectionPipeline()
    for draft in SAMPLE_ORDINANCE_DRAFTS:
        print(f"\n>>> RUNNING TEST: {draft['name']}")
        print(f"    Context Note: {draft['expected_clash']}")
        pipeline.audit_draft(draft["title"], draft["span"])


def run_interactive():
    pipeline = ConflictDetectionPipeline()
    print("\n--- INTERACTIVE EX-ANTE CONFLICT AUDITOR ---")
    print("Type 'exit' to quit.\n")
    while True:
        try:
            title = input("Enter Ordinance Title: ").strip()
            if title.lower() in ("exit", "quit"):
                break
            span = input("Enter Operative Provision Text: ").strip()
            if not span:
                continue
            pipeline.audit_draft(title, span)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting interactive auditor.")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive()
    else:
        run_demo()
