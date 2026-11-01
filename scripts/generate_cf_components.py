"""
Generates the 6 standalone, remade high-resolution Conceptual Framework component images
for presentation slides and cleanses AI buzzwords ("protocol" -> "framework" / "pipeline")
in both the standalone components and the master conceptual framework flowchart.
"""
import os
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FIGS_DIR = ROOT / "CS_Undergraduate_Thesis_Template" / "figs"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

COMMON_CSS = """
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    background-color: #ffffff;
    color: #000000;
    font-family: "Times New Roman", Times, Georgia, serif;
    line-height: 1.3;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px;
}

.capture-box {
    background-color: #ffffff;
    padding: 16px;
    border: 1px solid transparent;
}

/* Containers */
.phase-container {
    border: 2px solid #000000;
    padding: 26px 18px 18px 18px;
    position: relative;
    background-color: #ffffff;
}

.phase-title {
    position: absolute;
    top: -12px;
    left: 20px;
    background: #ffffff;
    padding: 0 10px;
    font-weight: bold;
    font-size: 14.5px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.sub-container {
    border: 1.5px solid #000000;
    padding: 22px 16px 16px 16px;
    position: relative;
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
}

.sub-title {
    position: absolute;
    top: -10px;
    left: 14px;
    background: #ffffff;
    padding: 0 6px;
    font-size: 13px;
    font-style: italic;
    font-weight: bold;
}

.stage-container {
    border: 1px dotted #000000;
    padding: 18px 16px 16px 16px;
    background-color: #ffffff;
    position: relative;
    margin-bottom: 6px;
}

.stage-title {
    font-weight: bold;
    font-size: 13.5px;
    text-align: center;
    margin-bottom: 12px;
    letter-spacing: 0.2px;
}

/* Academic Boxes */
.academic-box {
    border: 1px solid #000000;
    padding: 9px 13px;
    background-color: #ffffff;
    text-align: center;
    font-size: 12.5px;
    line-height: 1.35;
    position: relative;
    z-index: 10;
}

.box-title {
    font-weight: bold;
    font-size: 12.5px;
}

.box-desc {
    font-size: 10.5px;
    font-style: italic;
    color: #1e293b;
    margin-top: 2px;
    display: block;
}

.box-highlight {
    background-color: #f8fafc;
    border: 1.5px solid #000000;
}

/* Lines and Arrows */
.line-v {
    width: 1.5px;
    height: 16px;
    background-color: #000000;
    margin: 0 auto;
}

.line-v-sm {
    width: 1.5px;
    height: 10px;
    background-color: #000000;
    margin: 0 auto;
}

.line-v-md {
    width: 1.5px;
    height: 22px;
    background-color: #000000;
    margin: 0 auto;
}

.arrow-down {
    width: 0;
    height: 0;
    border-left: 4.5px solid transparent;
    border-right: 4.5px solid transparent;
    border-top: 7px solid #000000;
    margin: 0 auto;
}

.arrow-right {
    width: 0;
    height: 0;
    border-top: 4.5px solid transparent;
    border-bottom: 4.5px solid transparent;
    border-left: 7px solid #000000;
}

/* Stream Bridge */
.stream-bridge {
    width: 100%;
    height: 28px;
    position: relative;
    margin-top: 2px;
}

.stream-line-l {
    position: absolute;
    top: 0;
    left: 25%;
    width: 1.5px;
    height: 14px;
    background-color: #000000;
}

.stream-line-r {
    position: absolute;
    top: 0;
    right: 25%;
    width: 1.5px;
    height: 14px;
    background-color: #000000;
}

.stream-line-h {
    position: absolute;
    top: 14px;
    left: 25%;
    right: 25%;
    height: 1.5px;
    background-color: #000000;
}

.stream-line-c {
    position: absolute;
    top: 14px;
    left: 50%;
    width: 1.5px;
    height: 8px;
    background-color: #000000;
    transform: translateX(-50%);
}

.stream-arrow-c {
    position: absolute;
    top: 22px;
    left: 50%;
    transform: translateX(-50%);
}

/* Decision Diamond */
.diamond-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 2px 0 0 0;
    position: relative;
}

.academic-diamond {
    width: 90px;
    height: 90px;
    border: 1.5px solid #000000;
    transform: rotate(45deg);
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #ffffff;
    margin: 8px auto 6px auto;
    position: relative;
    z-index: 10;
}

.diamond-text {
    transform: rotate(-45deg);
    font-size: 11px;
    font-weight: bold;
    text-align: center;
    width: 95px;
    line-height: 1.25;
}

.diamond-threshold-badge {
    background-color: #ffffff;
    border: 1px solid #94a3b8;
    padding: 2px 8px;
    font-size: 10.5px;
    font-style: italic;
    color: #334155;
    z-index: 15;
    margin-top: -2px;
    margin-bottom: 2px;
}

/* Decision Splitter */
.decision-fork {
    position: relative;
    width: 100%;
    height: 44px;
}

.fork-line-center {
    position: absolute;
    top: 0;
    left: 50%;
    width: 1.5px;
    height: 14px;
    background-color: #000000;
    transform: translateX(-50%);
}

.fork-line-h {
    position: absolute;
    top: 14px;
    left: 25%;
    right: 25%;
    height: 1.5px;
    background-color: #000000;
}

.fork-drop-l {
    position: absolute;
    top: 14px;
    left: 25%;
    width: 1.5px;
    height: 22px;
    background-color: #000000;
}

.fork-arrow-l {
    position: absolute;
    top: 36px;
    left: 25%;
    transform: translateX(-50%);
}

.fork-label-l {
    position: absolute;
    top: 18px;
    left: 25%;
    transform: translateX(-50%);
    background: #ffffff;
    padding: 0 5px;
    font-size: 11.5px;
    font-weight: bold;
    z-index: 10;
    border: 1px solid #000;
}

.fork-drop-r {
    position: absolute;
    top: 14px;
    right: 25%;
    width: 1.5px;
    height: 22px;
    background-color: #000000;
}

.fork-arrow-r {
    position: absolute;
    top: 36px;
    right: 25%;
    transform: translateX(50%);
}

.fork-label-r {
    position: absolute;
    top: 18px;
    right: 25%;
    transform: translateX(50%);
    background: #ffffff;
    padding: 0 5px;
    font-size: 11.5px;
    font-weight: bold;
    z-index: 10;
    border: 1px solid #000;
}
"""

