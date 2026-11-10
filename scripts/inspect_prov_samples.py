import json

with open("data/unified_dual_statutory_provisions.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        if "0310-07" in line:
            d = json.loads(line)
            print("0310-07 item:", d.get("citation"), "| Title:", d.get("title", "")[:60], "| Keys:", list(d.keys()))
            print("  Text snippet:", d.get("text", "")[:100])
            break

with open("data/unified_dual_statutory_provisions.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        if "7783" in line and ("Manila" in line or "motel" in line or "Laguio" in line or "7783" in line):
            d = json.loads(line)
            print("\n7783 item:", d.get("citation"), "| Title:", d.get("title", "")[:60])
            print("  Text snippet:", d.get("text", "")[:100])
            break

