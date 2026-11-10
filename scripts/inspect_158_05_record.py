import json

with open('corpus/city_ordinances/categorized_davao_ordinances.jsonl', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if idx + 1 == 1613:
            d = json.loads(line)
            print("Ordinance ID:", d.get('ordinance_id'))
            print("Title:", d.get('title'))
            print("Total sections:", len(d.get('sections', [])))
            print("Word count:", d.get('word_count'))
            secs = d.get('sections', [])
            print("\nFirst 5 sections:")
            for s in secs[:5]:
                print(f"  {s.get('section_marker')}: {s.get('section_title')}")
            print("\nSample target sections (69, 135, 423):")
            for s in secs:
                m = str(s.get('section_marker', ''))
                t = str(s.get('section_title', ''))
                if any(k in m for k in ['69', '135', '423']):
                    txt = s.get('raw_text', '')
                    print(f"  [TARGET] {m}: {t} | text_len={len(txt)} | words={len(txt.split())}")
                    print(f"    Snippet: {txt[:120]}...\n")
            break

