# import subprocess
# import time
# import schedule
# import datetime
# import os
# from pathlib import Path
# import pandas as pd

# # Paths
# BASE_DIR = r"D:\SEMS\Repos\ai\Job-Portal"
# OUTPUT_DIR = os.path.join(BASE_DIR, "jobspresso_data")
# JOBSPRESSO_SCRIPT = os.path.join(BASE_DIR, "jobspresso.py")
# NAUKRI_SCRIPT = os.path.join(BASE_DIR, "naukri.py")
# LOG_FILE = os.path.join(OUTPUT_DIR, "scraper_log.txt")
# MERGED_FILE = os.path.join(OUTPUT_DIR, "merged_jobs.csv")
# VENV_PYTHON = r"D:\SEMS\Repos\ai\Scripts\python.exe"

# # Ensure output directory exists
# Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# def log_message(message):
#     with open(LOG_FILE, "a", encoding="utf-8") as f:
#         f.write(f"[{datetime.datetime.now()}] {message}\n")

# def run_scraper(script_path):
#     script_name = os.path.basename(script_path)
#     log_message(f"Running {script_name}...")
#     try:
#         result = subprocess.run([VENV_PYTHON, script_path], capture_output=True, text=True, check=True)
#         log_message(f"✅ {script_name} completed.")
#         if result.stdout:
#             log_message(f"STDOUT: {result.stdout.strip()}")
#         if result.stderr:
#             log_message(f"STDERR: {result.stderr.strip()}")
#     except subprocess.CalledProcessError as e:
#         log_message(f"❌ ERROR in {script_name}: {e}")
#         if e.stdout:
#             log_message(f"STDOUT: {e.stdout.strip()}")
#         if e.stderr:
#             log_message(f"STDERR: {e.stderr.strip()}")

# def merge_outputs():
#     try:
#         jp_path = os.path.join(BASE_DIR, "sdr_bdr_jobspresso_jobs.csv")
#         nk_path = os.path.join(BASE_DIR, "sdr_jobs_final.csv")
#         jp_df = pd.read_csv(jp_path)
#         nk_df = pd.read_csv(nk_path)

#         log_message(f"Loaded Jobspresso: {len(jp_df)} rows | Naukri: {len(nk_df)} rows")

#         # Standardize column names
#         jp_df.rename(columns={"Link": "Job URL"}, inplace=True)
#         all_df = pd.concat([jp_df, nk_df], ignore_index=True)

#         # Clean empty Company values
#         all_df.dropna(subset=["Company"], inplace=True)
#         all_df = all_df[all_df["Company"].str.strip() != ""]

#         # Deduplicate
#         all_df.drop_duplicates(subset=["Job Title", "Company", "Location"], inplace=True)

#         all_df["Date Posted"] = pd.to_datetime(all_df["Date Posted"], errors='coerce')
#         all_df.to_csv(MERGED_FILE, index=False)

#         log_message(f"✅ Merged CSV saved with {len(all_df)} rows to '{MERGED_FILE}'")

#     except Exception as e:
#         log_message(f"❌ Merge failed: {str(e)}")

# def job():
#     log_message("=== Scraping Job STARTED ===")
#     run_scraper(JOBSPRESSO_SCRIPT)
#     run_scraper(NAUKRI_SCRIPT)
#     merge_outputs()
#     log_message("=== Scraping Job COMPLETED ===\n")

# def run_scheduler():
#     schedule.every(2).minutes.do(job)

#     count = 0
#     max_runs = 4
#     log_message(f"Scheduler started: Will run {max_runs} times every 2 minutes.")

#     while count < max_runs:
#         if schedule.idle_seconds() <= 0:
#             schedule.run_pending()
#             count += 1
#             log_message(f"🔁 Completed run {count} of {max_runs}")
#         time.sleep(5)

# if __name__ == "__main__":
#     print("Starting automation. Logging + merged CSV enabled.")
#     log_message("🚀 Automation script started.")
#     run_scheduler()

import subprocess
import time
import schedule
import datetime
import os
from pathlib import Path
import pandas as pd
from pyairtable import Table

# Paths
BASE_DIR = r"D:\SEMS\Repos\ai\Job-Portal"
OUTPUT_DIR = os.path.join(BASE_DIR, "jobspresso_data")
JOBSPRESSO_SCRIPT = os.path.join(BASE_DIR, "jobspresso.py")
NAUKRI_SCRIPT = os.path.join(BASE_DIR, "naukri.py")
TALENT_SCRIPT = os.path.join(BASE_DIR, "talent.py")
LOG_FILE = os.path.join(OUTPUT_DIR, "scraper_log.txt")
MERGED_FILE = os.path.join(OUTPUT_DIR, "merged_jobs.csv")
VENV_PYTHON = r"D:\SEMS\Repos\ai\Scripts\python.exe"
# AIRTABLE_API_KEY = "patVLoJbBE5kP0uqY"
# AIRTABLE_BASE_ID = "appGyohuKbC4Kzw6E"
# AIRTABLE_TABLE_NAME = "Job Listings"

# airtable = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)

with open(LOG_FILE, "a", encoding="utf-8") as f:
    f.write(f"[{datetime.datetime.now()}] pipeline.py started\n")

