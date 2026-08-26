"""
categorize_query.py
===================
Interactive Lookup & Categorization Traceability Utility.

Allows:
1. Lookup by Law ID (e.g. `ra_7160_1991`, `act_1_1900`, `ca_1_1935`, `bp_14_1978`):
   Retrieves assigned category, topic confidence, keywords, and title.
2. Inference on Arbitrary Text / Local Ordinance Draft:
   Predicts the legal category, confidence distribution, and top-3 candidate domains.
"""

import os
import sys
import json
import argparse
from typing import Optional, Dict, Any

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.topic_modeler import StatutoryTopicModeler
from src.preprocess import clean_legal_text


class LegalCategorizerEngine:
    def __init__(self, model_path: str = "output/statutory_topic_model.pkl", categorized_corpus_path: str = "output/categorized_corpus.jsonl"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}. Please run topic_modeler.py first.")
            
        print(f"[Loading] Loading topic model from {model_path}...")
        self.modeler = StatutoryTopicModeler.load(model_path)
        
        self.indexed_laws: Dict[str, Dict[str, Any]] = {}
        if os.path.exists(categorized_corpus_path):
            print(f"[Loading] Loading categorized corpus index from {categorized_corpus_path}...")
            with open(categorized_corpus_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        rec = json.loads(line)
                        self.indexed_laws[rec["law_id"].lower()] = rec
            print(f"[Ready] Indexed {len(self.indexed_laws)} laws for instantaneous retrieval.")
        else:
            print("[Warning] Categorized corpus file not found; ID lookup might be limited.")

    def lookup_law_id(self, law_id: str) -> Optional[Dict[str, Any]]:
        """Look up an existing national statute by law ID."""
        key = law_id.strip().lower()
        if key in self.indexed_laws:
            rec = self.indexed_laws[key]
            return {
                "found": True,
                "law_id": rec["law_id"],
                "law_number": rec["law_number"],
                "category_type": rec["category"],
                "year": rec.get("year"),
                "long_title": rec["long_title"],
                "assigned_topic_id": rec["topic_id"],
                "topic_label": rec["topic_label"],
                "topic_confidence": rec["topic_confidence"],
                "topic_keywords": rec["topic_keywords"],
                "body_snippet": rec["body_snippet"],
                "url": rec.get("url", "")
            }
            
        # Try fuzzy match on law number
        for k, rec in self.indexed_laws.items():
            if law_id.lower() in rec["law_number"].lower():
                return {
                    "found": True,
                    "law_id": rec["law_id"],
                    "law_number": rec["law_number"],
                    "category_type": rec["category"],
                    "year": rec.get("year"),
                    "long_title": rec["long_title"],
                    "assigned_topic_id": rec["topic_id"],
                    "topic_label": rec["topic_label"],
                    "topic_confidence": rec["topic_confidence"],
                    "topic_keywords": rec["topic_keywords"],
                    "body_snippet": rec["body_snippet"],
                    "url": rec.get("url", "")
                }
        return {"found": False, "law_id": law_id, "message": "Law ID not found in indexed corpus."}

    def categorize_text(self, text: str) -> Dict[str, Any]:
        """Categorize an unseen text or draft ordinance."""
        prediction = self.modeler.predict(text)
        label = prediction.get("domain_name") or prediction.get("topic_label", "Unknown Domain")
        return {
            "input_preview": clean_legal_text(text)[:180] + "...",
            "assigned_topic_id": prediction["assigned_topic_id"],
            "topic_label": label,
            "confidence": prediction["confidence"],
            "top_keywords": prediction["top_keywords"],
            "candidate_rankings": prediction["candidate_rankings"]
        }


def print_result(res: Dict[str, Any]):
    print("=" * 60)
    if res.get("found") is False:
        print(f"[NOT FOUND] {res['message']}")
        print("=" * 60)
        return
        
    if "law_number" in res:
        print(f"LAW ID: {res['law_id']} | {res['law_number']} ({res.get('year', 'N/A')})")
        print(f"TITLE: {res['long_title']}")
        print(f"ASSIGNED CATEGORY: [{res['assigned_topic_id']:02d}] {res['topic_label']}")
        print(f"CONFIDENCE: {res['topic_confidence'] * 100:.1f}%")
        print(f"KEYWORDS: {', '.join(res['topic_keywords'])}")
        print(f"SNIPPET: {res['body_snippet'][:180]}...")
        if res.get("url"):
            print(f"SOURCE URL: {res['url']}")
    else:
        print(f"INPUT TEXT: {res['input_preview']}")
        print(f"PREDICTED CATEGORY: [{res['assigned_topic_id']:02d}] {res['topic_label']}")
        print(f"CONFIDENCE: {res['confidence'] * 100:.1f}%")
        print(f"KEYWORDS: {', '.join(res['top_keywords'])}")
        print("\nTOP CANDIDATE DOMAINS:")
        for cand in res["candidate_rankings"]:
            cand_name = cand.get("domain_name") or cand.get("label", "Unknown")
            print(f"  - [{cand['topic_id']:02d}] {cand_name} ({cand['probability']*100:.1f}%) | Kws: {', '.join(cand['keywords'])}")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query or Categorize Philippine Laws")
    parser.add_argument("--id", type=str, help="Law ID to look up (e.g. ra_7160_1991, bp_14_1978, ca_1_1935)")
    parser.add_argument("--text", type=str, help="Raw statutory text or ordinance snippet to categorize")
    args = parser.parse_args()
    
    engine = LegalCategorizerEngine()
    
    if args.id:
        result = engine.lookup_law_id(args.id)
        print_result(result)
    elif args.text:
        result = engine.categorize_text(args.text)
        print_result(result)
    else:
        print("Running demo test queries...")
        # Test 1: Sample local ordinance text
        demo_text = "AN ORDINANCE PROHIBITING THE USE, SALE, DISTRIBUTION AND ADVERTISEMENT OF VAPOR PRODUCTS AND ELECTRONIC CIGARETTES IN PUBLIC PLACES IN DAVAO CITY."
        print("\n--> Test 1: Predicting category for Davao City Draft Ordinance:")
        print_result(engine.categorize_text(demo_text))
        
        # Test 2: Sample telecom draft
        demo_text_2 = "AN ORDINANCE GRANTING A LOCAL PERMIT AND FRANCHISE TO OPERATE A WIRELESS TELECOMMUNICATIONS TOWER AND ANTENNA INFRASTRUCTURE."
        print("\n--> Test 2: Predicting category for Telecom Infrastructure:")
        print_result(engine.categorize_text(demo_text_2))
