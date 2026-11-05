# Running Davao Ordinances OCR on Kaggle (Free GPU)

This guide walks you through transcribing the remaining **349 ordinances (2020-2017, ~3,719 pages)** using Kaggle's free GPU compute with the exact same model (`Qwen2.5-VL-3B-Instruct` in 4-bit NF4) and formatting as your local pipeline.

---

## Why Kaggle?
- **Speed & Hardware**: Free NVIDIA T4 (16GB VRAM) or P100 with 30 GPU hours/week.
- **Background Execution**: You can submit the job to run in the background (headless) up to 12 hours. You can close your laptop or shut down your PC while it runs.
- **Estimated Time**: At ~2.5 - 3.5 seconds/page, 3,719 pages will take roughly **2.5 to 3.5 hours** (well within Kaggle's 12-hour limit).

---

## 3-Step Workflow

### Step 1: Upload the PDF Dataset to Kaggle
1. Run the local packaging script (or use the pre-generated zip in `kaggle/city_ordinances_2020_2017.zip`):
   ```bash
   python kaggle/prepare_dataset.py
   ```
2. Log in to [Kaggle](https://www.kaggle.com).
3. In the left navigation, click **Datasets** -> **New Dataset** (or go directly to [kaggle.com/datasets](https://www.kaggle.com/datasets)).
4. Drag and drop `kaggle/city_ordinances_2020_2017.zip`.
5. Enter a dataset title: **`davao-ordinances-2020-2017`**.
6. Set visibility to **Private**.
7. Click **Create**. Kaggle will upload and extract the files in the cloud.

---

### Step 2: Create & Run the Notebook on Kaggle
1. On Kaggle, click **Create** (+) in the top bar -> **New Notebook**.
2. Upload the ready-made notebook:
   - Click **File** -> **Import Notebook** in the top menu.
   - Choose `kaggle/kaggle_qwen_ocr.ipynb` from your project folder.
3. Attach your dataset:
   - On the right sidebar, under **Input**, click **+ Add Input** (or **+ Add Data**).
   - Click **Your Datasets** -> select **`davao-ordinances-2020-2017`** -> click **Add**.
4. Configure Kaggle Notebook Settings (right sidebar):
   - **Accelerator**: `GPU T4 x 2` or `GPU P100` (Crucial!)
   - **Internet**: **ON** (Toggle on! Crucial for HuggingFace model download & pip packages)
5. **Run in Background (Recommended)**:
   - Click the blue **"Save Version"** button in the top right.
   - Choose Version type: **"Save & Run All (Commit)"**.
   - Click **Save**.
   - Kaggle will run the entire batch in the cloud. You can safely close your browser!
   - You can monitor progress anytime by viewing the notebook's run logs.

---

### Step 3: Download & Integrate Results
1. Once Kaggle finishes, open your notebook page.
2. In the right panel under **Output** (or the **Version History** -> latest run -> Output), find:
   - **`vlm_transcriptions_2020_2017.zip`**
3. Click the download icon next to the zip file.
4. Move or leave the downloaded zip in your `Downloads/` or inside the `kaggle/` folder.
5. Run the automatic integration script:
   ```bash
   python kaggle/integrate_results.py
   ```
   *(Or pass the path directly: `python kaggle/integrate_results.py "C:\Users\...\Downloads\vlm_transcriptions_2020_2017.zip"`)*
6. This extracts all files directly into `vlm_transcriptions/` with the exact directory structure (`2016`, `2017`, `2018`, `2019`, `2020`).
7. Run your existing cleaning and audit scripts locally:
   ```bash
   python clean_transcripts.py
   python audit_transcripts.py
   ```
