import sys
sys.path.insert(0, ".")
from src.demo.app import NEURAL_ENGINE

query = "[AN ORDINANCE PROHIBITING THE OPERATION OF CASINO | SECTION 1: PROHIBITION OF CASINO OPERATIONS] The operation of gambling CASINO in the City of Cagayan de Oro is hereby prohibited."

raw_cands = NEURAL_ENGINE.retrieve_top_k(query, k=50, scope="national")

print(f"Top 15 Stage 1 Candidates for Magtajas Section 1:")
print("-" * 80)
for idx, c in enumerate(raw_cands[:15], 1):
    score = c.get('combined_score') or c.get('score') or 0.0
    print(f"{idx}. {c.get('citation')} | {c.get('title')} | Score: {score}")
    print(f"   Snippet: {c.get('text', '')[:120]}...\n")

# Check if Presidential Decree No. 1869 (PAGCOR Charter) is anywhere in top 50
pd1869 = [c for c in raw_cands if "1869" in c.get('citation', '') or "pagcor" in c.get('text', '').lower()]
print("=" * 80)
print(f"Is PD 1869 in Top 50? Found {len(pd1869)} matches:")
for c in pd1869:
    score = c.get('combined_score') or c.get('score') or 0.0
    print(f"  {c.get('citation')} | {c.get('title')} | Score: {score}")
