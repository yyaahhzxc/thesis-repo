"""
generate_corpus_sample_figures.py
=================================
Generates publication-grade figures illustrating:
1. Lawphil Project statutory archive web interface and extraction flow
2. Formatted JSONL statutory record and structural section chunking with metadata prepending
3. Municipal ordinance scanning, OCR artifacts, and normalization flow
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_jsonl_and_chunking_figure(output_path):
    plt.rcParams['font.family'] = 'DejaVu Sans'
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.2), dpi=300)

    # -------------------------------------------------------------
    # Panel A: Formatted JSONL Extracted Record
    # -------------------------------------------------------------
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('(a) Standardized National Statutory JSONL Schema (Extracted Record)', fontsize=11, fontweight='bold', pad=10)

    json_box = patches.FancyBboxPatch((0.2, 0.3), 9.6, 9.2, boxstyle="round,pad=0.3",
                                      facecolor="#f8f9fa", edgecolor="#343a40", linewidth=1.5)
    ax1.add_patch(json_box)

    json_text = """{
  "statute_id": "RA_07160",
  "statute_type": "Republic Act",
  "statute_number": 7160,
  "title": "An Act Providing for a Local Government Code of 1991",
  "short_title": "Local Government Code of 1991",
  "date_approved": "1991-10-10",
  "source_repository": "The Lawphil Project (Arellano Law Foundation)",
  "total_sections": 536,
  "macro_domain": "Local Government & Public Administration",
  "sections": [
    {
      "section_id": "RA_07160_SEC_0016",
      "section_number": "Section 16",
      "section_title": "General Welfare",
      "text": "Every local government unit shall exercise the powers expressly
granted, those necessarily implied therefrom, as well as powers necessary,
appropriate, or incidental for its efficient and effective governance, and
those which are essential to the promotion of the general welfare...",
      "token_count": 184,
      "contains_penalty": false,
      "contains_proviso": true
    },
    ...
  ]
}"""
    ax1.text(0.5, 8.8, json_text, fontfamily='monospace', fontsize=8.5, verticalalignment='top', color='#212529')

    # -------------------------------------------------------------
    # Panel B: Structural Section Chunking & Context Prepending
    # -------------------------------------------------------------
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('(b) Operational Chunking with Structural Context Prepending', fontsize=11, fontweight='bold', pad=10)

    # Box 1: Raw Section
    b1 = patches.FancyBboxPatch((0.5, 6.8), 9.0, 2.5, boxstyle="round,pad=0.2",
                                facecolor="#e9ecef", edgecolor="#6c757d", linewidth=1.2)
    ax2.add_patch(b1)
    ax2.text(0.8, 8.9, "1. Raw Statutory Section (Isolated Provision):", fontsize=9.5, fontweight='bold', color='#495057')
    raw_snippet = "\"Section 16. General Welfare. — Every local government unit shall\nexercise the powers expressly granted, those necessarily implied...\""
    ax2.text(0.8, 8.3, raw_snippet, fontfamily='monospace', fontsize=8.2, color='#212529')
    ax2.text(0.8, 7.1, "[Risk: Lacks statute identity; keyword searches for 'RA 7160' fail on isolated text]", fontsize=8, fontstyle='italic', color='#c00000')

    # Arrow Down
    ax2.annotate('', xy=(5.0, 5.8), xytext=(5.0, 6.7),
                 arrowprops=dict(facecolor='#1f4e79', width=1.5, headwidth=7))
    ax2.text(5.3, 6.2, "Automated Structural Context Prepending Protocol", fontsize=8.5, fontweight='bold', color='#1f4e79')

    # Box 2: Prepended Provision (Model-Ready)
    b2 = patches.FancyBboxPatch((0.5, 1.0), 9.0, 4.6, boxstyle="round,pad=0.2",
                                facecolor="#e8f4f8", edgecolor="#1f4e79", linewidth=1.5)
    ax2.add_patch(b2)
    ax2.text(0.8, 5.2, "2. Model-Ready Prepended Unit (Fed into Stage 1 & Stage 2):", fontsize=9.5, fontweight='bold', color='#1f4e79')

    prepended_text = """[STATUTE: Republic Act No. 7160]
[TITLE: Local Government Code of 1991]
[DATE: 1991-10-10] [HIERARCHY: Primary Congressional Act]
[PROVISION: Section 16 - General Welfare]

