

# 🔍 SDR/BDR Job Aggregator & Dashboard

A robust Python-based web scraping and automation framework that collects, merges, and visualizes Sales Development Representative (SDR) and Business Development Representative (BDR) job listings from **Jobspresso**, **Naukri**, and **Talent.com**, with automated scheduling and an interactive Streamlit frontend.

---

## 🚀 Project Overview

This end-to-end system consists of:

* **Scraper Modules**: Extract SDR/BDR jobs from multiple portals using Selenium and BeautifulSoup.
* **Data Cleaning & Enrichment**: Adds experience level, outreach tools used, and posted dates.
* **Pipeline Automation**: Scheduled backend automation to scrape, merge, deduplicate, and log results.
* **Frontend Dashboard**: A Streamlit-based web interface to filter, search, and explore jobs visually.

---


## ⚙️ Backend Logic

Each scraper (`jobspresso.py`, `naukri.py`, `talent.py`) performs the following:

* Uses **Selenium** (Jobspresso, Naukri) or **Requests + BeautifulSoup** (Talent.com)
* Parses HTML to extract:

  * Title, Company, Location, Logo
  * Experience level (via regex parsing job description)
  * Outreach tools (Salesforce, Hubspot, etc.)
  * Remote/On-site/Hybrid status
  * Posting date, and “Refreshed This Week” flag
* Deduplicates by `Job URL`, standardizes formats, and writes to CSV

The **`pipeline.py`** script:

* Runs each scraper as a subprocess
* Merges their outputs into a single unified file (`merged_jobs.csv`)
* Standardizes fields, deduplicates on `Job Title + Company + Location`
* Logs detailed run history to `scraper_log.txt`
* Supports optional Airtable integration (commented out for now)
* Scheduled to run **once every hour for 24 hours** via the `schedule` module

---

## 💻 Streamlit Frontend

The `job-scraper-app.py` UI offers:

* 🔎 Keyword search with real-time filtering
* 🏢 Filters by portal, experience level, remote type, date range, tools, and industry
* 🆕 Refresh button (triggered via subprocess to `pipeline.py`)
* 📊 Visual indicators for experience level and remote work
* 🔗 Clickable job links and badge-style tags for tech stack/tools

---

## ⏱️ Automation & Scheduler

The `pipeline.py` includes a `run_scheduler()` function configured to:

* Run the entire scraping + merge job **hourly for 24 hours**
* Persist logs and progress in `scraper_log.txt`
* Easily extensible for production-level cron integration

---

## 📦 Sample Output

The merged output file (`merged_jobs.csv`) contains:

| Job Title | Company | Location | Experience Level | Tools Tags          | Remote | Date Posted | Job URL      |
| --------- | ------- | -------- | ---------------- | ------------------- | ------ | ----------- | ------------ |
| SDR       | ABC Inc | Remote   | Entry-level      | Salesforce, HubSpot | Remote | 2025-06-28  | https\://... |

---

## ✅ Skills & Tools Demonstrated

* Python (Selenium, Requests, BeautifulSoup, Pandas)
* Data aggregation, cleansing, and regex pattern matching
* Automation with `subprocess`, `schedule`, and logging
* Frontend with **Streamlit**, including styling and dynamic UI controls
* CSV & API-ready output (Airtable integration stubbed)

---

## 🧠 Motivation

This project was built to simplify the job discovery process for aspiring SDRs and BDRs by programmatically pulling listings from fragmented sources, enriching them with context, and making them easily explorable through an elegant interface.

---

## 📎 How to Run

```bash
# (1) Activate virtual environment
source ./Scripts/activate  # or your env setup

# (2) Run the pipeline once
python pipeline.py

# (3) Launch frontend
streamlit run job-scraper-app.py
```

---

Let me know if you'd like a visual README version with badges or screenshots.
