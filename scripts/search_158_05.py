import json
import os
from pathlib import Path

def search_corpus_for_158_05():
    paths_to_check = [
        "corpus/city_ordinances/categorized_davao_ordinances.jsonl",
        "data/unified_dual_statutory_provisions.jsonl",
    ]
    for p in paths_to_check:
        if not os.path.exists(p): continue
        print(f"Scanning {p}...")
        with open(p, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                if "158-05" in line or "158 - 05" in line or "158-2005" in line or "Revenue Code of the City of Davao" in line:
                    try:
                        d = json.loads(line)
                        ord_id = d.get("ordinance_id") or d.get("id") or d.get("ordinance_number") or d.get("citation")
                        title = d.get("title", "")
                        secs = len(d.get("sections", []))
                        print(f"  [Found Line {idx+1}] ID: {ord_id} | Title: {title[:80]} | Secs: {secs}")
                    except Exception as e:
                        print(f"  [Found text on Line {idx+1}] Length: {len(line)}")

if __name__ == "__main__":
    search_corpus_for_158_05()