TEMPLATES = {
    "cf_phase1_ingestion": f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{COMMON_CSS}</style></head>
<body>
<div class="capture-box" style="width: 520px;">
    <div class="sub-container">
        <span class="sub-title">Dual-Corpus Ingestion &amp; Pre-Computation Pipeline</span>
        
        <div class="academic-box" style="margin-top: 4px;">
            <span class="box-title">Dual Statutory Corpus Acquisition</span>
            <span class="box-desc">Philippine National Statutory Archive (RAs, EOs, PDs, Acts, BPs, CAs)<br>+ Davao City Municipal Ordinances (Landmark &amp; Digital LISSP Archives)<br><b>Multi-Jurisdictional Legal Knowledge Base</b></span>
        </div>
        
        <div class="line-v-sm"></div><div class="arrow-down"></div>
        
        <div class="academic-box">
            <span class="box-title">Legal Text Normalization &amp; Section Chunking</span>
            <span class="box-desc">Structural Section Segmentation into Granular Regulatory Units<br>OCR Noise Mitigation on Local Scans &amp; Unsupervised Statutory Topic Modeling</span>
        </div>
        
        <div class="line-v-sm"></div><div class="arrow-down"></div>
        
        <div class="academic-box box-highlight">
            <span class="box-title">Offline Index &amp; Vector Store</span>
            <span class="box-desc">Pre-Computed Dense Vector Representations (Transformer Bi-Encoder Embeddings)<br>Sparse Inverted Index (BM25 with Term-Frequency &amp; Length Normalization)</span>
        </div>
    </div>
</div>
</body></html>
""",

    "cf_phase1_benchmarking": f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{COMMON_CSS}</style></head>
<body>
<div class="capture-box" style="width: 520px;">
    <div class="sub-container">
        <span class="sub-title">Model Evaluation Benchmark &amp; Selection Framework</span>
        
        <div class="academic-box" style="margin-top: 4px;">
            <span class="box-title">Ground Truth Legal Benchmark Curation</span>
            <span class="box-desc">Multi-Tiered Expert-Annotated Statutory Clause Pairs:<br>Tier 1 (Surface Lexical), Tier 2 (Structural Preemption), Tier 3 (Latent Semantic)</span>
        </div>
        
        <div class="line-v-sm"></div><div class="arrow-down"></div>
        
        <div class="academic-box">
            <span class="box-title">Empirical Candidate Screening &amp; Ablation</span>
            <span class="box-desc">Stage 1: Multi-Candidate Dense Bi-Encoder Evaluation (Latency vs. Recall@<i>k</i>)<br>Stage 2: Cross-Encoder Architecture Screening across Precision &amp; Quantization Axes</span>
        </div>
        
        <div class="line-v-sm"></div><div class="arrow-down"></div>
        
        <div class="academic-box box-highlight">
            <span class="box-title">Selected Production Logic Engines</span>
            <span class="box-desc">Stage 1 Retrieval Workhorse: Optimal Dense Bi-Encoder (Maximizing Candidate Recall)<br>Stage 2 Reasoning Engine: Optimal Cross-Encoder (Maximizing Contradiction <i>F</i><sub>1</sub>)</span>
        </div>
    </div>
</div>
</body></html>
""",

    "cf_phase2_input": f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{COMMON_CSS}</style></head>
<body>
<div class="capture-box" style="width: 980px;">
    <div class="sub-container">
        <span class="sub-title">1. System Input</span>
        
        <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-top: 4px;">
            <div class="academic-box" style="flex: 1;">
                <span class="box-title">Proposed Ex-Ante Ordinance Draft</span>
                <span class="box-desc">Digital-Born Legislative Submission<br>(.docx / Digital PDF from City Council)</span>
            </div>

            <div style="display: flex; align-items: center; width: 32px; justify-content: center;">
                <div style="width: 24px; height: 1.5px; background: #000;"></div>
                <div class="arrow-right" style="margin-left: -1px;"></div>
            </div>

            <div class="academic-box" style="flex: 1.2;">
                <span class="box-title">Automated Section Parsing &amp; Filtering</span>
                <span class="box-desc">Isolates Operative Regulatory Mandates;<br>Strips Title, Separability, Repealing &amp; Effectivity</span>
            </div>

            <div style="display: flex; align-items: center; width: 32px; justify-content: center;">
                <div style="width: 24px; height: 1.5px; background: #000;"></div>
                <div class="arrow-right" style="margin-left: -1px;"></div>
            </div>

            <div class="academic-box" style="flex: 1;">
                <span class="box-title">Live Provision Vectorization</span>
                <span class="box-desc">Real-Time Dense Vector Encoding<br>&amp; Sparse Lexical Token Extraction</span>
            </div>
        </div>
    </div>
</div>
</body></html>
""",

    "cf_phase2_stage1": f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{COMMON_CSS}</style></head>
<body>
<div class="capture-box" style="width: 980px;">
    <div class="sub-container" style="background-color: #fafbfc;">
        <span class="sub-title">2. Computational Process (Coarse-to-Fine Pipeline)</span>
        
        <!-- Stage 1 -->
        <div class="stage-container" style="width: 96%; margin: 6px auto 6px auto;">
            <div class="stage-title">Stage 1: Dual-Stream Hybrid Information Retrieval (Coarse Filter)</div>
            
            <div style="display: flex; justify-content: space-between; gap: 16px;">
                <div class="academic-box" style="flex: 1;">
                    <span class="box-title">Stream A: Lexical Sparse Search (BM25)</span>
                    <span class="box-desc">Exact Statutory Citations, Penalty Quantums &amp; Key Administrative Terms</span>
                </div>
                <div class="academic-box" style="flex: 1;">
                    <span class="box-title">Stream B: Dense Semantic Retrieval (Bi-Encoder)</span>
                    <span class="box-desc">Normalized Semantic Vector Cosine Similarity for Regulatory Intent</span>
                </div>
            </div>

            <!-- Stream Connector -->
            <div class="stream-bridge">
                <div class="stream-line-l"></div>
                <div class="stream-line-r"></div>
                <div class="stream-line-h"></div>
                <div class="stream-line-c"></div>
                <div class="stream-arrow-c"><div class="arrow-down"></div></div>
            </div>

            <div class="academic-box" style="width: 78%; margin: 0 auto;">
                <span class="box-title">Reciprocal Rank Fusion (RRF) &amp; Statutory Hierarchy Safeguard</span>
                <span class="box-desc">Fuses Lexical &amp; Semantic Ranks; Enforces Hierarchy Precedence (Constitution &gt; Statute &gt; Ordinance)</span>
            </div>

            <div class="line-v-sm"></div><div class="arrow-down"></div>

            <div class="academic-box box-highlight" style="width: 68%; margin: 0 auto;">
                <span class="box-title">Top-<i>k</i> Candidate Statutory Shortlist</span>
                <span class="box-desc">Prunes Broad Search Space to <i>k</i> Most Normatively Relevant Candidate Provisions</span>
            </div>
        </div>
    </div>
</div>
</body></html>
""",

    "cf_phase2_stage2": f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{COMMON_CSS}</style></head>
<body>
<div class="capture-box" style="width: 980px;">
    <div class="sub-container" style="background-color: #fafbfc;">
        <span class="sub-title">2. Computational Process (Coarse-to-Fine Pipeline)</span>
        
        <!-- Stage 2 -->
        <div class="stage-container" style="width: 96%; margin: 6px auto 6px auto;">
            <div class="stage-title">Stage 2: Natural Language Inference (Fine Contradiction Classification)</div>
            
            <div class="academic-box" style="width: 82%; margin: 0 auto;">
                <span class="box-title">Pair-wise Cross-Encoder Input Sequence Construction</span>
                <span class="box-desc">Formatted Input: <code>[CLS] Retrieved Statutory Premise [SEP] Proposed Ordinance Clause [SEP]</code></span>
            </div>

            <div class="line-v-sm"></div><div class="arrow-down"></div>

            <div class="academic-box box-highlight" style="width: 82%; margin: 0 auto;">
                <span class="box-title">Deep Cross-Attention Contradiction Classification</span>
                <span class="box-desc">Evaluated via Selected Cross-Encoder NLI Engine (Full Token-Level Cross-Attention Reasoning)</span>
            </div>
        </div>
    </div>
</div>
</body></html>
""",

    "cf_phase2_output": f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{COMMON_CSS}</style></head>
<body>
<div class="capture-box" style="width: 980px;">
    <div class="sub-container">
        <span class="sub-title">3. System Output &amp; Explainable Reporting</span>
        
        <div style="display: flex; flex-direction: column; align-items: center; margin-top: 4px;">
            
            <!-- Transparency View -->
            <div class="academic-box" style="width: 88%; margin-bottom: 8px; border-style: dashed; background-color: #f8fafc;">
                <span class="box-title" style="letter-spacing: 0.3px;">STAGE 1 RETRIEVAL TRANSPARENCY: SHORTLISTED STATUTES</span>
                <span class="box-desc">Ranked Top-<i>k</i> candidate national and municipal provisions displayed with similarity scores for legislative auditability</span>
            </div>

            <!-- Decision Diamond -->
            <div class="diamond-wrapper">
                <div class="academic-diamond">
                    <div class="diamond-text">
                        Contradiction<br>Probability<br><i>P</i>(<i>C</i>) &ge; &tau;*?
                    </div>
                </div>
                <div class="diamond-threshold-badge">
                    Calibrated Decision Threshold &tau;* (Cost-Sensitive Optimization for Recall Priority)
                </div>
            </div>

            <!-- Fork -->
            <div class="decision-fork">
                <div class="fork-line-center"></div>
                <div class="fork-line-h"></div>
                
                <div class="fork-drop-l"></div>
                <div class="fork-arrow-l"><div class="arrow-down"></div></div>
                <div class="fork-label-l">YES</div>

                <div class="fork-drop-r"></div>
                <div class="fork-arrow-r"><div class="arrow-down"></div></div>
                <div class="fork-label-r">NO</div>
            </div>

            <!-- Result Branches -->
            <div style="display: flex; justify-content: space-between; width: 100%; gap: 24px; padding: 0 10px;">
                
                <!-- Left: Conflict Detected -->
                <div style="flex: 1; display: flex; flex-direction: column; align-items: center;">
                    <div class="academic-box box-highlight" style="width: 100%; border: 2px solid #000;">
                        <span class="box-title" style="font-size: 13px;">FLAG SEMANTIC CONFLICT</span>
                        <span class="box-desc">Normative Legal Inconsistency Identified</span>
                    </div>

                    <div class="line-v-sm"></div><div class="arrow-down"></div>

                    <!-- Two-Tiered Alert -->
                    <div style="border: 1px solid #000; width: 100%; background: #ffffff; padding: 6px; box-sizing: border-box;">
                        <div style="font-size: 11px; font-weight: bold; text-align: center; margin-bottom: 4px; text-transform: uppercase;">
                            Two-Tiered Jurisdictional Conflict Classification
                        </div>
                        <div style="display: flex; gap: 6px;">
                            <div class="academic-box" style="flex: 1; padding: 6px 4px; background: #fef2f2; border: 1px solid #dc2626;">
                                <b style="font-size: 11px; color: #991b1b;">Critical Vertical Preemption Alert</b><br>
                                <span style="font-size: 9.5px; font-style: italic; color: #7f1d1d;">Superior National Law Collision<br>(<i>Magtajas</i> Doctrine / RA 7160 &sect;5(a))</span>
                            </div>
                            <div class="academic-box" style="flex: 1; padding: 6px 4px; background: #fffbeb; border: 1px solid #d97706;">
                                <b style="font-size: 11px; color: #92400e;">Horizontal Inconsistency Notice</b><br>
                                <span style="font-size: 9.5px; font-style: italic; color: #78350f;">Intra-Jurisdictional City Code Collision<br>(Ordinance Amendment &amp; Harmonization)</span>
                            </div>
                        </div>
                    </div>

                    <div class="line-v-sm"></div><div class="arrow-down"></div>

                    <div class="academic-box" style="width: 100%; background-color: #f8fafc;">
                        <span class="box-title">Intrinsic Structural Explainability (XAI)</span>
                        <span class="box-desc">Side-by-Side Comparative Spans, Highlighted Conflicting Clauses &amp; Calibrated Confidence %</span>
                    </div>
                </div>

                <!-- Right: Clear Draft -->
                <div style="flex: 1; display: flex; flex-direction: column; align-items: center;">
                    <div class="academic-box box-highlight" style="width: 100%; border: 2px solid #000;">
                        <span class="box-title" style="font-size: 13px;">CLEAR DRAFT MEASURE</span>
                        <span class="box-desc" style="font-weight: bold; font-size: 11px; margin-top: 3px; color: #047857;">(Legislative Compliance Confirmed)</span>
                    </div>

                    <div class="line-v-sm"></div><div class="arrow-down"></div>

                    <!-- Statutory Clearance Audit Box -->
                    <div style="border: 1px solid #000; width: 100%; background: #ffffff; padding: 6px; box-sizing: border-box;">
                        <div style="font-size: 11px; font-weight: bold; text-align: center; margin-bottom: 4px; text-transform: uppercase;">
                            Statutory Clearance &amp; Traceability Audit
                        </div>
                        <div style="display: flex; gap: 6px;">
                            <div class="academic-box" style="flex: 1; padding: 6px 4px; background: #f0fdf4; border: 1px solid #16a34a;">
                                <b style="font-size: 11px; color: #166534;">Verified National Harmony</b><br>
                                <span style="font-size: 9.5px; font-style: italic; color: #14532d;">Absence of Negative Preemption<br>(Valid Exercise of Police Power)</span>
                            </div>
                            <div class="academic-box" style="flex: 1; padding: 6px 4px; background: #f0fdf4; border: 1px solid #16a34a;">
                                <b style="font-size: 11px; color: #166534;">Local Coherence Verified</b><br>
                                <span style="font-size: 9.5px; font-style: italic; color: #14532d;">No Unintended Repeal or Conflict<br>(Coexists with Davao City Codes)</span>
                            </div>
                        </div>
                    </div>

                    <div class="line-v-sm"></div><div class="arrow-down"></div>

                    <div class="academic-box" style="width: 100%; background-color: #f8fafc;">
                        <span class="box-title">Audit Trail &amp; Enactment Clearance</span>
                        <span class="box-desc">Automated Clearance Certificate &amp; Full Candidate Verification Log for City Council Reporting</span>
                    </div>
                </div>

            </div>

        </div>
    </div>
</div>
</body></html>
"""
}


