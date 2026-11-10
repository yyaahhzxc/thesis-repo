import json

with open("data/unified_dual_statutory_provisions.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        doc = data.get("document_id", "")
        prov = data.get("provision_id", "")
        text = data.get("text", "")
        if "0310" in doc or "watershed" in doc.lower() or "0310-07" in text:
            print(f"Match line {i}: doc={doc} | prov={prov} | text={text[:100]}")
            break
print("Search complete.")

