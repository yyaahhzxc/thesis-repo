"""
scripts/generate_lofi_wireframes_svg.py
======================================
Generates an editable, clean Low-Fidelity SVG Wireframe of the
Ex-Ante Davao City Ordinance Conflict Detection System.

Contains two complete artboard frames side-by-side:
1. Frame 1: Document Upload & Benchmark Case Selector (Landing View)
2. Frame 2: Unified Master-Detail Conflict Audit Dashboard (Results View)

Designed specifically for 1-click drag-and-drop into Figma:
- All layers grouped semantically with clean IDs (`<g id="...">`)
- Pure SVG shapes (rectangles, crossed-X placeholder boxes, badges, sliders, text layers)
- Standard wireframe typography and grayscale palette with subtle alert accents.
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "wireframes"
STATIC_DIR = REPO_ROOT / "demo" / "static" / "wireframes"
SVG_FILE = OUTPUT_DIR / "conflict_detection_lofi_wireframe.svg"


def create_x_placeholder(x, y, w, h, label="IMAGE / ICON", bg="#F3F4F6", stroke="#D1D5DB", text_color="#9CA3AF"):
    """Generates a classic wireframe placeholder box with diagonal X lines and a centered label."""
    return f"""
      <g class="placeholder-box">
        <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{bg}" stroke="{stroke}" stroke-width="1.5"/>
        <line x1="{x}" y1="{y}" x2="{x+w}" y2="{y+h}" stroke="{stroke}" stroke-width="1.2" stroke-dasharray="4,4"/>
        <line x1="{x+w}" y1="{y}" x2="{x}" y2="{y+h}" stroke="{stroke}" stroke-width="1.2" stroke-dasharray="4,4"/>
        <rect x="{x + w//2 - 50}" y="{y + h//2 - 12}" width="100" height="24" rx="4" fill="#FFFFFF" opacity="0.9"/>
        <text x="{x + w//2}" y="{y + h//2 + 4}" font-size="11" font-weight="600" fill="{text_color}" text-anchor="middle" font-family="Inter, system-ui, sans-serif">{label}</text>
      </g>"""


def build_svg():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

    # Canvas Dimensions: 2 screens side-by-side (1400w each + 80px gap + 60px padding)
    canvas_w = 2960
    canvas_h = 1380

    svg = []
    svg.append(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}">
  <defs>
    <style>
      .bg-canvas {{ fill: #E5E7EB; }}
      .artboard-bg {{ fill: #F9FAFB; stroke: #9CA3AF; stroke-width: 2; }}
      .card-bg {{ fill: #FFFFFF; stroke: #E5E7EB; stroke-width: 1.5; }}
      .card-alt {{ fill: #F3F4F6; stroke: #D1D5DB; stroke-width: 1.5; }}
      .border-dashed {{ stroke-dasharray: 6,6; }}
      .text-title {{ font-family: Inter, -apple-system, system-ui, sans-serif; font-weight: 700; fill: #111827; }}
      .text-subtitle {{ font-family: Inter, -apple-system, system-ui, sans-serif; font-weight: 500; fill: #4B5563; }}
      .text-muted {{ font-family: Inter, -apple-system, system-ui, sans-serif; font-weight: 400; fill: #6B7280; }}
      .text-code {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; }}
    </style>
  </defs>

  <!-- Canvas Background -->
  <rect width="{canvas_w}" height="{canvas_h}" class="bg-canvas" />
""")

    # =========================================================================
    # SCREEN 1: UPLOAD & LANDING VIEW (X: 40, Y: 40, W: 1400, H: 1280)
    # =========================================================================
    s1_x = 40
    s1_y = 40
    s1_w = 1400
    s1_h = 1300

    svg.append(f"""
  <!-- ======================================================================= -->
  <!-- SCREEN 1: UPLOAD & BENCHMARK CASE LANDING VIEW                          -->
  <!-- ======================================================================= -->
  <g id="Screen-1-Upload-Landing">
    <!-- Artboard Frame -->
    <rect x="{s1_x}" y="{s1_y}" width="{s1_w}" height="{s1_h}" rx="12" class="artboard-bg" />

    <!-- Screen Title Annotation -->
    <text x="{s1_x + 30}" y="{s1_y - 12}" font-size="16" font-weight="700" fill="#374151" font-family="Inter, sans-serif">SCREEN 1: LANDING &amp; ORDINANCE INGESTION VIEW (LO-FI WIREFRAME)</text>

    <!-- Top App Navigation Bar -->
    <g id="S1-Navbar">
      <rect x="{s1_x}" y="{s1_y}" width="{s1_w}" height="70" rx="12" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="1.5"/>
      <!-- Brand Logo Placeholder -->
      <rect x="{s1_x + 30}" y="{s1_y + 15}" width="40" height="40" rx="8" fill="#E5E7EB" stroke="#D1D5DB" stroke-width="1.5"/>
      <text x="{s1_x + 50}" y="{s1_y + 40}" font-size="14" font-weight="700" fill="#4B5563" text-anchor="middle" font-family="Inter, sans-serif">ADDU</text>

      <!-- App Title -->
      <text x="{s1_x + 85}" y="{s1_y + 36}" font-size="16" font-weight="700" fill="#111827" font-family="Inter, sans-serif">EX-ANTE DAVAO ORDINANCE CONFLICT DETECTOR</text>
      <text x="{s1_x + 85}" y="{s1_y + 52}" font-size="11" font-weight="500" fill="#6B7280" font-family="Inter, sans-serif">Coarse-to-Fine Dual Retrieval &amp; NLI Preemption Triage (CS Undergraduate Thesis)</text>

      <!-- Status Chips (Top Right) -->
      <rect x="{s1_x + s1_w - 480}" y="{s1_y + 20}" width="210" height="30" rx="6" fill="#F3F4F6" stroke="#D1D5DB"/>
      <circle cx="{s1_x + s1_w - 465}" cy="{s1_y + 35}" r="5" fill="#16A34A"/>
      <text x="{s1_x + s1_w - 450}" y="{s1_y + 39}" font-size="11" font-weight="600" fill="#374151" font-family="Inter, sans-serif">Local PyTorch CPU Engine: ONLINE</text>

      <rect x="{s1_x + s1_w - 250}" y="{s1_y + 20}" width="220" height="30" rx="6" fill="#F3F4F6" stroke="#D1D5DB"/>
      <text x="{s1_x + s1_w - 235}" y="{s1_y + 39}" font-size="11" font-weight="600" fill="#4B5563" font-family="Inter, sans-serif">176,421 Statutory Provisions</text>
    </g>

    <!-- Main Hero Header -->
    <g id="S1-Hero-Section">
      <text x="{s1_x + s1_w//2}" y="{s1_y + 130}" font-size="28" font-weight="800" fill="#111827" text-anchor="middle" font-family="Inter, sans-serif">Ex-Ante Legal Conflict Detection Engine</text>
      <text x="{s1_x + s1_w//2}" y="{s1_y + 160}" font-size="14" font-weight="400" fill="#4B5563" text-anchor="middle" font-family="Inter, sans-serif">Automated statutory preemption and intra-jurisdictional consistency audit for proposed Davao City local ordinances</text>
    </g>

    <!-- Primary Upload Box (Drag and Drop) -->
    <g id="S1-Upload-Box">
      <rect x="{s1_x + 150}" y="{s1_y + 195}" width="{s1_w - 300}" height="320" rx="12" fill="#FFFFFF" stroke="#9CA3AF" stroke-width="2" class="border-dashed" />
      
      <!-- Upload Cloud / Folder Placeholder -->
      <g transform="translate({s1_x + s1_w//2 - 35}, {s1_y + 235})">
        <rect width="70" height="60" rx="8" fill="#F3F4F6" stroke="#D1D5DB" stroke-width="1.5"/>
        <line x1="0" y1="0" x2="70" y2="60" stroke="#D1D5DB" stroke-width="1.5"/>
        <line x1="70" y1="0" x2="0" y2="60" stroke="#D1D5DB" stroke-width="1.5"/>
        <text x="35" y="35" font-size="10" font-weight="700" fill="#9CA3AF" text-anchor="middle" font-family="Inter, sans-serif">UPLOAD</text>
      </g>

      <text x="{s1_x + s1_w//2}" y="{s1_y + 335}" font-size="18" font-weight="700" fill="#111827" text-anchor="middle" font-family="Inter, sans-serif">Drag &amp; Drop Draft Ordinance PDF Here</text>
      <text x="{s1_x + s1_w//2}" y="{s1_y + 360}" font-size="13" font-weight="400" fill="#6B7280" text-anchor="middle" font-family="Inter, sans-serif">Supports searchable PDF, scanned OCR pages, or plaintext draft (.pdf, .txt, .json)</text>

      <!-- Browse Button -->
      <rect x="{s1_x + s1_w//2 - 90}" y="{s1_y + 385}" width="180" height="42" rx="8" fill="#111827" />
      <text x="{s1_x + s1_w//2}" y="{s1_y + 411}" font-size="13" font-weight="600" fill="#FFFFFF" text-anchor="middle" font-family="Inter, sans-serif">Browse Local Files</text>

      <!-- Micro metadata hints -->
      <text x="{s1_x + s1_w//2}" y="{s1_y + 455}" font-size="11" font-weight="500" fill="#9CA3AF" text-anchor="middle" font-family="Inter, sans-serif">OCR Preprocessing &bull; Hierarchical Enactment-Section Prepending &bull; Token Compliance Filter</text>
      <text x="{s1_x + s1_w//2}" y="{s1_y + 475}" font-size="11" font-weight="500" fill="#9CA3AF" text-anchor="middle" font-family="Inter, sans-serif">Target: Sangguniang Panlungsod Legislative Drafting Workflow</text>
    </g>

    <!-- Divider with OR label -->
    <g id="S1-Divider">
      <line x1="{s1_x + 150}" y1="{s1_y + 555}" x2="{s1_x + s1_w//2 - 40}" y2="{s1_y + 555}" stroke="#D1D5DB" stroke-width="1.5"/>
      <text x="{s1_x + s1_w//2}" y="{s1_y + 560}" font-size="12" font-weight="700" fill="#9CA3AF" text-anchor="middle" font-family="Inter, sans-serif">OR QUICK LOAD BENCHMARK CASES</text>
      <line x1="{s1_x + s1_w//2 + 40}" y1="{s1_y + 555}" x2="{s1_x + s1_w - 150}" y2="{s1_y + 555}" stroke="#D1D5DB" stroke-width="1.5"/>
    </g>

    <!-- Benchmark Test Cases Preset Cards (2x2 Grid) -->
    <g id="S1-Preset-Cards">
      <!-- Preset 1: Aerial Spraying (Magtajas Landmark) -->
      <g transform="translate({s1_x + 150}, {s1_y + 590})">
        <rect width="530" height="95" rx="8" class="card-bg"/>
        <rect x="15" y="15" width="28" height="28" rx="6" fill="#FEE2E2" stroke="#EF4444"/>
        <text x="29" y="34" font-size="12" font-weight="800" fill="#DC2626" text-anchor="middle">!</text>
        <text x="55" y="32" font-size="14" font-weight="700" fill="#111827" font-family="Inter, sans-serif">Ordinance No. 0309-07 (Aerial Spraying Ban)</text>
        <text x="55" y="52" font-size="12" font-weight="400" fill="#4B5563" font-family="Inter, sans-serif">Vertical Preemption Conflict vs PD 1144 §6 (Fertilizer &amp; Pesticide Authority)</text>
        <text x="55" y="72" font-size="11" font-weight="600" fill="#DC2626" font-family="Inter, sans-serif">Known Ground Truth: CONFLICT (Mosqueda v. Davao City)</text>
        <rect x="420" y="30" width="95" height="34" rx="6" fill="#F3F4F6" stroke="#D1D5DB"/>
        <text x="467" y="52" font-size="12" font-weight="600" fill="#111827" text-anchor="middle" font-family="Inter, sans-serif">Load Case →</text>
      </g>

      <!-- Preset 2: Billboard & Signage Regulation -->
      <g transform="translate({s1_x + 720}, {s1_y + 590})">
        <rect width="530" height="95" rx="8" class="card-bg"/>
        <rect x="15" y="15" width="28" height="28" rx="6" fill="#FEE2E2" stroke="#EF4444"/>
        <text x="29" y="34" font-size="12" font-weight="800" fill="#DC2626" text-anchor="middle">!</text>
        <text x="55" y="32" font-size="14" font-weight="700" fill="#111827" font-family="Inter, sans-serif">Ordinance No. 092-2000 (Signage &amp; Billboards)</text>
        <text x="55" y="52" font-size="12" font-weight="400" fill="#4B5563" font-family="Inter, sans-serif">Vertical Conflict vs PD 1096 National Building Code setback mandates</text>
        <text x="55" y="72" font-size="11" font-weight="600" fill="#DC2626" font-family="Inter, sans-serif">Known Ground Truth: CONFLICT (DPWH v. City of Davao)</text>
        <rect x="420" y="30" width="95" height="34" rx="6" fill="#F3F4F6" stroke="#D1D5DB"/>
        <text x="467" y="52" font-size="12" font-weight="600" fill="#111827" text-anchor="middle" font-family="Inter, sans-serif">Load Case →</text>
      </g>

      <!-- Preset 3: Tier 2 Synthetic Draft #1 (Clean Air & Anti-Smoking) -->
      <g transform="translate({s1_x + 150}, {s1_y + 705})">
        <rect width="530" height="95" rx="8" class="card-bg"/>
        <rect x="15" y="15" width="28" height="28" rx="6" fill="#FEF3C7" stroke="#F59E0B"/>
        <text x="29" y="34" font-size="12" font-weight="800" fill="#B45309" text-anchor="middle">§</text>
        <text x="55" y="32" font-size="14" font-weight="700" fill="#111827" font-family="Inter, sans-serif">DRAFT-ORD-2026-02.pdf (Clean Air &amp; Anti-Smoking)</text>
        <text x="55" y="52" font-size="12" font-weight="400" fill="#4B5563" font-family="Inter, sans-serif">Multi-Section Document: 15 Operative Sections (2 Flagged Conflicts)</text>
        <text x="55" y="72" font-size="11" font-weight="600" fill="#B45309" font-family="Inter, sans-serif">Tier 2 Benchmark Test Set (Full PDF Ingestion)</text>
        <rect x="420" y="30" width="95" height="34" rx="6" fill="#F3F4F6" stroke="#D1D5DB"/>
        <text x="467" y="52" font-size="12" font-weight="600" fill="#111827" text-anchor="middle" font-family="Inter, sans-serif">Test PDF →</text>
      </g>

      <!-- Preset 4: Tier 2 Synthetic Draft #2 (Harmonious Ordinance) -->
      <g transform="translate({s1_x + 720}, {s1_y + 705})">
        <rect width="530" height="95" rx="8" class="card-bg"/>
        <rect x="15" y="15" width="28" height="28" rx="6" fill="#DCFCE7" stroke="#16A34A"/>
        <text x="29" y="34" font-size="12" font-weight="800" fill="#16A34A" text-anchor="middle">✓</text>
        <text x="55" y="32" font-size="14" font-weight="700" fill="#111827" font-family="Inter, sans-serif">DRAFT-ORD-2026-04.pdf (Barangay Health Devolution)</text>
        <text x="55" y="52" font-size="12" font-weight="400" fill="#4B5563" font-family="Inter, sans-serif">Multi-Section Document: 12 Operative Sections (0 Conflicts)</text>
        <text x="55" y="72" font-size="11" font-weight="600" fill="#16A34A" font-family="Inter, sans-serif">Known Ground Truth: STATUTORILY COMPLIANT (RA 7160 §17)</text>
        <rect x="420" y="30" width="95" height="34" rx="6" fill="#F3F4F6" stroke="#D1D5DB"/>
        <text x="467" y="52" font-size="12" font-weight="600" fill="#111827" text-anchor="middle" font-family="Inter, sans-serif">Test PDF →</text>
      </g>
    </g>

    <!-- Architecture & Pipeline Flow Card (Bottom) -->
    <g id="S1-Pipeline-Architecture" transform="translate({s1_x + 150}, {s1_y + 830})">
      <rect width="{s1_w - 300}" height="410" rx="10" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="1.5"/>
      <text x="30" y="35" font-size="15" font-weight="700" fill="#111827" font-family="Inter, sans-serif">Two-Stage Coarse-to-Fine Pipeline Specifications (Chapter 3 Methodology)</text>

      <!-- 3 Flow Step Cards -->
      <!-- Step 1 -->
      <g transform="translate(30, 60)">
        <rect width="320" height="150" rx="8" fill="#F9FAFB" stroke="#D1D5DB"/>
        <text x="20" y="30" font-size="13" font-weight="700" fill="#111827">1. Ingestion &amp; Parsing</text>
        <text x="20" y="52" font-size="11" font-weight="400" fill="#4B5563">• Regex structural sectioning</text>
        <text x="20" y="70" font-size="11" font-weight="400" fill="#4B5563">• Hierarchical enactment prepending</text>
        <text x="20" y="88" font-size="11" font-weight="400" fill="#4B5563">• 512-token truncation compliance</text>
        <text x="20" y="106" font-size="11" font-weight="400" fill="#4B5563">• 6-class typology classification</text>
        <rect x="20" y="120" width="130" height="20" rx="4" fill="#E5E7EB"/>
        <text x="85" y="134" font-size="10" font-weight="600" fill="#374151" text-anchor="middle">Input: Draft Ordinance</text>
      </g>

      <!-- Step 2 -->
      <g transform="translate(380, 60)">
        <rect width="330" height="150" rx="8" fill="#F9FAFB" stroke="#D1D5DB"/>
        <text x="20" y="30" font-size="13" font-weight="700" fill="#111827">2. Stage 1 Hybrid Retrieval</text>
        <text x="20" y="52" font-size="11" font-weight="400" fill="#4B5563">• Dense: all-MiniLM-L6-v2 (384-d)</text>
        <text x="20" y="70" font-size="11" font-weight="400" fill="#4B5563">• Sparse: BM25 Okapi (k1=1.5, b=0.75)</text>
        <text x="20" y="88" font-size="11" font-weight="400" fill="#4B5563">• alpha = 0.50 score fusion</text>
        <text x="20" y="106" font-size="11" font-weight="400" fill="#4B5563">• Pool: 176,421 dual provisions</text>
        <rect x="20" y="120" width="150" height="20" rx="4" fill="#DBEAFE"/>
        <text x="95" y="134" font-size="10" font-weight="600" fill="#1D4ED8" text-anchor="middle">Top-50 Candidate Buffer</text>
      </g>

      <!-- Step 3 -->
      <g transform="translate(740, 60)">
        <rect width="330" height="150" rx="8" fill="#F9FAFB" stroke="#D1D5DB"/>
        <text x="20" y="30" font-size="13" font-weight="700" fill="#111827">3. Stage 2 DeBERTa Cross-Encoder</text>
        <text x="20" y="52" font-size="11" font-weight="400" fill="#4B5563">• cross-encoder/nli-deberta-v3-base</text>
        <text x="20" y="70" font-size="11" font-weight="400" fill="#4B5563">• Pair: [Premise: Statute | Hypo: Clause]</text>
        <text x="20" y="88" font-size="11" font-weight="400" fill="#4B5563">• Softmax: [Contra, Entail, Neutral]</text>
        <text x="20" y="106" font-size="11" font-weight="400" fill="#4B5563">• Calibrated Threshold: tau* = 0.45</text>
        <rect x="20" y="120" width="150" height="20" rx="4" fill="#FEE2E2"/>
        <text x="95" y="134" font-size="10" font-weight="600" fill="#DC2626" text-anchor="middle">Binary Conflict Verdict</text>
      </g>

      <!-- Corpus Specs Table snippet -->
      <g transform="translate(30, 230)">
        <rect width="1040" height="150" rx="8" fill="#F9FAFB" stroke="#E5E7EB"/>
        <text x="20" y="25" font-size="12" font-weight="700" fill="#111827">Dual Statutory Knowledge Base Overview</text>
        <text x="20" y="48" font-size="11" fill="#4B5563">National Enactments (Lawphil): <strong>25,432</strong> acts (1901–2024) &bull; <strong>166,419</strong> searchable provisions</text>
        <text x="20" y="68" font-size="11" fill="#4B5563">Local Davao Enactments (SP / LISSP): <strong>1,664</strong> ordinances (1947–2026) &bull; <strong>10,002</strong> searchable provisions</text>
        <text x="20" y="88" font-size="11" fill="#4B5563">Total Statutory Corpus: <strong>27,096 enactments</strong> &bull; <strong>176,421 searchable provisions</strong> with full hierarchical ancestry</text>
        <text x="20" y="108" font-size="11" fill="#4B5563">Empirical Target: Local Government Unit Edge Deployment (Core i3-10105F, 8GB RAM, CPU-only latency &lt; 600ms)</text>
        <text x="20" y="128" font-size="11" fill="#6B7280">Proponents: Ralph Paolo Dulce &amp; Yahyah Odin | Adviser: Adrian "Ogs" Ablazo | Professor: Ma'am Grace Tacadao</text>
      </g>
    </g>
  </g>
""")

    # =========================================================================
    # SCREEN 2: UNIFIED MASTER-DETAIL RESULTS VIEW (X: 1480, Y: 40, W: 1440, H: 1300)
    # =========================================================================
    s2_x = 1480
    s2_y = 40
    s2_w = 1440
    s2_h = 1300

    svg.append(f"""
  <!-- ======================================================================= -->
  <!-- SCREEN 2: UNIFIED MASTER-DETAIL RESULTS AUDIT DASHBOARD                -->
  <!-- ======================================================================= -->
  <g id="Screen-2-Results-Dashboard">
    <!-- Artboard Frame -->
    <rect x="{s2_x}" y="{s2_y}" width="{s2_w}" height="{s2_h}" rx="12" class="artboard-bg" />

    <!-- Screen Title Annotation -->
    <text x="{s2_x + 30}" y="{s2_y - 12}" font-size="16" font-weight="700" fill="#374151" font-family="Inter, sans-serif">SCREEN 2: UNIFIED MASTER-DETAIL CONFLICT AUDIT (LO-FI WIREFRAME)</text>

    <!-- Top App Navigation Bar -->
    <g id="S2-Navbar">
      <rect x="{s2_x}" y="{s2_y}" width="{s2_w}" height="70" rx="12" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="1.5"/>
      
      <!-- Back Button -->
      <rect x="{s2_x + 25}" y="{s2_y + 18}" width="160" height="34" rx="6" fill="#F3F4F6" stroke="#D1D5DB"/>
      <text x="{s2_x + 105}" y="{s2_y + 40}" font-size="12" font-weight="600" fill="#111827" text-anchor="middle">← Upload New Draft</text>

      <!-- Active File Breadcrumb -->
      <text x="{s2_x + 210}" y="{s2_y + 36}" font-size="15" font-weight="700" fill="#111827">DRAFT-ORD-2026-02.pdf</text>
      <text x="{s2_x + 210}" y="{s2_y + 52}" font-size="11" font-weight="500" fill="#6B7280">Davao City Comprehensive Clean Air and Anti-Smoking Draft Ordinance of 2026</text>

      <!-- Right Export & Info Controls -->
      <rect x="{s2_x + s2_w - 380}" y="{s2_y + 18}" width="160" height="34" rx="6" fill="#FFFFFF" stroke="#D1D5DB"/>
      <text x="{s2_x + s2_w - 300}" y="{s2_y + 40}" font-size="11" font-weight="600" fill="#374151" text-anchor="middle">Export Audit Report ⤓</text>

      <rect x="{s2_x + s2_w - 200}" y="{s2_y + 18}" width="175" height="34" rx="6" fill="#F3F4F6" stroke="#D1D5DB"/>
      <text x="{s2_x + s2_w - 112}" y="{s2_y + 40}" font-size="11" font-weight="600" fill="#111827" text-anchor="middle">15 Operative Sections</text>
    </g>

    <!-- Executive Summary Banner (Top Status) -->
    <g id="S2-Executive-Banner" transform="translate({s2_x + 25}, {s2_y + 85})">
      <rect width="{s2_w - 50}" height="76" rx="8" fill="#FEF2F2" stroke="#F87171" stroke-width="1.5"/>
      <!-- Warning Icon -->
      <g transform="translate(20, 20)">
        <polygon points="18,3 33,31 3,31" fill="#EF4444" stroke="#DC2626" stroke-width="1.5"/>
        <text x="18" y="27" font-size="16" font-weight="800" fill="#FFFFFF" text-anchor="middle">!</text>
      </g>
      <text x="68" y="34" font-size="16" font-weight="800" fill="#991B1B" font-family="Inter, sans-serif">Potential Legal Conflict Detected (2 Operative Sections Flagged)</text>
      <text x="68" y="56" font-size="12" font-weight="400" fill="#7F1D1D" font-family="Inter, sans-serif">The ex-ante audit identified 2 operative provisions that appear to conflict with superior national statutes under RA 7160 Section 5(a) and the Magtajas doctrine.</text>

      <!-- Summary Pill Badge (Right) -->
      <rect x="{s2_w - 50 - 240}" y="20" width="220" height="36" rx="6" fill="#FFFFFF" stroke="#EF4444"/>
      <text x="{s2_w - 50 - 130}" y="43" font-size="12" font-weight="700" fill="#DC2626" text-anchor="middle">2 Flagged &bull; 13 Compliant</text>
    </g>

    <!-- MASTER SECTION TRIAGE STRIP (Horizontal Chips Navigator) -->
    <g id="S2-Section-Triage-Strip" transform="translate({s2_x + 25}, {s2_y + 175})">
      <rect width="{s2_w - 50}" height="105" rx="8" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="1.5"/>
      <text x="20" y="24" font-size="12" font-weight="700" fill="#374151">DOCUMENT OPERATIVE SECTION SELECTOR &amp; TRIAGE STRIP (Click to inspect section details):</text>
      
      <!-- Section Chips Flow -->
      <!-- Sec 1 (Neutral) -->
      <g transform="translate(20, 36)">
        <rect width="165" height="52" rx="6" fill="#F9FAFB" stroke="#D1D5DB"/>
        <text x="12" y="22" font-size="11" font-weight="700" fill="#111827">Sec. 1: Short Title</text>
        <rect x="12" y="28" width="60" height="16" rx="3" fill="#E5E7EB"/>
        <text x="42" y="40" font-size="9" font-weight="700" fill="#4B5563" text-anchor="middle">NEUTRAL</text>
        <text x="80" y="40" font-size="10" font-weight="500" fill="#6B7280">1.2% Risk</text>
      </g>

      <!-- Sec 2 (Entailment) -->
      <g transform="translate(195, 36)">
        <rect width="185" height="52" rx="6" fill="#F9FAFB" stroke="#D1D5DB"/>
        <text x="12" y="22" font-size="11" font-weight="700" fill="#111827">Sec. 2: Policy &amp; Purpose</text>
        <rect x="12" y="28" width="80" height="16" rx="3" fill="#DCFCE7"/>
        <text x="52" y="40" font-size="9" font-weight="700" fill="#16A34A" text-anchor="middle">ENTAILMENT</text>
        <text x="100" y="40" font-size="10" font-weight="500" fill="#6B7280">0.8% Risk</text>
      </g>

      <!-- Sec 3: Buffer Zone [ACTIVE SELECTED ITEM - CONFLICT] -->
      <g transform="translate(390, 36)">
        <!-- Highlighted Box with Active Indicator -->
        <rect width="245" height="52" rx="6" fill="#FEF2F2" stroke="#DC2626" stroke-width="2"/>
        <text x="12" y="22" font-size="11" font-weight="800" fill="#991B1B">Sec. 3: Buffer Zone Mandate</text>
        <rect x="12" y="28" width="95" height="16" rx="3" fill="#FEE2E2"/>
        <text x="59" y="40" font-size="9" font-weight="800" fill="#DC2626" text-anchor="middle">CONFLICT 88.4%</text>
        <text x="115" y="40" font-size="10" font-weight="700" fill="#DC2626">▲ INSPECTING</text>
        <!-- Triangle pointer pointing down -->
        <polygon points="122,54 130,62 138,54" fill="#DC2626"/>
      </g>

      <!-- Sec 4 (Neutral) -->
      <g transform="translate(645, 36)">
        <rect width="175" height="52" rx="6" fill="#F9FAFB" stroke="#D1D5DB"/>
        <text x="12" y="22" font-size="11" font-weight="700" fill="#111827">Sec. 4: Smoke-Free Areas</text>
        <rect x="12" y="28" width="60" height="16" rx="3" fill="#E5E7EB"/>
        <text x="42" y="40" font-size="9" font-weight="700" fill="#4B5563" text-anchor="middle">NEUTRAL</text>
        <text x="80" y="40" font-size="10" font-weight="500" fill="#6B7280">2.1% Risk</text>
      </g>

      <!-- Sec 5: Warrantless Search [CONFLICT #2] -->
      <g transform="translate(830, 36)">
        <rect width="215" height="52" rx="6" fill="#FFF7ED" stroke="#EA580C"/>
        <text x="12" y="22" font-size="11" font-weight="700" fill="#9A3412">Sec. 5: Vehicular Search</text>
        <rect x="12" y="28" width="95" height="16" rx="3" fill="#FFEDD5"/>
        <text x="59" y="40" font-size="9" font-weight="800" fill="#EA580C" text-anchor="middle">CONFLICT 74.6%</text>
        <text x="115" y="40" font-size="10" font-weight="500" fill="#9A3412">RA 4136 / Const.</text>
      </g>

      <!-- Sec 6 to 15 (Grouped / More) -->
      <g transform="translate(1055, 36)">
        <rect width="180" height="52" rx="6" fill="#F3F4F6" stroke="#D1D5DB" stroke-dasharray="3,3"/>
        <text x="15" y="25" font-size="11" font-weight="600" fill="#4B5563">Sec. 6–15 (Penalties)</text>
        <text x="15" y="42" font-size="10" font-weight="500" fill="#6B7280">10 Compliant Sections →</text>
      </g>

      <!-- Quick Filter Toggles (Right) -->
      <g transform="translate(1250, 42)">
        <rect width="120" height="38" rx="6" fill="#111827"/>
        <text x="60" y="24" font-size="11" font-weight="600" fill="#FFFFFF" text-anchor="middle">Only Flagged (2)</text>
      </g>
    </g>

    <!-- MAIN TWO-COLUMN SPLIT (Stage 1 Left vs Stage 2 Right) -->
    <!-- COLUMN 1 (LEFT): STAGE 1 CANDIDATE SHORTLIST (Width: 420px) -->
    <g id="S2-Col1-Stage1-Shortlist" transform="translate({s2_x + 25}, {s2_y + 295})">
      <rect width="420" height="970" rx="8" class="card-bg"/>
      
      <!-- Card Header -->
      <rect width="420" height="55" rx="8" fill="#F9FAFB" stroke="#E5E7EB"/>
      <rect x="20" y="16" width="60" height="22" rx="4" fill="#DBEAFE"/>
      <text x="50" y="31" font-size="10" font-weight="700" fill="#1D4ED8" text-anchor="middle">STAGE 1</text>
      <text x="90" y="32" font-size="13" font-weight="700" fill="#111827">Statutory Candidate Shortlist</text>
      <rect x="310" y="16" width="95" height="22" rx="4" fill="#E5E7EB"/>
      <text x="357" y="31" font-size="9" font-weight="600" fill="#374151" text-anchor="middle">176,421 Screened</text>

      <text x="20" y="80" font-size="11" font-weight="400" fill="#6B7280">Hybrid Retrieval: all-MiniLM-L6-v2 + BM25 (α = 0.50)</text>
      <text x="20" y="98" font-size="10" font-weight="500" fill="#9CA3AF">Latency: 1.33 ms &bull; Top-50 Safety Buffer</text>

      <!-- Table Header -->
      <g transform="translate(15, 115)">
        <rect width="390" height="30" fill="#F3F4F6" rx="4"/>
        <text x="12" y="20" font-size="10" font-weight="700" fill="#4B5563">Rank</text>
        <text x="50" y="20" font-size="10" font-weight="700" fill="#4B5563">Citation &amp; Provision</text>
        <text x="260" y="20" font-size="10" font-weight="700" fill="#4B5563">Score</text>
        <text x="320" y="20" font-size="10" font-weight="700" fill="#4B5563">Action</text>
      </g>

      <!-- Table Row 1 (Controlling Match - Active) -->
      <g transform="translate(15, 155)">
        <rect width="390" height="75" rx="6" fill="#EFF6FF" stroke="#3B82F6" stroke-width="1.5"/>
        <text x="12" y="25" font-size="12" font-weight="800" fill="#1D4ED8">#1</text>
        <text x="50" y="22" font-size="12" font-weight="700" fill="#111827">PD 1144 §6</text>
        <text x="50" y="40" font-size="10" font-weight="400" fill="#4B5563">Fertilizer and Pesticide Authority</text>
        <text x="50" y="55" font-size="10" font-weight="400" fill="#6B7280">Exclusive chemical &amp; aerial regulation</text>
        <text x="260" y="25" font-size="11" font-weight="700" fill="#1D4ED8">94.8%</text>
        <rect x="315" y="15" width="60" height="24" rx="4" fill="#FFFFFF" stroke="#3B82F6"/>
        <text x="345" y="31" font-size="10" font-weight="600" fill="#1D4ED8" text-anchor="middle">Lawphil ↗</text>
      </g>

      <!-- Table Row 2 -->
      <g transform="translate(15, 240)">
        <rect width="390" height="70" rx="6" fill="#FFFFFF" stroke="#E5E7EB"/>
        <text x="12" y="25" font-size="12" font-weight="700" fill="#4B5563">#2</text>
        <text x="50" y="22" font-size="12" font-weight="700" fill="#111827">RA 7160 §16</text>
        <text x="50" y="40" font-size="10" font-weight="400" fill="#4B5563">Local Government Code of 1991</text>
        <text x="50" y="55" font-size="10" font-weight="400" fill="#6B7280">General Welfare Clause authority</text>
        <text x="260" y="25" font-size="11" font-weight="700" fill="#4B5563">88.4%</text>
        <rect x="315" y="15" width="60" height="24" rx="4" fill="#F3F4F6" stroke="#D1D5DB"/>
        <text x="345" y="31" font-size="10" font-weight="600" fill="#4B5563" text-anchor="middle">Lawphil ↗</text>
      </g>

      <!-- Table Row 3 -->
      <g transform="translate(15, 320)">
        <rect width="390" height="70" rx="6" fill="#FFFFFF" stroke="#E5E7EB"/>
        <text x="12" y="25" font-size="12" font-weight="700" fill="#4B5563">#3</text>
        <text x="50" y="22" font-size="12" font-weight="700" fill="#111827">PD 856 §88</text>
        <text x="50" y="40" font-size="10" font-weight="400" fill="#4B5563">Code on Sanitation of the Philippines</text>
        <text x="50" y="55" font-size="10" font-weight="400" fill="#6B7280">Environmental health &amp; pest control</text>
        <text x="260" y="25" font-size="11" font-weight="700" fill="#4B5563">84.1%</text>
        <rect x="315" y="15" width="60" height="24" rx="4" fill="#F3F4F6" stroke="#D1D5DB"/>
        <text x="345" y="31" font-size="10" font-weight="600" fill="#4B5563" text-anchor="middle">Lawphil ↗</text>
      </g>

      <!-- Table Row 4 -->
      <g transform="translate(15, 400)">
        <rect width="390" height="70" rx="6" fill="#FFFFFF" stroke="#E5E7EB"/>
        <text x="12" y="25" font-size="12" font-weight="700" fill="#4B5563">#4</text>
        <text x="50" y="22" font-size="12" font-weight="700" fill="#111827">RA 8749 §19</text>
        <text x="50" y="40" font-size="10" font-weight="400" fill="#4B5563">Philippine Clean Air Act of 1999</text>
        <text x="50" y="55" font-size="10" font-weight="400" fill="#6B7280">Pollution control standards</text>
        <text x="260" y="25" font-size="11" font-weight="700" fill="#4B5563">81.2%</text>
        <rect x="315" y="15" width="60" height="24" rx="4" fill="#F3F4F6" stroke="#D1D5DB"/>
        <text x="345" y="31" font-size="10" font-weight="600" fill="#4B5563" text-anchor="middle">Lawphil ↗</text>
      </g>

      <!-- Table Row 5 -->
      <g transform="translate(15, 480)">
        <rect width="390" height="70" rx="6" fill="#FFFFFF" stroke="#E5E7EB"/>
        <text x="12" y="25" font-size="12" font-weight="700" fill="#4B5563">#5</text>
        <text x="50" y="22" font-size="12" font-weight="700" fill="#111827">Davao City Ord. 0367-12 §5</text>
        <text x="50" y="40" font-size="10" font-weight="400" fill="#4B5563">Comprehensive Anti-Smoking Ordinance</text>
        <text x="50" y="55" font-size="10" font-weight="400" fill="#6B7280">Local 10-meter open space buffer zone</text>
        <text x="260" y="25" font-size="11" font-weight="700" fill="#4B5563">76.5%</text>
        <rect x="315" y="15" width="60" height="24" rx="4" fill="#F3F4F6" stroke="#D1D5DB"/>
        <text x="345" y="31" font-size="10" font-weight="600" fill="#4B5563" text-anchor="middle">LISSP ↗</text>
      </g>

      <!-- Table Row 6 -->
      <g transform="translate(15, 560)">
        <rect width="390" height="70" rx="6" fill="#FFFFFF" stroke="#E5E7EB"/>
        <text x="12" y="25" font-size="12" font-weight="700" fill="#4B5563">#6</text>
        <text x="50" y="22" font-size="12" font-weight="700" fill="#111827">RA 7394 §5</text>
        <text x="50" y="40" font-size="10" font-weight="400" fill="#4B5563">Consumer Act of the Philippines</text>
        <text x="50" y="55" font-size="10" font-weight="400" fill="#6B7280">Hazardous substances labeling</text>
        <text x="260" y="25" font-size="11" font-weight="700" fill="#4B5563">72.6%</text>
        <rect x="315" y="15" width="60" height="24" rx="4" fill="#F3F4F6" stroke="#D1D5DB"/>
        <text x="345" y="31" font-size="10" font-weight="600" fill="#4B5563" text-anchor="middle">Lawphil ↗</text>
      </g>

      <!-- Table Row 7 to 50 summary -->
      <g transform="translate(15, 640)">
        <rect width="390" height="50" rx="6" fill="#F9FAFB" stroke="#D1D5DB" stroke-dasharray="3,3"/>
        <text x="195" y="30" font-size="11" font-weight="600" fill="#6B7280" text-anchor="middle">+ 44 Additional Candidate Provisions Ranked</text>
      </g>

      <!-- Shortlist Footnote info -->
      <g transform="translate(15, 710)">
        <rect width="390" height="240" rx="6" fill="#F3F4F6" stroke="#E5E7EB"/>
        <text x="15" y="25" font-size="11" font-weight="700" fill="#111827">Candidate Shortlist Audit Trail</text>
        <text x="15" y="48" font-size="10" fill="#4B5563">• 1st rank match: PD 1144 §6 selected as controlling premise.</text>
        <text x="15" y="66" font-size="10" fill="#4B5563">• Both national statutes and local ordinances are dynamically</text>
        <text x="15" y="82" font-size="10" fill="#4B5563">  queried for dual vertical and horizontal screening.</text>
        <text x="15" y="102" font-size="10" fill="#4B5563">• All candidates retain direct hyperlinked traceability to</text>
        <text x="15" y="118" font-size="10" fill="#4B5563">  official government repositories (Lawphil / LISSP).</text>
        <text x="15" y="140" font-size="10" fill="#4B5563">• Prepending syntax: [Citation | Title | Sub-heading | Text]</text>
        <text x="15" y="158" font-size="10" fill="#4B5563">• Preserves 98.4% Recall@20 across test benchmark.</text>

        <rect x="15" y="185" width="360" height="36" rx="6" fill="#FFFFFF" stroke="#D1D5DB"/>
        <text x="195" y="208" font-size="11" font-weight="600" fill="#374151" text-anchor="middle">View Full 50-Candidate Matrix Modal</text>
      </g>
    </g>

    <!-- COLUMN 2 (RIGHT): STAGE 2 NLI GAUGE & DUAL CLAUSE COMPARISON (Width: 940px) -->
    <g id="S2-Col2-Stage2-Analysis" transform="translate({s2_x + 470}, {s2_y + 295})">
      
      <!-- CARD 2A: STAGE 2 CONTRADICTION GAUGE & NLI METRICS (Height: 180px) -->
      <g id="S2-Gauge-Card">
        <rect width="940" height="180" rx="8" class="card-bg"/>
        
        <!-- Header -->
        <rect width="940" height="48" rx="8" fill="#F9FAFB" stroke="#E5E7EB"/>
        <rect x="20" y="13" width="60" height="22" rx="4" fill="#FEE2E2"/>
        <text x="50" y="28" font-size="10" font-weight="700" fill="#DC2626" text-anchor="middle">STAGE 2</text>
        <text x="90" y="29" font-size="13" font-weight="700" fill="#111827">Cross-Encoder NLI &amp; Preemption Decision Triage</text>
        <text x="440" y="29" font-size="11" font-weight="500" fill="#16A34A">DeBERTa-v3-base &bull; Live Neural CPU (297.6 ms forward pass)</text>

        <!-- Left: Gauge Metric -->
        <g transform="translate(30, 65)">
          <text x="0" y="14" font-size="11" font-weight="700" fill="#6B7280">CONTRADICTION CONFIDENCE</text>
          <text x="0" y="52" font-size="38" font-weight="800" fill="#DC2626">88.4%</text>

          <rect x="150" y="22" width="180" height="26" rx="4" fill="#FEE2E2" stroke="#EF4444"/>
          <text x="240" y="39" font-size="11" font-weight="800" fill="#DC2626" text-anchor="middle">CONTRADICTION DETECTED</text>
        </g>

        <!-- Center: Threshold Slider -->
        <g transform="translate(390, 80)">
          <!-- Track -->
          <rect width="500" height="10" rx="5" fill="#E5E7EB"/>
          <!-- Active Value Fill up to 88.4% -->
          <rect width="442" height="10" rx="5" fill="#DC2626"/>
          
          <!-- 45% Threshold marker pin -->
          <line x1="225" y1="-8" x2="225" y2="18" stroke="#111827" stroke-width="2.5"/>
          <polygon points="220,-8 230,-8 225,-1" fill="#111827"/>
          <text x="225" y="-14" font-size="10" font-weight="800" fill="#111827" text-anchor="middle">▲ 45.0% DECISION THRESHOLD</text>

          <!-- Scale labels -->
          <text x="0" y="28" font-size="10" font-weight="600" fill="#6B7280">0% (Harmonious)</text>
          <text x="500" y="28" font-size="10" font-weight="600" fill="#6B7280" text-anchor="end">100% (Direct Preemption)</text>

          <!-- Explanation caption -->
          <text x="0" y="50" font-size="11" font-weight="500" fill="#374151">Flagged because contradiction probability (88.4%) strictly exceeds the calibrated 45.0% threshold.</text>
        </g>
      </g>

      <!-- CARD 2B: DUAL STATUTORY CLAUSE COMPARISON (Height: 520px) -->
      <g id="S2-Dual-Clauses-Card" transform="translate(0, 195)">
        <rect width="940" height="520" rx="8" class="card-bg"/>

        <!-- Header -->
        <rect width="940" height="48" rx="8" fill="#F9FAFB" stroke="#E5E7EB"/>
        <text x="20" y="29" font-size="13" font-weight="700" fill="#111827">Side-by-Side Clause Cross-Examination (Hierarchical Tree &amp; Lexical Grounding)</text>
        <text x="890" y="29" font-size="11" font-weight="600" fill="#2563EB" text-anchor="end">Synchronized View</text>

        <!-- SUB-PANE 1: CONTROLLING NATIONAL STATUTE (LEFT SUB-COLUMN, Width: 440px) -->
        <g id="S2-Subpane-Statute" transform="translate(20, 60)">
          <rect width="440" height="440" rx="8" fill="#F8FAFC" stroke="#93C5FD" stroke-width="1.5"/>
          
          <!-- Subpane Title -->
          <rect width="440" height="40" rx="8" fill="#EFF6FF" stroke="#BFDBFE"/>
          <text x="15" y="25" font-size="12" font-weight="800" fill="#1E40AF">CONTROLLING NATIONAL STATUTE (PREMISE)</text>
          <rect x="330" y="8" width="95" height="24" rx="4" fill="#DBEAFE"/>
          <text x="377" y="24" font-size="10" font-weight="700" fill="#1D4ED8" text-anchor="middle">SUPERIOR LAW</text>

          <!-- Hierarchical Breadcrumb Tree -->
          <g transform="translate(15, 52)">
            <rect width="410" height="75" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
            <text x="12" y="22" font-size="11" font-weight="800" fill="#0F172A">Presidential Decree No. 1144</text>
            <text x="12" y="38" font-size="10" font-weight="500" fill="#475569">CREATING THE FERTILIZER AND PESTICIDE AUTHORITY (1977)</text>
            
            <line x1="20" y1="46" x2="20" y2="58" stroke="#3B82F6" stroke-width="2"/>
            <text x="28" y="58" font-size="11" font-weight="700" fill="#1E40AF">↳ Section 6: Powers and Functions</text>
          </g>

          <!-- Operative Clause Text Box with Token Highlights -->
          <g transform="translate(15, 140)">
            <rect width="410" height="240" rx="6" fill="#FFFFFF" stroke="#CBD5E1"/>
            <text x="12" y="24" font-size="11" font-weight="700" fill="#334155">Controlling Operative Text (Lawphil Official Transcript):</text>
            
            <!-- Simulated Paragraph with Lexical Highlight Blocks -->
            <text x="12" y="55" font-size="12" font-family="Inter, sans-serif" fill="#1E293B">"The </text>
            <!-- Highlight 1: Fertilizer and Pesticide Authority (Blue) -->
            <rect x="42" y="42" width="220" height="18" rx="3" fill="#BAE6FD"/>
            <text x="46" y="55" font-size="12" font-weight="700" fill="#0369A1">Fertilizer and Pesticide Authority</text>
            <text x="268" y="55" font-size="12" fill="#1E293B"> shall have</text>

            <!-- Highlight 2: exclusive jurisdiction (Blue) -->
            <rect x="12" y="65" width="145" height="18" rx="3" fill="#BAE6FD"/>
            <text x="16" y="78" font-size="12" font-weight="700" fill="#0369A1">exclusive jurisdiction</text>
            <text x="162" y="78" font-size="12" fill="#1E293B"> over all fertilizers, pesticides,</text>

            <text x="12" y="101" font-size="12" fill="#1E293B">and other agricultural chemicals, and shall </text>

            <!-- Highlight 3: regulate and monitor (Blue) -->
            <rect x="265" y="88" width="135" height="18" rx="3" fill="#BAE6FD"/>
            <text x="269" y="101" font-size="12" font-weight="700" fill="#0369A1">regulate and monitor</text>

            <text x="12" y="124" font-size="12" fill="#1E293B">their importation, manufacture, formulation, sale,</text>
            <text x="12" y="145" font-size="12" fill="#1E293B">distribution, delivery, transport, storage, and aerial</text>
            <text x="12" y="166" font-size="12" fill="#1E293B">application in order to assure agricultural safety."</text>

            <!-- Metadata info box -->
            <rect x="12" y="190" width="386" height="38" rx="4" fill="#F1F5F9"/>
            <text x="20" y="206" font-size="10" font-weight="600" fill="#475569">Source: Lawphil National Statute Archive (Verified)</text>
            <text x="20" y="220" font-size="10" font-weight="500" fill="#64748B">Prepended Context Length: 124 tokens (512-compliant)</text>
          </g>

          <!-- Direct Link -->
          <rect x="15" y="390" width="410" height="36" rx="6" fill="#EFF6FF" stroke="#3B82F6"/>
          <text x="220" y="413" font-size="11" font-weight="700" fill="#1D4ED8" text-anchor="middle">Open Controlling Statute on Lawphil ↗</text>
        </g>

        <!-- SUB-PANE 2: DRAFT LOCAL ORDINANCE (RIGHT SUB-COLUMN, Width: 440px) -->
        <g id="S2-Subpane-Ordinance" transform="translate(480, 60)">
          <rect width="440" height="440" rx="8" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1.5"/>

          <!-- Subpane Title -->
          <rect width="440" height="40" rx="8" fill="#FEF3C7" stroke="#FCD34D"/>
          <text x="15" y="25" font-size="12" font-weight="800" fill="#92400E">DRAFT LOCAL ORDINANCE CLAUSE (HYPOTHESIS)</text>
          <rect x="330" y="8" width="95" height="24" rx="4" fill="#FDE68A"/>
          <text x="377" y="24" font-size="10" font-weight="700" fill="#78350F" text-anchor="middle">LOCAL SCOPE</text>

          <!-- Hierarchical Breadcrumb Tree -->
          <g transform="translate(15, 52)">
            <rect width="410" height="75" rx="6" fill="#FFFFFF" stroke="#FDE68A"/>
            <text x="12" y="22" font-size="11" font-weight="800" fill="#0F172A">DRAFT-ORD-2026-02.pdf</text>
            <text x="12" y="38" font-size="10" font-weight="500" fill="#475569">Davao City Clean Air &amp; Anti-Smoking Draft Ordinance</text>
            
            <line x1="20" y1="46" x2="20" y2="58" stroke="#D97706" stroke-width="2"/>
            <text x="28" y="58" font-size="11" font-weight="800" fill="#B45309">↳ Section 3: Buffer Zone &amp; Aerial Prohibitions</text>
          </g>

          <!-- Operative Clause Text Box with Token Highlights -->
          <g transform="translate(15, 140)">
            <rect width="410" height="240" rx="6" fill="#FFFFFF" stroke="#CBD5E1"/>
            <text x="12" y="24" font-size="11" font-weight="700" fill="#78350F">Challenged Operative Clause (Proposed Draft):</text>

            <!-- Simulated Paragraph with Yellow Highlights -->
            <text x="12" y="55" font-size="12" font-family="Inter, sans-serif" fill="#1E293B">"All agricultural entities </text>

            <!-- Highlight 1: must maintain a mandatory (Yellow) -->
            <rect x="145" y="42" width="165" height="18" rx="3" fill="#FEF08A"/>
            <text x="149" y="55" font-size="12" font-weight="700" fill="#854D0E">must maintain a mandatory</text>

            <text x="12" y="78" font-size="12" fill="#1E293B">thirty (30) meter buffer zone within plantations, and</text>
            
            <text x="12" y="101" font-size="12" fill="#1E293B">aerial application of chemicals is hereby </text>

            <!-- Highlight 2: strictly prohibited (Yellow/Red) -->
            <rect x="250" y="88" width="120" height="18" rx="3" fill="#FECACA"/>
            <text x="254" y="101" font-size="12" font-weight="800" fill="#991B1B">strictly prohibited</text>

            <text x="12" y="124" font-size="12" fill="#1E293B">without prior written clearance from the Sangguniang</text>
            <text x="12" y="145" font-size="12" fill="#1E293B">Panlungsod of Davao City."</text>

            <!-- Conflict Badge info -->
            <rect x="12" y="190" width="386" height="38" rx="4" fill="#FEF2F2"/>
            <text x="20" y="206" font-size="10" font-weight="700" fill="#DC2626">Conflict Mechanism: Ultra Vires Prohibitive Preemption</text>
            <text x="20" y="220" font-size="10" font-weight="500" fill="#991B1B">An LGU cannot prohibit what national authority expressly regulates.</text>
          </g>

          <!-- Toggle Action -->
          <rect x="15" y="390" width="410" height="36" rx="6" fill="#FEF3C7" stroke="#D97706"/>
          <text x="220" y="413" font-size="11" font-weight="700" fill="#92400E" text-anchor="middle">View Proposed Legislative Amendment Suggestion ✎</text>
        </g>
      </g>

      <!-- CARD 2C: JURISPRUDENTIAL RATIONALE & DOCTRINAL CONTEXT (Height: 240px) -->
      <g id="S2-Legal-Rationale-Card" transform="translate(0, 725)">
        <rect width="940" height="240" rx="8" class="card-bg"/>

        <!-- Header -->
        <rect width="940" height="42" rx="8" fill="#F9FAFB" stroke="#E5E7EB"/>
        <text x="20" y="26" font-size="13" font-weight="700" fill="#111827">Doctrinal Rationale &amp; Supreme Court Precedent Context (Magtajas Doctrine)</text>
        <text x="890" y="26" font-size="11" font-weight="600" fill="#4B5563" text-anchor="end">Section 5(a), RA 7160</text>

        <!-- Rationale Body -->
        <g transform="translate(20, 55)">
          <text x="0" y="18" font-size="12" font-weight="700" fill="#111827">Controlling Jurisprudential Doctrine:</text>
          <text x="0" y="38" font-size="11" font-weight="400" fill="#374151">Under the landmark ruling in <em>Magtajas v. Pryce Properties Corp. (234 SCRA 255)</em> and affirmed in <em>Mosqueda v. Pilipino Banana Growers (G.R. 189180)</em>:</text>
          <text x="15" y="58" font-size="11" font-weight="600" fill="#1E293B">"A municipal ordinance must not contravene the Constitution or any statute. An ordinance cannot prohibit that which the statute</text>
          <text x="15" y="74" font-size="11" font-weight="600" fill="#1E293B">permits, nor permit that which the statute prohibits. Local regulation must conform to national standards."</text>

          <line x1="0" y1="92" x2="900" y2="92" stroke="#E5E7EB" stroke-width="1"/>

          <text x="0" y="112" font-size="12" font-weight="700" fill="#111827">Ex-Ante Recommendation for Sangguniang Panlungsod Legal Researchers:</text>
          <text x="0" y="132" font-size="11" font-weight="400" fill="#374151">1. Amend Section 3 to harmoniously adopt FPA safety guidelines rather than enacting a categorical local prohibition.</text>
          <text x="0" y="150" font-size="11" font-weight="400" fill="#374151">2. Retain 10-meter open space buffer for ground smoking (consistent with RA 9211 and Ordinance 0367-12).</text>
          <text x="0" y="168" font-size="11" font-weight="400" fill="#374151">3. Refer challenged operative wording to SP Committee on Ordinances and Rules prior to 2nd reading.</text>
        </g>
      </g>
    </g>
  </g>
</svg>
""")

    svg_content = "\n".join(svg)

    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg_content)

    static_svg = STATIC_DIR / "conflict_detection_lofi_wireframe.svg"
    with open(static_svg, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"[x] Wireframe SVG created successfully:")
    print(f"    - Main:   {SVG_FILE}")
    print(f"    - Static: {static_svg}")


if __name__ == "__main__":
    build_svg()
