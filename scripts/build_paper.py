"""
build_paper.py
==============
One-click compilation script for the thesis LaTeX document.
Runs: pdflatex -> bibtex -> pdflatex (x2) to guarantee all citations,
figures, tables, and cross-references are 100% resolved.
"""

import os
import subprocess
import sys
import time

def extract_log_errors(log_path):
    if not os.path.exists(log_path):
        return []
    errors = []
    try:
        with open(log_path, 'r', encoding='latin1', errors='ignore') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith('! '):
                context = [line.strip()]
                for follow in lines[i+1:i+6]:
                    if follow.strip() and not follow.startswith('! '):
                        context.append('    ' + follow.strip())
                    elif follow.startswith('! '):
                        break
                errors.append('\n'.join(context))
    except Exception as e:
        errors.append(f"Could not read log file: {e}")
    return errors

def compile_thesis(template_dir="CS_Undergraduate_Thesis_Template", main_file="main.tex", fast=False):
    # If template_dir is relative, make it relative to repository root or check current dir
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isabs(template_dir):
        candidate_repo = os.path.join(repo_root, template_dir)
        if os.path.exists(candidate_repo):
            template_dir = candidate_repo
        elif not os.path.exists(template_dir):
            # If current working directory is already template_dir
            if os.path.exists(main_file):
                template_dir = os.getcwd()
            else:
                print(f"Error: Directory '{template_dir}' not found.")
                return False
        else:
            template_dir = os.path.abspath(template_dir)
        
    start_time = time.time()
    pdf_path = os.path.join(template_dir, main_file.replace(".tex", ".pdf"))
    log_path = os.path.join(template_dir, main_file.replace(".tex", ".log"))
    
    print(f"=== Compiling Thesis LaTeX Document ({main_file}) {'[FAST MODE]' if fast else '[FULL 4-PASS MODE]'} ===")
    cmd_pdf = ["pdflatex", "-synctex=1", "-interaction=nonstopmode", "-enable-installer", main_file]
    
    if fast:
        print("\n[Fast Pass] Running single-pass pdflatex for quick update...")
        res = subprocess.run(cmd_pdf, cwd=template_dir, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"\n[!] pdflatex returned non-zero exit code ({res.returncode}).")
            errs = extract_log_errors(log_path)
            if errs:
                print("--- Top LaTeX Errors Detected ---")
                for err in errs[:5]:
                    print(err)
            return False
    else:
        # Step 1: First pdflatex pass
        print("\n[Pass 1/4] Running initial pdflatex...")
        res1 = subprocess.run(cmd_pdf, cwd=template_dir, capture_output=True, text=True)
        if res1.returncode != 0:
            print(f"\n[!] Initial pdflatex pass failed with exit code {res1.returncode}.")
            errs = extract_log_errors(log_path)
            for err in errs[:5]:
                print(err)
            return False
            
        # Step 2: BibTeX for citations
        print("[Pass 2/4] Running bibtex for references...")
        cmd_bib = ["bibtex", main_file.replace(".tex", "")]
        res_bib = subprocess.run(cmd_bib, cwd=template_dir, capture_output=True, text=True)
        if res_bib.returncode != 0:
            print(f"\n[!] BibTeX warning/error (exit code {res_bib.returncode}). Check bibtex logs if citations are missing.")
            
        # Step 3: Second pdflatex pass
        print("[Pass 3/4] Running second pdflatex pass...")
        subprocess.run(cmd_pdf, cwd=template_dir, capture_output=True, text=True)
        
        # Step 4: Final pdflatex pass for cross-references
        print("[Pass 4/4] Running final pdflatex pass for TOC/Figures...")
        res_final = subprocess.run(cmd_pdf, cwd=template_dir, capture_output=True, text=True)
        if res_final.returncode != 0:
            print(f"\n[!] Final pdflatex pass failed with exit code {res_final.returncode}.")
            errs = extract_log_errors(log_path)
            for err in errs[:5]:
                print(err)
            return False
    
    if os.path.exists(pdf_path) and os.path.getmtime(pdf_path) >= start_time - 5:
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"\nSUCCESS! Thesis PDF compiled and updated successfully:")
        print(f"  Path: {os.path.abspath(pdf_path)}")
        print(f"  Size: {size_kb:.1f} KB")
        return True
    else:
        print("\nCompilation failed or output PDF was not updated. Check main.log for errors.")
        errs = extract_log_errors(log_path)
        for err in errs[:5]:
            print(err)
        return False

if __name__ == "__main__":
    is_fast = "--fast" in sys.argv or "-f" in sys.argv
    compile_thesis(fast=is_fast)
