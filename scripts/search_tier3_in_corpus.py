import json
from pathlib import Path

targets = ['0309-07', '092-2000', '158-05', '0310-07', '0367-12', '0270-23', '3353', '7783', '210', 'GSIS', 'aerial', 'smoking', 'speed', 'watershed', 'revenue']
found = {}

print("--- Searching in corpus/city_ordinances/categorized_davao_ordinances.jsonl ---")
with open('corpus/city_ordinances/categorized_davao_ordinances.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if not line.strip(): continue
        d = json.loads(line)
        title = d.get('title', '')
        ord_no = d.get('ordinance_no', '')
        text = d.get('text', '') or d.get('body', '') or ''
        for t in targets:
            if t.lower() in ord_no.lower() or t.lower() in title.lower():
                if t not in found:
                    found[t] = []
                found[t].append({
                    'ordinance_no': ord_no,
                    'title': title[:75],
                    'text_len': len(text),
                    'sections': len(d.get('sections', []))
                })

for t, matches in found.items():
    print(f"\nTarget: {t} ({len(matches)} matches)")
    for m in matches[:3]:
        print(f"  No: {m['ordinance_no']} | Title: {m['title']} | Len: {m['text_len']} | Secs: {m['sections']}")

