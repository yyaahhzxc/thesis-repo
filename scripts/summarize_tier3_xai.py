import json, re

def extract_tokens(html_str):
    if not html_str:
        return []
    pattern = re.compile(r'data-weight="([0-9.]+)"[^>]*>([^<]+)</span>')
    matches = pattern.findall(html_str)
    items = [(float(w), text.strip()) for w, text in matches if text.strip()]
    items.sort(key=lambda x: x[0], reverse=True)
    return items[:5]

files_to_check = [
    ('output/tier3_demo_full_audit_results.json', ['DAVAO-TIER3-01', 'DAVAO-TIER3-02']),
    ('output/tier3_demo_full_audit_results_05_10.json', ['DAVAO-TIER3-05', 'DAVAO-TIER3-06', 'DAVAO-TIER3-07', 'DAVAO-TIER3-08', 'SC-PHIL-09', 'SC-PHIL-10'])
]

with open('output/tier3_xai_saliency_summary.txt', 'w', encoding='utf-8') as out:
    for json_file, cases in files_to_check:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for case_id in cases:
            if case_id not in data:
                continue
            audit = data[case_id].get('audit', {})
            out.write('='*80 + '\n')
            out.write(f"CASE: {case_id} | Document: {audit.get('document_name')}\n")
            out.write('='*80 + '\n')
            flagged = 0
            for s in audit.get('sections', []):
                if s.get('verdict') == 'CONTRADICTION':
                    flagged += 1
                    tc = s.get('top_candidate', {})
                    num = s.get('sec_num')
                    title = s.get('sec_title')
                    conf = s.get('confidence_percentage')
                    target = tc.get('citation')
                    ord_tokens = extract_tokens(s.get('ordinance_html'))
                    stat_tokens = extract_tokens(s.get('statute_html'))
                    out.write(f"\n[FLAGGED] Sec {num}: {title} | Confidence: {conf}%\n")
                    out.write(f"   Target Statute : {target}\n")
                    out.write(f"   Top Draft Attn  : {ord_tokens}\n")
                    out.write(f"   Top Statute Attn: {stat_tokens}\n")
            out.write(f"\nTotal Flagged Sections: {flagged}\n\n")

print("Generated output/tier3_xai_saliency_summary.txt successfully.")