def render_html_to_png(html_text: str, target_png: Path, window_size: str = "1200,1600") -> None:
    temp_html = ROOT / "temp_cf_render.html"
    temp_png = ROOT / "temp_cf_render.png"
    
    temp_html.write_text(html_text, encoding="utf-8")
    
    subprocess.run([
        EDGE_PATH,
        "--headless",
        f"--window-size={window_size}",
        "--force-device-scale-factor=3",
        "--hide-scrollbars",
        f"--screenshot={temp_png}",
        f"file:///{str(temp_html).replace(os.sep, '/')}"
    ], capture_output=True, check=True)
    
    # Auto-crop with PIL
    im = Image.open(temp_png)
    gray = im.convert("L")
    inv = gray.point(lambda p: 255 if p < 248 else 0)
    bbox = inv.getbbox()
    if bbox:
        pad = 20
        crop_box = (
            max(0, bbox[0] - pad),
            max(0, bbox[1] - pad),
            min(im.size[0], bbox[2] + pad),
            min(im.size[1], bbox[3] + pad)
        )
        final_im = im.crop(crop_box)
        final_im.save(target_png, "PNG")
        print(f"Generated high-res {target_png.name} ({final_im.size[0]}x{final_im.size[1]} px)")
    else:
        im.save(target_png, "PNG")
        print(f"Saved uncropped {target_png.name}")
        
    if temp_html.exists():
        temp_html.unlink()
    if temp_png.exists():
        temp_png.unlink()


