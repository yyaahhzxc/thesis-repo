# LawPhil Scraper

A lightweight Streamlit-based scraper for building a JSONL corpus of Philippine Republic Acts from LawPhil.

The app scans yearly index pages, collects law links, extracts cleaned text content, and appends results into a local dataset (`lawphil_corpus.jsonl`). It also supports a small test run mode before you launch a full scrape.

## Tech Stack

- **Python** (main language)
- **Streamlit** (simple web UI)
- **Requests** (HTTP requests)
- **BeautifulSoup4 + lxml** (HTML parsing)
- **Pandas** (preview table in UI)
- **JSONL** (output format for corpus records)

## Project Structure

- `lawphil_scraper.py` — main Streamlit app + scraping logic
- `lawphil_corpus.jsonl` — scraped output data (append-only)
- `scraper_errors.log` — error logs from failed requests

## Setup

1. Open this folder in your terminal.
2. (Recommended) Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install streamlit requests beautifulsoup4 lxml pandas
```

## Run the App

```bash
streamlit run lawphil_scraper.py
```
or
``` bash
python -m streamlit run lawphil_scraper.py
```

After running, Streamlit will open in your browser.

## How to Use

1. Choose a **Start Year** and **End Year** in the sidebar.
2. Click **Run Test (First 5 Only)** to do a small sanity check.
3. Click **Start Full Scrape** for full collection.

Notes:
- Full scrape mode skips laws that already exist in `lawphil_corpus.jsonl`.
- Data is saved as one JSON object per line (JSONL), useful for downstream NLP or analysis workflows.

## Output Record Format

Each saved record includes:
- `law_id`
- `year`
- `url`
- `text`
- `scraped_at`

---

This project keeps things intentionally straightforward: just enough engineering to be reproducible, inspectable, and easy to extend for legal-text research.