# Ensure output directory exists
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def log_message(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {message}\n")

def run_scraper(script_path):
    script_name = os.path.basename(script_path)
    log_message(f"Running {script_name}...")
    try:
        result = subprocess.run([VENV_PYTHON, script_path], capture_output=True, text=True, check=True)
        log_message(f"{script_name} completed.")
        if result.stdout:
            log_message(f"STDOUT: {result.stdout.strip()}")
        if result.stderr:
            log_message(f"STDERR: {result.stderr.strip()}")
    except subprocess.CalledProcessError as e:
        log_message(f"ERROR in {script_name}: {e}")
        if e.stdout:
            log_message(f"STDOUT: {e.stdout.strip()}")
        if e.stderr:
            log_message(f"STDERR: {e.stderr.strip()}")

def merge_outputs():
    try:
        jp_path = os.path.join(BASE_DIR, "sdr_bdr_jobspresso_jobs.csv")
        nk_path = os.path.join(BASE_DIR, "sdr_jobs_final.csv")
        tl_path = os.path.join(BASE_DIR, "talent_jobs.csv")

        dfs = []

        if os.path.exists(jp_path):
            jp_df = pd.read_csv(jp_path)
            jp_df.rename(columns={"Link": "Job URL"}, inplace=True)
            dfs.append(jp_df)
            log_message(f"Loaded Jobspresso: {len(jp_df)} rows")

        if os.path.exists(nk_path):
            nk_df = pd.read_csv(nk_path)
            dfs.append(nk_df)
            log_message(f"Loaded Naukri: {len(nk_df)} rows")

        if os.path.exists(tl_path):
            tl_df = pd.read_csv(tl_path)
            dfs.append(tl_df)
            log_message(f"Loaded Talent: {len(tl_df)} rows")

        if not dfs:
            log_message("No scraper files found to merge.")
            return

        all_df = pd.concat(dfs, ignore_index=True)
        all_df.dropna(subset=["Company"], inplace=True)
        all_df = all_df[all_df["Company"].str.strip() != ""]
        all_df.drop_duplicates(subset=["Job Title", "Company", "Location"], inplace=True)
        all_df["Date Posted"] = pd.to_datetime(all_df["Date Posted"], errors='coerce')

        # 🔄 Normalize: replace "None", "N/A", None, NaN with "N/A"
        columns_to_clean = ["Experience Level", "Tools Tags", "Industry Type"]
        for col in columns_to_clean:
            all_df[col] = all_df[col].replace(["None", "N/A", None], "-", regex=False).fillna("-")

        all_df.to_csv(MERGED_FILE, index=False)
        log_message(f"Merged CSV saved with {len(all_df)} rows to '{MERGED_FILE}'")

        # push_to_airtable(all_df)
    
    except Exception as e:
        log_message(f"Merge failed: {str(e)}")

# def push_to_airtable(df):
#     try:
#         existing_records = airtable.all()
#         existing_urls = {r['fields'].get("Job URL") for r in existing_records if 'Job URL' in r['fields']}
#         new_jobs = df[df["Job URL"].notna() & ~df["Job URL"].isin(existing_urls)]

#         log_message(f"Pushing {len(new_jobs)} new jobs to Airtable...")

#         for _, row in new_jobs.iterrows():
#             airtable.create({
#                 "Job Title": row["Job Title"],
#                 "Company": row["Company"],
#                 "Location": row["Location"],
#                 "Remote": row["Remote"],
#                 "Job URL": row["Job URL"],
#                 "Logo URL": row["Logo URL"],
#                 "Experience Level": row["Experience Level"],
#                 "Tools Tags": row["Tools Tags"],
#                 "Industry Type": row["Industry Type"],
#                 "Date Posted": str(row["Date Posted"]),
#                 "Refreshed This Week": bool(row["Refreshed This Week"]),
#                 "Job Portal": row["Job Portal"],
#                 "Approval Status": "Pending"
#             })

#         log_message("New jobs pushed to Airtable.")

#     except Exception as e:
#         log_message(f"Failed to push to Airtable: {str(e)}")

def job():
    log_message("=== Scraping Job STARTED ===")
    run_scraper(JOBSPRESSO_SCRIPT)
    run_scraper(NAUKRI_SCRIPT)
    run_scraper(TALENT_SCRIPT)
    merge_outputs()
    log_message("=== Scraping Job COMPLETED ===\n")

def run_scheduler():
    import time
    import schedule

    schedule.every(1).hours.do(job)
    start_time = time.time()
    duration_seconds = 24 * 60 * 60  # 24 hours
    run_count = 0

    log_message("Scheduler started: once every 1 hour, for 24 hours.")

    while time.time() - start_time < duration_seconds:
        if schedule.idle_seconds() <= 0:
            schedule.run_pending()
            run_count += 1
            log_message(f"✅ Completed scheduled run #{run_count}")
        time.sleep(5)

    log_message("⏹️ Scheduler finished after 24 hours.")

if __name__ == "__main__":
    print("🔁 Starting automation. Logging + merged CSV enabled.")
    log_message("🚀 Automation script started.")
    run_scheduler()
    # job()  # Run once immediately for testing