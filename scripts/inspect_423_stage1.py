import sys
sys.path.insert(0, ".")
from src.demo.app import NEURAL_ENGINE

query = "[THE 2005 REVENUE CODE OF THE CITY OF DAVAO | SECTION 423: PAYMENT UNDER PROTEST] No protest against an assessment shall be entertained unless the taxpayer first pays under protest the full amount of the tax assessed by the City Treasurer."

raw_cands = NEURAL_ENGINE.retrieve_top_k(query, k=25, scope="national")

print(f"Top 10 Stage 1 Candidates for Section 423 (Payment Under Protest):")
print("-" * 80)
for idx, c in enumerate(raw_cands[:10], 1):
    score = c.get('combined_score') or c.get('score') or 0.0
    print(f"{idx}. {c.get('citation')} | {c.get('title')}")
    print(f"   Snippet: {c.get('text', '')[:100]}...\n")

# Check if RA 7160 Section 195 is in candidates
ra7160_195 = [c for c in raw_cands if "7160" in c.get('citation', '') and "195" in c.get('citation', '')]
print("=" * 80)
print(f"Is RA 7160 Section 195 in Top 25? Found {len(ra7160_195)} matches:")
for c in ra7160_195:
    print(f"  {c.get('citation')} | {c.get('title')}")