Every local government unit shall exercise the powers expressly
granted, those necessarily implied therefrom, as well as powers
necessary, appropriate, or incidental for its efficient and effective
governance, and those which are essential to the promotion of the
general welfare. Within their respective territorial jurisdictions,
local government units shall ensure and support..."""

    ax2.text(0.8, 4.7, prepended_text, fontfamily='monospace', fontsize=8.2, verticalalignment='top', color='#0b3c5d')
    ax2.text(0.8, 1.3, "[Result: Captures exact citations, hierarchy rank, and substantive semantic intent]", fontsize=8, fontstyle='italic', color='#2e7d32')

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated: {output_path}")

def create_lawphil_and_scan_figure(output_path):
    plt.rcParams['font.family'] = 'DejaVu Sans'
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.8), dpi=300)

    # -------------------------------------------------------------
    # Panel A: Lawphil Repository Layout
    # -------------------------------------------------------------
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('(a) The Lawphil Project Web Extraction Interface & DOM Structure', fontsize=11, fontweight='bold', pad=10)

    browser_box = patches.FancyBboxPatch((0.2, 0.4), 9.6, 9.0, boxstyle="round,pad=0.2",
                                         facecolor="#ffffff", edgecolor="#1f4e79", linewidth=1.5)
    ax1.add_patch(browser_box)

    # Browser header bar
    header_bar = patches.Rectangle((0.2, 8.6), 9.6, 0.8, facecolor="#e9ecef", edgecolor="#1f4e79", linewidth=1.0)
    ax1.add_patch(header_bar)
    ax1.text(0.5, 9.0, "URL: https://lawphil.net/statutes/repacts/ra1991/ra_7160_1991.html", fontfamily='monospace', fontsize=8, color='#495057')

    # Web Content
    ax1.text(5.0, 8.1, "THE LAWPHIL PROJECT - PHILIPPINE LAWS AND JURISPRUDENCE", fontsize=8.5, fontweight='bold', ha='center', color='#1f4e79')
    ax1.text(5.0, 7.6, "ARELLANO LAW FOUNDATION", fontsize=8, fontstyle='italic', ha='center', color='#6c757d')
    ax1.axhline(y=7.4, xmin=0.08, xmax=0.92, color='#ced4da', linewidth=1)

    dom_text = """<CENTER>
  <B>REPUBLIC ACT NO. 7160</B><BR>
  <I>AN ACT PROVIDING FOR A LOCAL GOVERNMENT CODE OF 1991</I>
</CENTER>

<P><B>Be it enacted by the Senate and House of Representatives...</B></P>

<P><B>BOOK I: GENERAL PROVISIONS</B><BR>
<B>TITLE ONE: BASIC PRINCIPLES</B><BR>
<B>CHAPTER 1: The Code, Policy and Application</B></P>

<P><B>Section 1. Title.</B> — This Act shall be known and cited
as the "Local Government Code of 1991."</P>

<P><B>Section 2. Declaration of Policy.</B> — (a) It is hereby
declared the policy of the State that territorial and political
subdivisions shall enjoy genuine and meaningful local autonomy...</P>"""

    ax1.text(0.6, 7.1, dom_text, fontfamily='monospace', fontsize=7.2, verticalalignment='top', color='#212529')

    # Callout
    ax1.text(0.6, 0.8, "Uniform HTML <P> DOM structure enables robust section-level tag parsing without OCR degradation", fontsize=7.8, fontstyle='italic', color='#1f4e79')

    # -------------------------------------------------------------
    # Panel B: Local Municipal Ordinance PDF & OCR Noise
    # -------------------------------------------------------------
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('(b) Davao City Municipal Ordinance Archive: Scan Artifacts & OCR Noise', fontsize=11, fontweight='bold', pad=10)

    doc_box = patches.FancyBboxPatch((0.2, 0.4), 9.6, 9.0, boxstyle="round,pad=0.2",
                                     facecolor="#fffdf7", edgecolor="#856404", linewidth=1.5)
    ax2.add_patch(doc_box)

    # Document Header
    ax2.text(5.0, 8.8, "Republic of the Philippines", fontsize=8.5, ha='center', color='#333333')
    ax2.text(5.0, 8.4, "CITY OF DAVAO", fontsize=9.5, fontweight='bold', ha='center', color='#111111')
    ax2.text(5.0, 8.0, "Office of the Sangguniang Panlungsod", fontsize=8.5, fontstyle='italic', ha='center', color='#333333')

    # Seal representation
    seal_circle = patches.Circle((1.5, 8.4), 0.7, facecolor="#ffeeba", edgecolor="#856404", linewidth=1.2)
    ax2.add_patch(seal_circle)
    ax2.text(1.5, 8.4, "CITY SEAL\n(Stamp)", fontsize=6, ha='center', va='center', fontweight='bold', color='#856404')

    ord_text = """ORDINANCE NO. 0309-07, Series of 2007

AN ORDINANCE BANNING AERIAL SPRAYING AS AN AGRICULTURAL PRACTICE
BY ALL AGRICULTURAL ENTITIES IN DAVAO CITY

SECTION 1. Title. — This Ordinance shall be known as the "Banning of Aerial
Spraying in Davao City".

SECTION 2. Scope. — This Ordinance shall apply to all agricultural entities
operating within the territorial jurisdiction of Davao City.

SECTION 5. Prohibited Acts. — It shall be strictly prohibited for any person
or entity to conduct aerial spraying of agricultural chemicals within Davao City.

[OCR NOISE: 'prohihited', 'Dav@o C1ty', smudged line numbers, broken hyphens]
[ARTIFACTS: Physical ink bleed, off-axis rotation (3.2°), official signatures]"""

    ax2.text(0.6, 7.2, ord_text, fontfamily='monospace', fontsize=7.8, verticalalignment='top', color='#212529')

    # Contrast Callout
    ax2.text(0.6, 0.8, "Scanned legacy PDFs require OCR filtering; digital-born ex-ante drafts bypass OCR error cascade", fontsize=8, fontstyle='italic', color='#856404')

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated: {output_path}")

if __name__ == '__main__':
    p1 = os.path.join("CS_Undergraduate_Thesis_Template", "figs", "structured_jsonl_record_and_chunking.png")
    p2 = os.path.join("CS_Undergraduate_Thesis_Template", "figs", "lawphil_statutory_extraction_interface.png")
    create_jsonl_and_chunking_figure(p1)
    create_lawphil_and_scan_figure(p2)
