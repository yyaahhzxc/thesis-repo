import json

targets = [
    ('Davao Ord 0309-07', ['0309', '309']),
    ('PD 1144', ['1144']),
    ('Davao Ord 092-2000', ['092', '92']),
    ('RA 7160', ['7160']),
    ('PD 1096', ['1096']),
    ('Davao Ord 0158-05', ['0158', '158']),
    ('Davao Ord 0325-15', ['0325', '325']),
    ('RA 7942', ['7942']),
    ('Davao Ord 0367-12', ['0367', '367']),
    ('RA 9211', ['9211']),
    ('Davao Ord 0270-23', ['0270', '270']),
    ('RA 4136', ['4136']),
    ('CDO Ord 3375-93', ['3375']),
    ('PD 1869', ['1869']),
    ('Manila Ord 7783', ['7783']),
    ('Constitution', ['constitution'])
]

found = {}
with open('data/knowledge_graph/statutory_kg_nodes.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        node = json.loads(line)
        nid = node.get('id', '').lower()
        num = node.get('number', '').lower()
        title = node.get('title', '').lower()
        for label, keys in targets:
            if any(k in nid or k in num for k in keys):
                if node.get('node_type') == 'enactment':
                    if label not in found:
                        found[label] = []
                    found[label].append({
                        'id': node.get('id'),
                        'jurisdiction': node.get('jurisdiction'),
                        'number': node.get('number'),
                        'domain': node.get('domain'),
                        'title': (node.get('title') or '')[:80]
                    })

for label, items in found.items():
    print(f"=== {label} (matches: {len(items)}) ===")
    for item in items[:5]:
        print(f"  ID: {item['id']} | Jur: {item['jurisdiction']} | Num: {item['number']} | Domain: {item['domain']}")

