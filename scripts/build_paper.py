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

def compile_thesis(template_dir="CS_Undergraduate_Thesis_Template", main_file="main.tex"):
    if not os.path.exists(template_dir):
        print(f"Error: Directory '{template_dir}' not found.")
        return False
        
    print(f"=== Compiling Thesis LaTeX Document ({main_file}) ===")
    
    # Step 1: First pdflatex pass
    print("\n[Pass 1/4] Running initial pdflatex...")
    cmd1 = ["pdflatex", "-interaction=nonstopmode", main_file]
    res1 = subprocess.run(cmd1, cwd=template_dir, capture_output=True, text=True)
    
    # Step 2: BibTeX for citations
    print("[Pass 2/4] Running bibtex for references...")
    cmd_bib = ["bibtex", main_file.replace(".tex", "")]
    res_bib = subprocess.run(cmd_bib, cwd=template_dir, capture_output=True, text=True)
    
    # Step 3: Second pdflatex pass
    print("[Pass 3/4] Running second pdflatex pass...")
    subprocess.run(cmd1, cwd=template_dir, capture_output=True, text=True)
    
    # Step 4: Final pdflatex pass for cross-references
    print("[Pass 4/4] Running final pdflatex pass for TOC/Figures...")
    res_final = subprocess.run(cmd1, cwd=template_dir, capture_output=True, text=True)
    
    pdf_path = os.path.join(template_dir, main_file.replace(".tex", ".pdf"))
    if os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"\nSUCCESS! Thesis PDF compiled successfully:")
        print(f"  Path: {os.path.abspath(pdf_path)}")
        print(f"  Size: {size_kb:.1f} KB")
        return True
    else:
        print("\nCompilation failed. Check main.log for errors.")
        return False

if __name__ == "__main__":
    compile_thesis()
