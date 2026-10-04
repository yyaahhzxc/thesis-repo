import os
import glob
import re
import json
import pypdf
import warnings
warnings.filterwarnings('ignore')

# 1. Parse main.bbl to map citekeys to citation numbers
with open('CS_Undergraduate_Thesis_Template/main.bbl', 'r', encoding='utf-8', errors='ignore') as f:
    bbl = f.read()

bbl_entries = re.findall(r'\\bibitem(?:\[([^\]]*)\])?\{([^}]+)\}', bbl)
key_to_num = {}
for idx, (num, key) in enumerate(bbl_entries, 1):
    c_num = num if num else str(idx)
    key_to_num[key.strip()] = c_num

print(f"Total entries in main.bbl: {len(key_to_num)}")

# 2. Map citations to LaTeX chapters
tex_files = {
    'Introduction': 'CS_Undergraduate_Thesis_Template/chapters/introduction.tex',
    'Literature Review': 'CS_Undergraduate_Thesis_Template/chapters/literature_review.tex',
    'Methodology': 'CS_Undergraduate_Thesis_Template/chapters/methodology.tex',
    'Results & Discussion': 'CS_Undergraduate_Thesis_Template/chapters/results_and_discussion.tex'
}

tex_claims = {}
for chap, fpath in tex_files.items():
    if not os.path.exists(fpath): continue
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Split by sentences or paragraphs
    paras = content.split('\n\n')
    for p in paras:
        p_clean = ' '.join(p.strip().split())
        if not p_clean or p_clean.startswith('%'): continue
        
        for m in re.finditer(r'\\cite[a-z]*\{([^}]+)\}', p_clean):
            keys = [k.strip() for k in m.group(1).split(',')]
            for k in keys:
                tex_claims.setdefault(k, []).append({
                    'chapter': chap,
                    'file': os.path.basename(fpath),
                    'paragraph': p_clean
                })

# 3. Check against local PDFs
audit_results = []
pdf_dir = 'docs/references'

for key, c_num in key_to_num.items():
    pdf_path = os.path.join(pdf_dir, f"{key}.pdf")
    if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) < 500:
        continue
    
    cites = tex_claims.get(key, [])
    if not cites:
        continue
    
    # Extract PDF text (first 10 pages)
    pdf_text = ""
    try:
        reader = pypdf.PdfReader(pdf_path)
        for page in reader.pages[:10]:
            t = page.extract_text()
            if t: pdf_text += t + " "
    except Exception as e:
        pdf_text = f"ERROR: {e}"
        
    pdf_text_lower = pdf_text.lower()
    
    # Analyze each citation instance
    for c in cites:
        para = c['paragraph']
        # Extract potential numbers or specific terms
        # Clean latex commands
        clean_para = re.sub(r'\\[a-zA-Z]+(\[[^\]]*\])?(\{([^}]*)\})?', r'\3', para)
        clean_para = re.sub(r'[\{\}\$]', '', clean_para)
        
        # Find numbers
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', clean_para)
        
        # Check if numbers exist in PDF
        num_checks = []
        for n in numbers:
            # ignore single digit 1, 2, 3 if very common
            if len(n) > 1 or '.' in n:
                found_in_pdf = n in pdf_text
                num_checks.append({'number': n, 'in_pdf': found_in_pdf})
        
        audit_results.append({
            'citation_num': c_num,
            'citekey': key,
            'chapter': c['chapter'],
            'paragraph': clean_para,
            'numbers': num_checks,
            'pdf_path': pdf_path,
            'pdf_len': len(pdf_text)
        })

print(f"Audited {len(audit_results)} citation instances across {len(set(r['citekey'] for r in audit_results))} unique keys with local PDFs.")

with open('scratch/full_audit_results.json', 'w', encoding='utf-8') as f:
    json.dump(audit_results, f, indent=2)

print("Saved scratch/full_audit_results.json")