def main():
    FIGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Render the 6 standalone component figures
    window_sizes = {
        "cf_phase1_ingestion": "700,900",
        "cf_phase1_benchmarking": "700,900",
        "cf_phase2_input": "1150,500",
        "cf_phase2_stage1": "1150,800",
        "cf_phase2_stage2": "1150,700",
        "cf_phase2_output": "1150,1100",
    }
    
    for name, html_content in TEMPLATES.items():
        out_path = FIGS_DIR / f"{name}.png"
        w_size = window_sizes.get(name, "1200,1600")
        render_html_to_png(html_content, out_path, window_size=w_size)

    # Also re-run scripts/render_flowchart.py to ensure the master flowchart is cleansed of "protocol"
    print("\nUpdating master conceptual_framework_flowchart.png with cleansed subtitles...")
    rf_script = ROOT / "scripts" / "render_flowchart.py"
    if rf_script.exists():
        rf_text = rf_script.read_text(encoding="utf-8")
        # Cleans buzzword "protocol" in subtitles
        rf_text = rf_text.replace("Offline Foundation & Optimization Protocol", "Offline Foundation & Optimization Framework")
        rf_text = rf_text.replace("Dual-Corpus Ingestion & Pre-Computation Protocol", "Dual-Corpus Ingestion & Pre-Computation Pipeline")
        rf_text = rf_text.replace("Model Evaluation Benchmark & Selection Protocol", "Model Evaluation Benchmark & Selection Framework")
        rf_script.write_text(rf_text, encoding="utf-8")
        
        subprocess.run(["python", str(rf_script)], capture_output=True, check=True)
        print("Updated master conceptual_framework_flowchart.png successfully!")


if __name__ == "__main__":
    main()
