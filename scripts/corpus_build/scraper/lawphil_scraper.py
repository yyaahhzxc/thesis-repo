import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os
import logging
import re
import importlib
import pandas as pd
from datetime import datetime
from urllib.parse import urljoin

try:
    tiktoken = importlib.import_module("tiktoken")
except Exception:
    tiktoken = None

# --- LOGGING SETUP ---
logging.basicConfig(
    filename='scraper_errors.log', 
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- DEFAULT CONFIGURATION ---
DEFAULT_CONFIG = {
    "Republic Acts": {
        "start": 1946, "end": 2025,
        "base_url": "https://lawphil.net/statutes/repacts",
        "index_pattern": "ra{year}/ra{year}.html",
        "prefix_indicators": ["ra_"],
        "default_filename": "republic_acts.jsonl"
    },
    "Acts": {
        "start": 1900, "end": 1935,
        "base_url": "https://lawphil.net/statutes/acts",
        "index_pattern": "act{year}/act{year}.html",
        "prefix_indicators": ["act_"],
        "default_filename": "acts.jsonl"
    },
    "Commonwealth Acts": {
        "start": 1935, "end": 1946,
        "base_url": "https://lawphil.net/statutes/comacts",
        "index_pattern": "ca{year}/ca{year}.html",
        "prefix_indicators": ["ca_", "comact_"],
        "default_filename": "commonwealth_acts.jsonl"
    },
    "Presidential Decrees": {
        "start": 1972, "end": 1986,
        "base_url": "https://lawphil.net/statutes/presdecs",
        "index_pattern": "pd{year}/pd{year}.html",
        "prefix_indicators": ["pd_"],
        "default_filename": "presidential_decrees.jsonl"
    },
    "Executive Orders": {
        "start": 1966, "end": 2025,
        "base_url": "https://lawphil.net/executive/execord",
        "index_pattern": "eo{year}/eo{year}.html",
        "prefix_indicators": ["eo_"],
        "default_filename": "executive_orders.jsonl"
    },
    "Batas Pambansa": {
        "start": 1978, "end": 1986,
        "base_url": "https://lawphil.net/statutes/bataspam",
        "index_pattern": "bp{year}/bp{year}.html",
        "prefix_indicators": ["bp_"],
        "default_filename": "batas_pambansa.jsonl"
    }
}

FILE_MAP_STORAGE = "file_map_config.json"

def load_file_map_from_disk():
    default_map = {k: v['default_filename'] for k, v in DEFAULT_CONFIG.items()}
    if not os.path.exists(FILE_MAP_STORAGE):
        return default_map
    try:
        with open(FILE_MAP_STORAGE, 'r', encoding='utf-8') as f:
            stored = json.load(f)
        if not isinstance(stored, dict):
            return default_map
        merged = default_map.copy()
        for cat in default_map:
            value = stored.get(cat)
            if isinstance(value, str) and value.strip():
                merged[cat] = value.strip()
        return merged
    except Exception:
        return default_map

def save_file_map_to_disk(file_map):
    with open(FILE_MAP_STORAGE, 'w', encoding='utf-8') as f:
        json.dump(file_map, f, ensure_ascii=False, indent=2)

class LawPhilScraper:
    def __init__(self, file_config):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        self.file_config = file_config
        self.existing_ids = self._load_all_checkpoints()

    def _load_all_checkpoints(self):
        ids = set()
        for cat, filename in self.file_config.items():
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            ids.add(data.get('law_id'))
                        except: continue
        return ids

    def robust_get(self, url, retries=3):
        for attempt in range(retries):
            try:
                time.sleep(random.uniform(1.0, 2.5))
                response = self.session.get(url, timeout=20)
                if response.encoding == 'ISO-8859-1':
                    response.encoding = 'cp1252' 
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to fetch {url}: {e}")
                time.sleep(2 * (attempt + 1))
        return None

    def get_links(self, category, year):
        cfg = DEFAULT_CONFIG[category]
        target_url = f"{cfg['base_url']}/{cfg['index_pattern'].format(year=year)}"
        
        response = self.robust_get(target_url)
        if not response:
            return []

        soup = BeautifulSoup(response.text, 'lxml')
        links = []

        for a in soup.find_all('a', href=True):
            href = a['href']
            if any(ind in href.lower() for ind in cfg['prefix_indicators']) and '.html' in href.lower():
                if 'index.html' in href.lower() or href.endswith(cfg['index_pattern'].format(year=year).split('/')[-1]):
                    continue

                full_url = urljoin(response.url, href)
                law_id = href.split('/')[-1].replace('.html', '')
                
                if law_id:
                    links.append({
                        "law_id": law_id,
                        "url": full_url,
                        "year": year,
                        "category": category
                    })
        return links

    # RESTORED TO PROVEN VERSION
    def extract_text(self, url):
        response = self.robust_get(url)
        if not response: 
            return None

        soup = BeautifulSoup(response.text, 'lxml')

        # Cleaning: Removed 'center' to preserve older law texts
        for tag in soup(["script", "style", "header", "footer", "iframe"]):
            tag.decompose()

        text = soup.body.get_text(separator='\n') if soup.body else soup.get_text(separator='\n')
        
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(lines)
        return clean_text

    def save_record(self, record, category):
        filename = self.file_config[category]
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def sort_file(self, category):
        filename = self.file_config[category]
        if not os.path.exists(filename): return 0
        data = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                try: data.append(json.loads(line))
                except: continue
        
        data.sort(key=lambda x: (x.get('year', 0), int(re.search(r'\d+', x.get('law_id', '0')).group() if re.search(r'\d+', x.get('law_id', '')) else 0)))
        
        with open(filename, 'w', encoding='utf-8') as f:
            for r in data: f.write(json.dumps(r, ensure_ascii=False) + "\n")
        return len(data)

    def check_missing(self, category):
        filename = self.file_config[category]
        if not os.path.exists(filename): return None
        nums = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                try: 
                    d = json.loads(line)
                    m = re.search(r'\d+', d.get('law_id', ''))
                    if m: nums.append(int(m.group()))
                except: continue
        if not nums: return None
        
        nums = sorted(set(nums))
        full_set = set(range(nums[0], nums[-1] + 1))
        missing = sorted(list(full_set - set(nums)))
        return {
            "range": f"{nums[0]} - {nums[-1]}",
            "count": len(missing),
            "examples": missing
        }

    def rename_file_on_disk(self, category, new_name):
        old_name = self.file_config[category]
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
            return True, f"Renamed {old_name} to {new_name}"
        return False, "Original file not found."

    def _count_tokens(self, text):
        if not text: return 0
        if tiktoken is not None:
            try:
                enc = tiktoken.get_encoding("cl100k_base")
                return len(enc.encode(text))
            except Exception: pass
        return len(re.findall(r"\S+", text))

    def get_corpus_stats(self, category):
        filename = self.file_config[category]
        if not os.path.exists(filename): return None
        entries = []
        total_chars = total_words = total_tokens = 0
        min_year = float('inf')
        max_year = 0
        latest_scrape = None
        
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    record = json.loads(line)
                    text = (record.get('text') or '').strip()
                    if not text: continue
                    
                    year = record.get('year')
                    if isinstance(year, int):
                        min_year = min(min_year, year)
                        max_year = max(max_year, year)
                        
                    scraped_at_str = record.get('scraped_at')
                    if scraped_at_str:
                        dt = datetime.fromisoformat(scraped_at_str)
                        if latest_scrape is None or dt > latest_scrape:
                            latest_scrape = dt
                    
                    chars = len(text)
                    words = len(re.findall(r"\S+", text))
                    tokens = self._count_tokens(text)
                    
                    total_chars += chars
                    total_words += words
                    total_tokens += tokens
                    
                    entries.append({
                        "law_id": record.get('law_id', 'unknown'),
                        "year": record.get('year', 'unknown'),
                        "chars": chars,
                        "words": words,
                        "tokens": tokens,
                    })
                except Exception: continue

        valid_entries = len(entries)
        if valid_entries == 0:
            return {"valid_entries": 0}

        sorted_by_chars = sorted(entries, key=lambda x: x['chars'])
        return {
            "valid_entries": valid_entries,
            "avg_chars": total_chars / valid_entries,
            "avg_words": total_words / valid_entries,
            "avg_tokens": total_tokens / valid_entries,
            "shortest_top5": sorted_by_chars[:5],
            "longest_top5": sorted_by_chars[::-1][:5],
            "year_range": f"{min_year} - {max_year}" if min_year != float('inf') else "Unknown",
            "latest_scrape": latest_scrape.strftime("%Y-%m-%d %H:%M:%S") if latest_scrape else "Unknown"
        }

class BaseAlternativeScraper:
    name = "Base"
    def fetch_law(self, session, category, law_number):
        raise NotImplementedError

class ChanRoblesScraper(BaseAlternativeScraper):
    name = "ChanRobles Virtual Law Library"
    def fetch_law(self, session, category, law_number):
        if category != "Republic Acts":
            return None
        base_url = "https://laws.chanrobles.com/republicacts/7_republicacts.php?id="
        current_id = int(law_number)
        
        for _ in range(15): 
            url = f"{base_url}{current_id}"
            try:
                resp = session.get(url, timeout=10)
                if resp.status_code != 200:
                    return None
                soup = BeautifulSoup(resp.text, 'lxml')
                text = soup.get_text(separator='\n')
                match = re.search(r'REPUBLIC\s+ACT\s+NO\.?\s+(\d+)', text, re.IGNORECASE)
                if match:
                    found_num = int(match.group(1))
                    if found_num == int(law_number):
                        return text, url
                    elif found_num > int(law_number):
                        return None
                    else:
                        current_id += 1
                        continue
                else:
                    return None
            except:
                return None
        return None

class SenateScraper(BaseAlternativeScraper):
    name = "Senate Legislative Digital Resources"
    def fetch_law(self, session, category, law_number):
        if category != "Republic Acts":
            return None
        url = f"https://issuances-library.senate.gov.ph/legislative-issuance/republic-act-no-{law_number}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }
        try:
            resp = session.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                return None
            soup = BeautifulSoup(resp.text, 'lxml')
            for tag in soup(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            text = soup.get_text(separator='\n')
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            clean_text = "\n".join(lines)
            if len(clean_text) < 200 or str(law_number) not in clean_text:
                return None
            return clean_text, url
        except:
            return None

class SCElibraryScraper(BaseAlternativeScraper):
    name = "Supreme Court E-Library"
    def fetch_law(self, session, category, law_number):
        return None

class FallbackManager:
    def __init__(self, session, active_sources):
        self.session = session
        all_scrapers = [SenateScraper(), ChanRoblesScraper(), SCElibraryScraper()]
        self.scrapers = []
        for src_name in active_sources:
            for s in all_scrapers:
                if s.name == src_name:
                    self.scrapers.append(s)
                    break

    def resolve_missing(self, category, law_number):
        for scraper in self.scrapers:
            result = scraper.fetch_law(self.session, category, law_number)
            if result:
                text, url = result
                return text, url, scraper.name
        return None, None, None

# --- INITIALIZATION ---
if 'file_map' not in st.session_state:
    st.session_state['file_map'] = load_file_map_from_disk()

st.set_page_config(page_title="LawPhil Scraper", layout="wide")
st.title("LawPhil Corpus Builder")

# --- TABS ---
categories = list(DEFAULT_CONFIG.keys())
tabs = st.tabs(categories)

for idx, cat in enumerate(categories):
    with tabs[idx]:
        st.header(f"Manage: {cat}")
        
        # Nested tabs for better grouping
        t_file, t_db, t_scrape = st.tabs(["File & Data Management", "Database Viewer", "Scrape & Cross-Reference"])
        
        # -------------------------------------------------------------
        # FILE & DATA MANAGEMENT
        # -------------------------------------------------------------
        with t_file:
            st.subheader("File Operations")
            current_file = st.session_state['file_map'][cat]
            st.caption(f"Active file: {current_file}")
            
            f1, f2, f3 = st.columns(3)
            if f1.button("Locate / Initialize File", key=f"btn_loc_{cat}"):
                if not os.path.exists(current_file):
                    open(current_file, 'a', encoding='utf-8').close()
                    st.warning(f"File missing. Created new: {current_file}")
                else:
                    st.success(f"File found: {current_file}")

            if f2.button("Sort File", key=f"sf_{cat}"):
                s = LawPhilScraper(st.session_state['file_map'])
                st.success(f"Sorted {s.sort_file(cat)} laws.")
                
            if f3.button("Rename File", key=f"btn_start_ren_{cat}"):
                st.session_state[f"rename_mode_{cat}"] = True

            if st.session_state.get(f"rename_mode_{cat}", False):
                rename_target = st.text_input("New filename", value=current_file, key=f"ren_target_{cat}")
                r1, r2 = st.columns(2)
                if r1.button("Confirm Rename", key=f"btn_confirm_ren_{cat}"):
                    if rename_target.strip():
                        scraper = LawPhilScraper(st.session_state['file_map'])
                        success, msg = scraper.rename_file_on_disk(cat, rename_target.strip())
                        if success:
                            st.session_state['file_map'][cat] = rename_target.strip()
                            save_file_map_to_disk(st.session_state['file_map'])
                            st.session_state[f"rename_mode_{cat}"] = False
                            st.rerun()
                if r2.button("Cancel Rename", key=f"btn_cancel_ren_{cat}"):
                    st.session_state[f"rename_mode_{cat}"] = False
                    st.rerun()

            st.divider()
            
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Corpus Statistics")
                if st.button("Generate Stats", key=f"ls_{cat}"):
                    s = LawPhilScraper(st.session_state['file_map'])
                    stats = s.get_corpus_stats(cat)
                    if stats and stats['valid_entries'] > 0:
                        st.metric("Total Records", stats['valid_entries'])
                        
                        m1, m2 = st.columns(2)
                        m1.metric("Year Range", stats['year_range'])
                        m2.metric("Latest Scrape", stats['latest_scrape'])
                        
                        m3, m4, m5 = st.columns(3)
                        m3.metric("Avg Characters", f"{stats['avg_chars']:,.0f}")
                        m4.metric("Avg Words", f"{stats['avg_words']:,.0f}")
                        m5.metric("Avg Tokens", f"{stats['avg_tokens']:,.0f}")
                        
                        with st.expander("Show Extremes (Shortest & Longest)"):
                            st.write("**Top 5 Shortest**")
                            st.dataframe(pd.DataFrame(stats['shortest_top5']), use_container_width=True)
                            st.write("**Top 5 Longest**")
                            st.dataframe(pd.DataFrame(stats['longest_top5']), use_container_width=True)
                    else:
                        st.warning("No valid data to generate stats.")
                        
            with c2:
                st.subheader("Database Integrity")
                if st.button("Check Missing Laws", key=f"cm_{cat}"):
                    s = LawPhilScraper(st.session_state['file_map'])
                    res = s.check_missing(cat)
                    if res and res['count'] > 0:
                        st.warning(f"Missing {res['count']} files in range {res['range']}")
                        with st.container(height=300):
                            st.write(res['examples'])
                    else:
                        st.success("No missing files found.")

        # -------------------------------------------------------------
        # DATABASE VIEWER
        # -------------------------------------------------------------
        with t_db:
            fname = st.session_state['file_map'][cat]
            if os.path.exists(fname):
                try:
                    df = pd.read_json(fname, lines=True)
                    if not df.empty:
                        # Dynamic source fallback for older records
                        def populate_source(row):
                            if pd.isna(row.get('source')) or not row.get('source'):
                                url = str(row.get('url', ''))
                                if 'chanrobles' in url: return 'ChanRobles'
                                elif 'senate.gov' in url: return 'Senate'
                                elif 'judiciary' in url: return 'SC E-Library'
                                else: return 'LawPhil'
                            return row['source']
                        
                        if 'source' not in df.columns:
                            df['source'] = None
                        df['source'] = df.apply(populate_source, axis=1)

                        cols_order = ['law_id', 'year', 'source', 'url', 'text', 'scraped_at']
                        df = df[[c for c in cols_order if c in df.columns]]
                        
                        st.subheader(f"Data Browser ({len(df)} records)")
                        
                        # Pagination and filtering UI
                        col_pg1, col_pg2 = st.columns([1, 1])
                        page_size = col_pg1.selectbox("Rows per page", [10, 50, 100, 500], key=f"ps_{cat}")
                        total_pages = max(1, (len(df) - 1) // page_size + 1)
                        page = col_pg2.number_input("Page", min_value=1, max_value=total_pages, value=1, key=f"pg_{cat}")
                        
                        start_idx = (page - 1) * page_size
                        end_idx = start_idx + page_size
                        
                        # Display chunk with column configs
                        st.dataframe(
                            df.iloc[start_idx:end_idx],
                            use_container_width=True,
                            column_config={
                                "url": st.column_config.LinkColumn("URL"),
                                "text": st.column_config.TextColumn("Content", max_chars=100)
                            }
                        )
                        st.caption(f"Showing rows {start_idx + 1} to {min(end_idx, len(df))} of {len(df)}")
                    else:
                        st.info("The database is currently empty.")
                except Exception as e:
                    st.error(f"Failed to parse database: {e}")
            else:
                st.warning("Database file not found.")

        # -------------------------------------------------------------
        # SCRAPE & CROSS-REFERENCE
        # -------------------------------------------------------------
        with t_scrape:
            st.subheader("LawPhil Scraper Operations")
            cfg = DEFAULT_CONFIG[cat]
            sc1, sc2, sc3 = st.columns([1, 1, 2])
            start = sc1.number_input("Start Year", 1900, 2030, cfg['start'], key=f"s_{cat}")
            end = sc1.number_input("End Year", 1900, 2030, cfg['end'], key=f"e_{cat}")
            
            if sc2.button("Test Run (10 Random)", key=f"t_{cat}"):
                s = LawPhilScraper(st.session_state['file_map'])
                st_log = st.empty()
                st_log.info("Collecting available links...")
                
                # Fetch all links first
                all_links = []
                for y in range(start, end+1):
                    links = s.get_links(cat, y)
                    if links:
                        all_links.extend(links)
                
                if not all_links:
                    st.warning("No links found in the specified year range.")
                else:
                    # Randomly sample up to 10
                    sample_size = min(10, len(all_links))
                    sampled_links = random.sample(all_links, sample_size)
                    
                    st_log.info(f"Selected {sample_size} random laws for test run.")
                    preview_data = []
                    
                    for l in sampled_links:
                        if l['law_id'] in s.existing_ids: 
                            st_log.text(f"Skipping {l['law_id']} (Already in Database)")
                            continue
                            
                        st_log.info(f"Processing: {l['law_id']}")
                        txt = s.extract_text(l['url'])
                        
                        if txt:
                            l['text'] = txt
                            l['scraped_at'] = datetime.now().isoformat()
                            s.save_record(l, cat)
                            s.existing_ids.add(l['law_id'])
                            
                            st.write(f"Saved: {l['law_id']} ({len(txt)} characters)")
                            preview_data.append({
                                "Law ID": l['law_id'], 
                                "Year": l['year'], 
                                "Content Snippet": txt[:150] + "...",
                                "URL": l['url']
                            })
                            
                    if preview_data:
                        st.dataframe(pd.DataFrame(preview_data), use_container_width=True)
                    st.success("Test run completed.")

            if sc3.button("Full Run", key=f"r_{cat}"):
                s = LawPhilScraper(st.session_state['file_map'])
                prog = st.progress(0)
                st_log = st.empty()
                years = range(start, end+1)
                for i, y in enumerate(years):
                    st_log.info(f"Scanning Year Index: {y}...")
                    links = s.get_links(cat, y)
                    if not links:
                        prog.progress((i+1)/len(years))
                        continue
                    for l in links:
                        if l['law_id'] in s.existing_ids: 
                            st_log.text(f"Skipping {l['law_id']}")
                            continue
                        st_log.info(f"Processing: {l['law_id']}")
                        txt = s.extract_text(l['url'])
                        if txt:
                            l['text'] = txt
                            l['scraped_at'] = datetime.now().isoformat()
                            s.save_record(l, cat)
                            s.existing_ids.add(l['law_id'])
                            st_log.text(f"Saved: {l['law_id']} ({len(txt)} characters)")
                    prog.progress((i+1)/len(years))
                st.success("Full run completed.") 
                
            st.divider()
            
            st.subheader("Cross-Reference Alternative Sources")
            st.info("Check and reorder alternative sources (Drag Priority if needed). The system will check these in order for missing laws.")
            
            if f'alt_src_{cat}' not in st.session_state:
                st.session_state[f'alt_src_{cat}'] = pd.DataFrame({
                    "Enabled": [True, True, False],
                    "Source": ["Senate Legislative Digital Resources", "ChanRobles Virtual Law Library", "Supreme Court E-Library"],
                    "Priority": [1, 2, 3]
                })
                
            edited_df = st.data_editor(
                st.session_state[f'alt_src_{cat}'],
                hide_index=True,
                column_config={
                    "Enabled": st.column_config.CheckboxColumn("Enable", default=True),
                    "Source": st.column_config.TextColumn("Source", disabled=True),
                    "Priority": st.column_config.NumberColumn("Priority (1 is highest)", min_value=1, max_value=10, step=1)
                },
                key=f"editor_{cat}",
                use_container_width=True
            )
            st.session_state[f'alt_src_{cat}'] = edited_df
            
            if st.button("Run Alternative Scrape", key=f"alt_btn_{cat}"):
                active_df = edited_df[edited_df["Enabled"]].sort_values("Priority")
                active_sources = active_df["Source"].tolist()
                
                if not active_sources:
                    st.warning("Please enable at least one alternative source.")
                else:
                    s = LawPhilScraper(st.session_state['file_map'])
                    res = s.check_missing(cat)
                    if not res or res['count'] == 0:
                        st.success("No missing laws found for this category!")
                    else:
                        missing_ids = res['examples']
                        fm = FallbackManager(s.session, active_sources)
                        
                        st_log = st.empty()
                        prog = st.progress(0)
                        
                        found_count = 0
                        for i, missing_num in enumerate(missing_ids):
                            st_log.info(f"Searching for missing RA {missing_num}...")
                            text, url, source_name = fm.resolve_missing(cat, missing_num)
                            if text:
                                year_match = re.search(r'(?:19|20)\d{2}', text[:500])
                                year = int(year_match.group(0)) if year_match else 0
                                
                                # Use default law_id format if possible
                                cfg = DEFAULT_CONFIG[cat]
                                prefix = cfg['prefix_indicators'][0] if cfg['prefix_indicators'] else "law_"
                                law_id_str = f"{prefix.strip('_')}_{missing_num}"
                                
                                record = {
                                    "law_id": law_id_str,
                                    "year": year,
                                    "url": url,
                                    "text": text,
                                    "source": source_name,
                                    "scraped_at": datetime.now().isoformat()
                                }
                                s.save_record(record, cat)
                                found_count += 1
                                st_log.success(f"Found RA {missing_num} on {source_name}!")
                            else:
                                st_log.error(f"RA {missing_num} not found in alternatives.")
                            
                            prog.progress((i + 1) / len(missing_ids))
                        
                        st.success(f"Alternative scrape complete. Recovered {found_count} missing laws.")