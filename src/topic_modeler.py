"""
topic_modeler.py
================
Automated Unsupervised Statutory Topic Discovery and Legal Categorization
with Consolidated Macro-Domains and >= 1% Minimum Corpus Threshold.

Features:
- Unsupervised discovery + Hierarchical Macro-Domain Consolidation:
  Merges template-based sub-clusters (e.g. school renamings, conversions, creations) into unified substantive legal domains.
  Reassigns any micro-cluster (< 1% of corpus) to its closest semantic parent centroid.
- Cosine-normalized vector space and Class-based TF-IDF (c-TF-IDF) extraction.
- Exports enriched categorized corpus and topic summary tables.
- Model persistence for instant inference and draft ordinance categorization.
"""

import os
import sys
import re
import json
import pickle
import argparse
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

from src.preprocess import load_corpus, clean_legal_text, parse_statutory_metadata


LEGAL_STOPWORDS = {
    'act', 'acts', 'section', 'sections', 'sec', 'hereby', 'thereof', 'therefor',
    'therein', 'whereas', 'be', 'it', 'enacted', 'senate', 'house', 'representatives',
    'philippines', 'congress', 'assembled', 'provided', 'further', 'general',
    'order', 'orders', 'decree', 'decrees', 'president', 'presidential',
    'republic', 'national', 'state', 'government', 'davao', 'city', 'office',
    'shall', 'may', 'must', 'any', 'all', 'such', 'upon', 'under', 'pursuant',
    'provisions', 'accordance', 'law', 'laws', 'force', 'effect', 'approval',
    'approved', 'take', 'day', 'days', 'month', 'months', 'year', 'years',
    'hundred', 'thousand', 'pesos', 'philippine', 'malacanang', 'manila',
    'known', 'cited', 'otherwise', 'following', 'including', 'person', 'persons'
}


DOMAIN_KEYWORD_TAXONOMY = {
    "Education & Academic Institutions": [
        'elementary school', 'high school', 'integrated school', 'vocational school',
        'school of arts and trades', 'college', 'university', 'curriculum', 'education culture',
        'sports issue', 'campus', 'elementary', 'school', 'school arts', 'trades', 'polytechnic',
        'changing the name', 'renaming', 'independent high'
    ],
    "Public Utilities & Telecommunications Franchises": [
        'telecommunications', 'broadcast', 'broadcasting', 'radio', 'television', 'frequency',
        'temporary permit', 'private fixed', 'transmitting', 'station', 'franchise construct',
        'scope franchise', 'franchise', 'electric light', 'heat and power', 'light and power',
        'electric', 'power system', 'thirty six', 'ice plant', 'cold storage'
    ],
    "Local Government & Territorial Boundaries": [
        'barrio', 'barrios', 'sitio', 'sitios', 'municipality', 'barangay', 'province',
        'boundary', 'constituting', 'territory', 'thence', 'sitio', 'annex barangay'
    ],
    "Public Finance & General Appropriations": [
        'appropriation', 'appropriating', 'appropriated', 'budget', 'operating expenses',
        'expenditures', 'funds for', 'not appropriated', 'sums much', 'out funds',
        'insular treasury', 'the sum', 'appropriating funds', 'fiscal ending'
    ],
    "Taxation, Tariffs & Revenue Administration": [
        'customs code', 'tariff', 'tariff and customs', 'excise', 'taxation',
        'internal revenue', 'import duty', 'duties', 'taxes', 'rates import'
    ],
    "Public Health, Hospitals & Medical Services": [
        'bed capacity', 'hospital', 'infirmary', 'medical center', 'health center',
        'sanitation', 'physician', 'disease', 'ten bed', 'medical services', 'district hospital'
    ],
    "Judiciary, Courts & Administration of Justice": [
        'trial court', 'regional trial', 'court', 'judicial', 'judiciary', 'prosecutor',
        'jurisdiction', 'judge', 'stationed the', 'reorganization amended'
    ],
    "Public Works, Highways & Transportation": [
        'road', 'highway', 'bridge', 'public works', 'infrastructure', 'transportation',
        'lto', 'traffic', 'into road', 'port', 'port zone', 'ports authority', 'ppa'
    ],
    "Public Holidays & Cultural Commemorations": [
        'holiday', 'special nonworking', 'special working', 'commemoration',
        'foundation day', 'working holiday', 'anniversary'
    ],
    "Criminal Law, Public Safety & Law Enforcement": [
        'penal', 'penalty', 'crime', 'imprisonment', 'firearms', 'dangerous drugs',
        'police', 'punished', 'offense', 'forfeiture'
    ],
    "Natural Resources, Environment & Agriculture": [
        'forest', 'mining', 'mineral', 'timber', 'fisheries', 'natural resources',
        'agriculture', 'lands', 'public land', 'watershed'
    ],
    "Labor, Employment & Civil Service": [
        'labor', 'employment', 'worker', 'wages', 'civil service', 'employees',
        'retirement', 'pension', 'compensation', 'benefits'
    ],
    "Elections, Suffrage & Governance": [
        'election', 'electoral', 'commission on elections', 'comelec', 'ballot',
        'voter', 'suffrage', 'registration of voters'
    ],
    "Executive Issuances & Policy Reorganization": [
        'executive', 'powers vested', 'presidential', 'policy', 'decree', 'economic',
        'ferdinand', 'virtue the', 'the executive', 'dated', 'vested', 'powers', 'program'
    ],
    "Statutory Codes & General Legal Amendments": [
        'administrative code', 'amend', 'commonwealth numbered', 'revised',
        'numbered one', 'code amended', 'numbered twenty', 'forty', 'ninety', 'one and'
    ]
}


