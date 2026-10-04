"""
compare_with_gemini.py
======================
Automated OCR Benchmark Workflow: LocalLLM vs. Gemini AI Baseline.
Renders PDF pages to images, queries the Gemini API for a verbatim legal transcription,
computes Word Error Rate (WER) and Character Error Rate (CER), and generates a side-by-side
discrepancy report for rapid human verification.

Zero-bloat execution: runs locally, calls Gemini API via lightweight HTTPS, and isolates scratch images.
"""

import os
import sys
import re
import json
import base64
import difflib
import subprocess
import time
import requests
from typing import List, Tuple, Dict, Any


def levenshtein(s1: List[str], s2: List[str]) -> int:
    """Calculates Levenshtein distance between two token lists."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def calculate_wer_cer(ref: str, hyp: str) -> Tuple[float, float]:
    ref_words = ref.split()
    hyp_words = hyp.split()
    wer = levenshtein(ref_words, hyp_words) / max(len(ref_words), 1)

    ref_chars = list(ref)
    hyp_chars = list(hyp)
    cer = levenshtein(ref_chars, hyp_chars) / max(len(ref_chars), 1)
    return round(wer * 100.0, 2), round(cer * 100.0, 2)


def render_pdf_to_images(pdf_path: str, scratch_dir: str) -> List[str]:
    """Renders PDF pages to PNG images using pdftoppm."""
    os.makedirs(scratch_dir, exist_ok=True)
    base_prefix = os.path.join(scratch_dir, "page")
    cmd = ["pdftoppm.exe", "-png", "-r", "150", pdf_path, base_prefix]
    subprocess.run(cmd, check=True, capture_output=True)
    
    # Collect rendered PNG files sorted by page number
    png_files = []
    for f in os.listdir(scratch_dir):
        if f.startswith("page-") and f.endswith(".png"):
            png_files.append(os.path.join(scratch_dir, f))
    png_files.sort(key=lambda x: int(re.search(r'page-(\d+)\.png', x).group(1)))
    return png_files


def transcribe_page_with_gemini(image_path: str, api_key: str, primary_model: str = "gemini-3.8-flash") -> str:
    """Sends a single page image to Gemini for verbatim legal transcription with robust retries and fallbacks."""
    with open(image_path, "rb") as f:
        encoded_img = base64.b64encode(f.read()).decode("utf-8")

    prompt = (
        "You are an expert archival paleographer and legal document transcriber. "
        "Transcribe the exact legal text from this historical Philippine municipal ordinance scan verbatim. "
        "Preserve all section headers (e.g., SECTION 1, SEC. 2), ordinance numbers, monetary amounts, "
        "dates, and official signatures exactly as typed or printed. "
        "Do not summarize, do not modernize historical phrasing, and do not invent text. "
        "Output ONLY the transcribed plain text."
    )

    models_to_try = [primary_model, "gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-flash-latest"]
    last_err = None

    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": encoded_img
                        }
                    }
                ]
            }],
            "generationConfig": {
                "temperature": 0.0,
                "maxOutputTokens": 2048
            }
        }

        for attempt in range(2):
            try:
                response = requests.post(url, json=payload, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    return text
                elif response.status_code in [503, 429]:
                    last_err = f"HTTP {response.status_code} ({model}): {response.text[:120]}"
                    print(f"    [Notice] {model} high demand ({response.status_code}), trying fallback...", flush=True)
                    time.sleep(1.5)
                else:
                    last_err = f"HTTP {response.status_code} ({model}): {response.text[:120]}"
                    break
            except Exception as e:
                last_err = f"Exception ({model}): {str(e)}"
                time.sleep(1)

    raise RuntimeError(f"Gemini API transcription failed across candidate models: {last_err}")


def run_comparison(pdf_name: str):
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pdf_path = os.path.join(repo_root, "flagged pdfs", pdf_name)
    scratch_dir = os.path.join(repo_root, "scratch", "ocr_compare")
    output_benchmark_dir = os.path.join(repo_root, "data", "ocr_benchmark_samples")
    os.makedirs(output_benchmark_dir, exist_ok=True)
    os.makedirs(scratch_dir, exist_ok=True)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not found.")
        sys.exit(1)

    if not os.path.exists(pdf_path):
        print(f"Error: PDF '{pdf_path}' not found.")
        sys.exit(1)

    print(f"=== Running Multi-Model Archival OCR Benchmark for: {pdf_name} ===")

    # 1. Load LocalLLM transcription
    base_no_ext = os.path.splitext(pdf_name)[0]
    local_txt_path = os.path.join(repo_root, "vlm_transcriptions", f"{base_no_ext}.txt")
    if not os.path.exists(local_txt_path):
        # Fallback to cleaned_transcriptions
        local_txt_path = os.path.join(repo_root, "cleaned_transcriptions", f"{base_no_ext}.txt")

    if not os.path.exists(local_txt_path):
        print(f"Error: Local transcription not found for {base_no_ext}.")
        sys.exit(1)

    with open(local_txt_path, "r", encoding="utf-8", errors="ignore") as f:
        localllm_raw = f.read().strip()

    # 2. Render pages to images
    print("[Step 1/3] Rendering PDF pages to high-resolution images...")
    page_images = render_pdf_to_images(pdf_path, scratch_dir)
    print(f"  Rendered {len(page_images)} page(s).")

    # 3. Transcribe each page with Gemini
    print("[Step 2/3] Transcribing pages via Gemini API (gemini-flash-latest)...")
    gemini_pages = []
    for idx, img_path in enumerate(page_images, 1):
        print(f"  Querying Gemini for Page {idx}/{len(page_images)}...")
        page_text = transcribe_page_with_gemini(img_path, api_key)
        gemini_pages.append(f"--- [Page {idx}] ---\n{page_text}")

    gemini_full_text = "\n\n".join(gemini_pages).strip()

    # Save Gemini transcription
    gemini_out_path = os.path.join(output_benchmark_dir, f"{base_no_ext}_gemini.txt")
    with open(gemini_out_path, "w", encoding="utf-8") as f:
        f.write(gemini_full_text)
    print(f"  Saved Gemini transcript to: {gemini_out_path}")

    # Save raw LocalLLM transcription to benchmark folder
    localllm_out_path = os.path.join(output_benchmark_dir, f"{base_no_ext}_localllm_raw.txt")
    with open(localllm_out_path, "w", encoding="utf-8") as f:
        f.write(localllm_raw)
    print(f"  Saved LocalLLM raw baseline to: {localllm_out_path}")

    # 4. Compare LocalLLM vs. Gemini
    print("[Step 3/3] Computing Comparative Error Rates & Identifying Discrepancies...")
    wer, cer = calculate_wer_cer(gemini_full_text, localllm_raw)
    print(f"\n========================================================")
    print(f"  Relative Word Error Rate (WER) vs. Gemini:    {wer}%")
    print(f"  Relative Character Error Rate (CER) vs. Gemini: {cer}%")
    print(f"========================================================\n")

    # Generate Unified Diff of Discrepancies
    diff_lines = list(difflib.unified_diff(
        localllm_raw.splitlines(),
        gemini_full_text.splitlines(),
        fromfile="LocalLLM (Qwen2.5-VL-3B-NF4)",
        tofile="Gemini 3.8 Flash (Cloud Baseline)",
        lineterm=""
    ))

    diff_report_path = os.path.join(output_benchmark_dir, f"{base_no_ext}_diff_report.txt")
    with open(diff_report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(diff_lines))
    print(f"  Saved discrepancy diff report to: {diff_report_path}\n")

    print("--- Key Discrepancies (LocalLLM [-] vs Gemini [+]): ---")
    diff_count = 0
    for line in diff_lines:
        if line.startswith("- ") or line.startswith("+ "):
            print(f"  {line}")
            diff_count += 1
            if diff_count >= 40:
                print("  ... [Remaining diff lines truncated in console, full diff saved to file] ...")
                break
    print("--------------------------------------------------------\n")

    # Clean up scratch images
    for img in page_images:
        try:
            os.remove(img)
        except Exception:
            pass

    return localllm_raw, gemini_full_text, wer, cer


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "Ordinance No. 000044-56.pdf"
    run_comparison(target)
