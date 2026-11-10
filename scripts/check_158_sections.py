import json

with open('corpus/city_ordinances/categorized_davao_ordinances.jsonl', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if idx + 1 == 1613:
            d = json.loads(line)
            secs = d.get('sections', [])
            print(f"Total sections: {len(secs)}")
            empty_secs = [s for s in secs if not s.get('raw_text', '').strip()]
            print(f"Sections with empty raw_text: {len(empty_secs)}")
            if empty_secs:
                print("Sample empty sections:")
                for es in empty_secs[:5]:
                    print(f"  {es.get('section_marker')}: {es.get('section_title')}")
            break