def extract_c_tf_idf(documents_per_topic: Dict[int, str], top_n: int = 10) -> Dict[int, List[Tuple[str, float]]]:
    """Computes Class-based TF-IDF across grouped topic documents."""
    topics = sorted(documents_per_topic.keys())
    corpus = [documents_per_topic[t] for t in topics]
    
    vec = CountVectorizer(
        stop_words=list(LEGAL_STOPWORDS),
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.85,
        token_pattern=r'(?u)\b[a-zA-Z]{3,}\b'
    )
    X = vec.fit_transform(corpus)
    words = np.array(vec.get_feature_names_out())
    
    tf = X.toarray() / np.maximum(X.toarray().sum(axis=1, keepdims=True), 1e-9)
    doc_freq = (X.toarray() > 0).sum(axis=0)
    idf = np.log(1 + (len(topics) / np.maximum(doc_freq, 1)))
    c_tf_idf = tf * idf
    
    topic_keywords = {}
    for idx, t in enumerate(topics):
        top_indices = np.argsort(c_tf_idf[idx])[::-1][:top_n]
        topic_keywords[t] = [(words[i], float(c_tf_idf[idx, i])) for i in top_indices]
        
    return topic_keywords


def assign_domain_by_keywords(keywords: List[Tuple[str, float]]) -> str:
    """Matches a cluster's c-TF-IDF keyword distribution to a consolidated macro-domain."""
    if not keywords:
        return "General Statutory Provisions"
        
    domain_scores = {k: 0.0 for k in DOMAIN_KEYWORD_TAXONOMY}
    
    for rank, (kw, weight) in enumerate(keywords[:10]):
        kw_clean = kw.lower()
        rank_multiplier = 1.0 / (rank + 1)
        for domain, terms in DOMAIN_KEYWORD_TAXONOMY.items():
            for term in terms:
                if re.search(r'\b' + re.escape(term) + r'\b', kw_clean):
                    domain_scores[domain] += weight * rank_multiplier * 5.0
                    break
                    
    best_domain = max(domain_scores, key=domain_scores.get)
    if domain_scores[best_domain] > 0.05:
        return best_domain
    return "Executive Issuances & Policy Reorganization"


