# ==============================================================================
# 0. HARDCODED CACHE REDIRECTION (D: DRIVE ENFORCEMENT)
# ==============================================================================
import os
import sys

# Guarantee Hugging Face and PyTorch write to D: drive
os.environ["HF_HOME"] = r"D:\ai_cache\huggingface"
os.environ["TORCH_HOME"] = r"D:\ai_cache\torch"
os.environ["PIP_CACHE_DIR"] = r"D:\ai_cache\pip"
os.environ["HF_HUB_CACHE"] = r"D:\ai_cache\huggingface\hub"
os.environ["HF_DATASETS_CACHE"] = r"D:\ai_cache\huggingface\datasets"

import time
import gc
import argparse
from pathlib import Path

# Keep model caches on the D: drive
os.environ["HF_HOME"] = r"D:\ai_cache\huggingface"
os.environ["TORCH_HOME"] = r"D:\ai_cache\torch"
os.environ["PIP_CACHE_DIR"] = r"D:\ai_cache\pip"

import torch
import pymupdf
from PIL import Image
from transformers import (
    Qwen2_5_VLForConditionalGeneration,
    AutoProcessor,
    BitsAndBytesConfig,
)
from qwen_vl_utils import process_vision_info


# ==============================================================================
# 1. DIRECTORY CONFIGURATION
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_PDF_DIR = (
    BASE_DIR
    / "corpus"
    / "city_ordinances"
    / "City Ordinances (2025-2021)"
)

OUTPUT_TXT_DIR = BASE_DIR / "vlm_transcriptions"

INPUT_PDF_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_TXT_DIR.mkdir(parents=True, exist_ok=True)
Path(r"D:\ai_cache\huggingface").mkdir(parents=True, exist_ok=True)

if not torch.cuda.is_available():
    raise RuntimeError(
        "CUDA GPU is required for this 4-bit Qwen VLM pipeline."
    )

DEVICE = "cuda"
MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct"


# ==============================================================================
# 2. LOAD MODEL
# ==============================================================================

print("=" * 65)
print("[*] Starting Davao Ordinance VLM OCR Pipeline")
print(f"[*] Compute Target:     {torch.cuda.get_device_name(0)}")
print(f"[*] Hugging Face Cache: {os.environ['HF_HOME']}")
print(f"[*] Model:              {MODEL_ID} (4-Bit NF4)")
print(f"[*] Input Directory:    {INPUT_PDF_DIR}")
print(f"[*] Output Directory:   {OUTPUT_TXT_DIR}")
print("=" * 65)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

print("[*] Loading 4-bit model...")

model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto",
    low_cpu_mem_usage=True,
    attn_implementation="sdpa",
)

model.eval()

processor = AutoProcessor.from_pretrained(
    MODEL_ID,
    min_pixels=256 * 28 * 28,
    max_pixels=448 * 28 * 28,
)

print("[✓] Model and processor loaded successfully.\n")


# ==============================================================================
# 3. PAGE TRANSCRIPTION
# ==============================================================================

def transcribe_page(pil_image: Image.Image) -> str:
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": pil_image,
                },
                {
                    "type": "text",
                    "text": (
                        "Transcribe the legal text on this page completely and "
                        "verbatim. Preserve exact section titles, ordinals, "
                        "numbers, dates, names, and currency amounts. "
                        "Do not summarize, omit provisions, or add commentary."
                    ),
                },
            ],
        }
    ]

    text_prompt = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    image_inputs, video_inputs = process_vision_info(messages)

    inputs = processor(
        text=[text_prompt],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    ).to(DEVICE)

    with torch.inference_mode():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=1000,
            do_sample=False,
            use_cache=True,
        )

    trimmed_ids = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(
            inputs.input_ids,
            generated_ids,
        )
    ]

    transcription = processor.batch_decode(
        trimmed_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0]

    return transcription.strip()


# ==============================================================================
# 4. PDF PROCESSING
# ==============================================================================

def process_pdf_document(pdf_path: Path, output_path: Path) -> None:
    print(f"[*] Opening: {pdf_path.name}")

    document = pymupdf.open(pdf_path)
    total_pages = len(document)
    page_records = []

    try:
        for page_index in range(total_pages):
            start_time = time.time()
            page = document.load_page(page_index)

            rect = page.rect
            crop_box = pymupdf.Rect(
                rect.width * 0.03,
                rect.height * 0.03,
                rect.width * 0.97,
                rect.height * 0.97,
            )
            page.set_cropbox(crop_box)

            pixmap = page.get_pixmap(dpi=105)

            image = Image.frombytes(
                "RGB",
                [pixmap.width, pixmap.height],
                pixmap.samples,
            )

            page_text = transcribe_page(image)

            page_records.append(
                f"--- [Page {page_index + 1}] ---\n{page_text}"
            )

            del pixmap
            del image
            del page

            elapsed = time.time() - start_time

            print(
                f"      -> Page {page_index + 1}/{total_pages} "
                f"transcribed in {elapsed:.1f}s"
            )

    finally:
        document.close()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as output_file:
        output_file.write(
            f"=== ORDINANCE: {pdf_path.stem} ===\n\n"
        )
        output_file.write("\n\n".join(page_records))

    gc.collect()
    torch.cuda.empty_cache()


# ==============================================================================
# 5. DISPATCHER AND RESUME LOGIC
# ==============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Qwen2.5-VL OCR on city ordinance PDFs."
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Process only the first three PDFs.",
    )

    args = parser.parse_args()

    all_pdfs = sorted(
        path
        for path in INPUT_PDF_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() == ".pdf"
    )

    if not all_pdfs:
        print(f"[-] No PDF files found in: {INPUT_PDF_DIR}")
        sys.exit(1)

    target_queue = all_pdfs[:3] if args.test else all_pdfs

    print(
        f"[*] Queue Size: {len(target_queue)} file(s) "
        f"(Mode: {'TEST' if args.test else 'FULL BATCH'})"
    )
    print(f"[*] Input Path:  {INPUT_PDF_DIR}")
    print(f"[*] Output Path: {OUTPUT_TXT_DIR}\n")

    overall_start = time.time()

    for index, pdf_path in enumerate(target_queue, start=1):
        relative_path = pdf_path.relative_to(INPUT_PDF_DIR)
        output_path = (
            OUTPUT_TXT_DIR
            / relative_path.with_suffix(".txt")
        )

        if output_path.exists() and output_path.stat().st_size > 100:
            print(
                f"[{index}/{len(target_queue)}] "
                f"Skipping completed file: {relative_path}"
            )
            continue

        print(
            f"[{index}/{len(target_queue)}] "
            f"Processing: {relative_path}"
        )

        file_start = time.time()

        try:
            process_pdf_document(pdf_path, output_path)

            duration = time.time() - file_start

            print(
                f"   -> [✓] Saved: {output_path} "
                f"({duration:.1f}s)"
            )

        except Exception as error:
            print(
                f"   -> [X] Failed on {relative_path}: {error}"
            )

    total_time = time.time() - overall_start

    print("\n" + "=" * 65)
    print(f"[✓] Pipeline finished in {total_time / 60:.2f} minutes.")
    print(f"[✓] Transcripts saved in: {OUTPUT_TXT_DIR}")
    print("=" * 65)


if __name__ == "__main__":
    main()