class StatutoryTopicModeler:
    """Unsupervised Topic Modeler with Consolidated Macro-Domains & >=1% Threshold."""
    
    def __init__(self, n_initial_clusters: int = 28, max_features: int = 25000, min_corpus_pct: float = 1.0):
        self.n_initial_clusters = n_initial_clusters
        self.max_features = max_features
        self.min_corpus_pct = min_corpus_pct
        
        self.vectorizer = TfidfVectorizer(
            stop_words=list(LEGAL_STOPWORDS),
            ngram_range=(1, 2),
            max_features=self.max_features,
            min_df=3,
            max_df=0.75,
            sublinear_tf=True,
            token_pattern=r'(?u)\b[a-zA-Z]{3,}\b'
        )
        self.dim_reducer = TruncatedSVD(n_components=64, random_state=42)
        self.cluster_model = MiniBatchKMeans(
            n_clusters=self.n_initial_clusters,
            random_state=42,
            batch_size=1024,
            max_iter=300,
            n_init=5
        )
        self.macro_centroids: Optional[np.ndarray] = None
        self.macro_metadata: Dict[int, Dict[str, Any]] = {}
        self.domain_to_id: Dict[str, int] = {}
        self.is_fitted = False

    def fit_transform(self, documents: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fits initial clusters, groups into macro-domains, and enforces >=1% threshold.
        """
        print(f"[Topic Modeler] Vectorizing {len(documents)} statutes with TF-IDF...")
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        
        print(f"[Topic Modeler] Reducing to 64 SVD components...")
        svd_matrix = self.dim_reducer.fit_transform(tfidf_matrix)
        norm_svd_matrix = normalize(svd_matrix)
        
        print(f"[Topic Modeler] Performing initial clustering into {self.n_initial_clusters} micro-clusters...")
        self.cluster_model.fit(svd_matrix)
        init_centroids = normalize(self.cluster_model.cluster_centers_)
        init_labels = np.argmax(cosine_similarity(norm_svd_matrix, init_centroids), axis=1)
        
        # Step 1: Compute c-TF-IDF for initial micro-clusters
        docs_per_init = {}
        for t in range(self.n_initial_clusters):
            idx = np.where(init_labels == t)[0]
            docs_per_init[t] = " ".join([documents[i] for i in idx]) if len(idx) > 0 else ""
        init_keywords = extract_c_tf_idf(docs_per_init, top_n=10)
        
        # Step 2: Map each initial cluster to its Macro Domain
        init_to_macro_name = {}
        for t in range(self.n_initial_clusters):
            kws = init_keywords.get(t, [])
            macro_name = assign_domain_by_keywords(kws)
            init_to_macro_name[t] = macro_name
            
        doc_macro_names = np.array([init_to_macro_name[lab] for lab in init_labels])
        
        # Step 3: Enforce >= 1% Minimum Threshold
        total_docs = len(documents)
        min_doc_count = int(total_docs * (self.min_corpus_pct / 100.0))
        
        # Identify domains that meet the threshold
        unique_domains = sorted(list(set(doc_macro_names)))
        valid_domains = [d for d in unique_domains if (doc_macro_names == d).sum() >= min_doc_count]
        
        print(f"[Topic Modeler] Consolidating into {len(valid_domains)} Macro Legal Domains (>= {self.min_corpus_pct}% threshold)...")
        
        # Create domain IDs
        self.domain_to_id = {dom: idx for idx, dom in enumerate(valid_domains)}
        
        # Calculate Macro Centroids for valid domains
        macro_centroids_list = []
        for dom in valid_domains:
            idx = np.where(doc_macro_names == dom)[0]
            centroid = norm_svd_matrix[idx].mean(axis=0)
            macro_centroids_list.append(centroid)
            
        self.macro_centroids = normalize(np.array(macro_centroids_list))
        
        # Re-assign all documents (including any merged micro-clusters) to closest macro centroid
        sims_matrix = cosine_similarity(norm_svd_matrix, self.macro_centroids)
        final_topic_ids = np.argmax(sims_matrix, axis=1)
        
        # Calculate calibrated confidence scores
        scaled_sims = np.exp(sims_matrix * 6.0)
        confidences = scaled_sims[np.arange(len(scaled_sims)), final_topic_ids] / np.maximum(scaled_sims.sum(axis=1), 1e-9)
        
        # Step 4: Compute final c-TF-IDF for the consolidated macro domains
        docs_per_macro = {}
        for mid in range(len(valid_domains)):
            idx = np.where(final_topic_ids == mid)[0]
            docs_per_macro[mid] = " ".join([documents[i] for i in idx]) if len(idx) > 0 else ""
        macro_keywords = extract_c_tf_idf(docs_per_macro, top_n=12)
        
        self.macro_metadata = {}
        for mid, dom_name in enumerate(valid_domains):
            kws = macro_keywords.get(mid, [])
            count = int((final_topic_ids == mid).sum())
            pct = (count / total_docs) * 100.0
            
            self.macro_metadata[mid] = {
                "topic_id": mid,
                "domain_name": dom_name,
                "keywords": [k[0] for k in kws],
                "keyword_weights": kws,
                "doc_count": count,
                "corpus_percentage": round(pct, 2)
            }
            
        self.is_fitted = True
        return final_topic_ids, confidences

    def predict(self, text: str) -> Dict[str, Any]:
        """Classifies an unseen statute or local ordinance text into discovered macro domains."""
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
            
        clean_doc = clean_legal_text(text)
        tfidf_vec = self.vectorizer.transform([clean_doc])
        svd_vec = self.dim_reducer.transform(tfidf_vec)
        norm_svd_vec = normalize(svd_vec)
        
        sims = cosine_similarity(norm_svd_vec, self.macro_centroids)[0]
        scaled_sims = np.exp(sims * 6.0)
        probs = scaled_sims / np.maximum(scaled_sims.sum(), 1e-9)
        
        top_topic_id = int(np.argmax(sims))
        raw_sim = float(sims[top_topic_id])
        confidence = float(probs[top_topic_id])
        
        meta = self.macro_metadata[top_topic_id]
        
        top_3_indices = np.argsort(sims)[::-1][:3]
        candidate_ranks = [
            {
                "topic_id": int(tid),
                "domain_name": self.macro_metadata[int(tid)]["domain_name"],
                "similarity": float(round(sims[tid], 4)),
                "probability": float(round(probs[tid], 4)),
                "keywords": self.macro_metadata[int(tid)]["keywords"][:5]
            }
            for tid in top_3_indices
        ]
        
        return {
            "assigned_topic_id": top_topic_id,
            "domain_name": meta["domain_name"],
            "cosine_similarity": round(raw_sim, 4),
            "confidence": round(confidence, 4),
            "top_keywords": meta["keywords"],
            "candidate_rankings": candidate_ranks
        }

    def save(self, filepath: str) -> None:
        """Saves fitted topic model to disk."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump({
                "n_initial_clusters": self.n_initial_clusters,
                "max_features": self.max_features,
                "min_corpus_pct": self.min_corpus_pct,
                "vectorizer": self.vectorizer,
                "dim_reducer": self.dim_reducer,
                "macro_centroids": self.macro_centroids,
                "macro_metadata": self.macro_metadata,
                "domain_to_id": self.domain_to_id,
                "is_fitted": self.is_fitted
            }, f)
        print(f"[Save] Consolidated topic model saved to {filepath}")

    @classmethod
    def load(cls, filepath: str) -> 'StatutoryTopicModeler':
        """Loads a saved topic model from disk."""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        obj = cls(
            n_initial_clusters=data["n_initial_clusters"],
            max_features=data["max_features"],
            min_corpus_pct=data["min_corpus_pct"]
        )
        obj.vectorizer = data["vectorizer"]
        obj.dim_reducer = data["dim_reducer"]
        obj.macro_centroids = data["macro_centroids"]
        obj.macro_metadata = data["macro_metadata"]
        obj.domain_to_id = data["domain_to_id"]
        obj.is_fitted = data["is_fitted"]
        return obj


def run_pipeline(
    corpus_dir: str = ".",
    output_dir: str = "output",
    n_initial: int = 28,
    min_pct: float = 1.0,
    include_executive: bool = True
) -> None:
    """Executes the full preprocessing, consolidated topic clustering, and export pipeline."""
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"=== Starting Consolidated Statutory Topic Modeling Pipeline ===")
    records = load_corpus(base_dir=corpus_dir, include_executive=include_executive)
    docs_to_fit = [r["searchable_doc"] for r in records]
    
    modeler = StatutoryTopicModeler(n_initial_clusters=n_initial, min_corpus_pct=min_pct)
    topic_ids, confidences = modeler.fit_transform(docs_to_fit)
    
    # Enrich records
    print(f"[Topic Modeler] Enriching records with macro-domain metadata...")
    for idx, r in enumerate(records):
        t_id = int(topic_ids[idx])
        meta = modeler.macro_metadata[t_id]
        r["topic_id"] = t_id
        r["topic_label"] = meta["domain_name"]
        r["topic_confidence"] = float(round(confidences[idx], 4))
        r["topic_keywords"] = meta["keywords"][:6]
        
    # Export categorized JSONL
    enriched_path = os.path.join(output_dir, "categorized_corpus.jsonl")
    with open(enriched_path, 'w', encoding='utf-8') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f"[Export] Enriched corpus written to {enriched_path}")
    
    # Save Model
    model_path = os.path.join(output_dir, "statutory_topic_model.pkl")
    modeler.save(model_path)
    
    # Export Topic Summary Table (CSV)
    summary_rows = []
    for mid in range(len(modeler.macro_metadata)):
        meta = modeler.macro_metadata[mid]
        topic_records = [r for r in records if r["topic_id"] == mid]
        top_samples = sorted(topic_records, key=lambda x: x["topic_confidence"], reverse=True)[:3]
        samples_str = " | ".join([f"[{s['law_number']}] {s['long_title'][:55]}..." for s in top_samples])
        
        summary_rows.append({
            "Topic_ID": mid,
            "Macro_Legal_Domain": meta["domain_name"],
            "Document_Count": meta["doc_count"],
            "Corpus_Pct": f"{meta['corpus_percentage']}%",
            "Top_Salient_Keywords": ", ".join(meta["keywords"][:8]),
            "Representative_Statutes": samples_str
        })
        
    summary_df = pd.DataFrame(summary_rows)
    summary_csv_path = os.path.join(output_dir, "topic_summary.csv")
    summary_df.to_csv(summary_csv_path, index=False)
    print(f"[Export] Summary report written to {summary_csv_path}")
    
    print("\n=== CONSOLIDATED MACRO-DOMAIN SUMMARY (>= 1% Corpus Threshold) ===")
    for _, row in summary_df.iterrows():
        print(f"[{row['Topic_ID']:02d}] {row['Macro_Legal_Domain']} ({row['Document_Count']} laws - {row['Corpus_Pct']})")
        print(f"     Keywords: {row['Top_Salient_Keywords']}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Philippine Statutory Topic Modeling")
    parser.add_argument("--n_initial", type=int, default=28, help="Number of initial micro-clusters")
    parser.add_argument("--min_pct", type=float, default=1.0, help="Minimum corpus percentage threshold")
    parser.add_argument("--include_executive", action="store_true", default=True, help="Include EOs and PDs")
    args = parser.parse_args()
    
    run_pipeline(n_initial=args.n_initial, min_pct=args.min_pct, include_executive=args.include_executive)
