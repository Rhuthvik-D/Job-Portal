

# import pandas as pd
# import streamlit as st
# from datetime import datetime
# import subprocess
# import time
# import os

# # ---- Configuration ----
# SCRAPER_PATH = r"D:\SEMS\Repos\ai\Job-Portal\pipeline.py"
# VENV_PYTHON = r"D:\SEMS\Repos\ai\Scripts\python.exe"
# DATA_PATH = r"D:\SEMS\Repos\ai\Job-Portal\jobspresso_data\merged_jobs.csv"

# # ---- Streamlit Page Settings ----
# st.set_page_config(
#     page_title="BDR/SDR Job Finder",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ---- Custom CSS ----
# st.markdown("""
# <style>
# body {
#     font-family: 'Segoe UI', sans-serif;
# }
# [data-testid="stExpander"] {
#     border: 1px solid #444;
#     border-radius: 8px;
#     background-color: #1e1e1e;
#     padding: 1em;
# }
# .tag {
#     background-color: #333;
#     color: white;
#     padding: 3px 8px;
#     margin-right: 5px;
#     border-radius: 4px;
#     font-size: 0.8em;
#     display: inline-block;
# }
# [data-testid="stImage"] img {
#     border-radius: 6px;
#     background: #fff;
#     padding: 4px;
# }
# </style>
# """, unsafe_allow_html=True)

# # ---- Load Data ----
# @st.cache_data(ttl=300)
# def load_data():
#     df = pd.read_csv(DATA_PATH, parse_dates=["Date Posted"])
#     df["Date Posted"] = pd.to_datetime(df["Date Posted"], errors="coerce").dt.date
#     df.dropna(subset=["Company"], inplace=True)
#     return df

# df = load_data()

# # ---- Top Filters UI ----
# st.markdown("## 🎯Job Portal")

# col1, col2, col3, col4, col5 = st.columns(5)
# with col1:
#     search = st.text_input("🔍 Keyword Search")
# with col2:
#     experience = st.multiselect("💼 Experience", sorted(df["Experience Level"].dropna().unique()))
# with col3:
#     remote = st.multiselect("🏡 Remote Type", sorted(df["Remote"].dropna().unique()))
# with col4:
#     portal = st.multiselect("🌐 Job Portal", sorted(df["Job Portal"].dropna().unique()))
# with col5:
#     refreshed_only = st.checkbox("🆕 Refreshed This Week", value=False)

# col6, col7, col8 = st.columns([1.5, 1.5, 2])
# min_date = df["Date Posted"].min()
# max_date = df["Date Posted"].max()
# with col6:
#     start_date = st.date_input("📅 From", value=min_date, min_value=min_date, max_value=max_date)
# with col7:
#     end_date = st.date_input("📅 To", value=max_date, min_value=start_date, max_value=max_date)
# with col8:
#     cooldown = 600
#     now = time.time()
#     if "last_scrape_time" not in st.session_state:
#         st.session_state.last_scrape_time = 0
#     time_since = now - st.session_state.last_scrape_time
#     if time_since >= cooldown:
#         if st.button("🔄 Refresh Jobs Now"):
#             subprocess.Popen([VENV_PYTHON, SCRAPER_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#             st.session_state.last_scrape_time = time.time()
#             st.success("✅ Refresh started.")
#     else:
#         st.button("🔄 Refresh Jobs Now", disabled=True)
#         remaining = int(cooldown - time_since)
#         st.info(f"⏳ {remaining//60}m {remaining%60}s until refresh")

# # ---- Apply Filters ----
# filtered = df.copy()
# if search:
#     s = search.lower()
#     filtered = filtered[
#         df["Job Title"].str.lower().str.contains(s) |
#         df["Company"].str.lower().str.contains(s) |
#         df["Tools Tags"].str.lower().str.contains(s, na=False)
#     ]
# if experience:
#     filtered = filtered[filtered["Experience Level"].isin(experience)]
# if remote:
#     filtered = filtered[filtered["Remote"].isin(remote)]
# if portal:
#     filtered = filtered[filtered["Job Portal"].isin(portal)]
# if refreshed_only:
#     filtered = filtered[filtered["Refreshed This Week"] == True]
# filtered = filtered[
#     (filtered["Date Posted"] >= start_date) & (filtered["Date Posted"] <= end_date)
# ]

# # ---- Results ----
# st.markdown(f"📊 **Total Jobs:** `{len(df)}` | 🎯 **Matching Filters:** `{len(filtered)}`")

# if filtered.empty:
#     st.warning("No jobs matched. Try adjusting the filters.")
# else:
#     for _, row in filtered.iterrows():
#         title_display = f"🔹 {row['Job Title']} at {row['Company']}"
#         with st.expander(title_display, expanded=False):
#             cols = st.columns([1, 5])
#             with cols[0]:
#                 if pd.notna(row["Logo URL"]) and row["Logo URL"] != "N/A":
#                     st.image(row["Logo URL"], width=80)
#             with cols[1]:
#                 st.markdown(f"""
# - 📍 **Location:** {row['Location']}
# - 🧭 **Remote Type:** {row['Remote']}
# - 💼 **Experience Level:** {row['Experience Level']}
# - 🛠️ **Tools:** {' '.join([f"<span class='tag'>{t.strip()}</span>" for t in str(row['Tools Tags']).split(',') if t.strip()])}
# - 🏢 **Industry:** {row['Industry Type']}
# - 📅 **Posted:** {row['Date Posted']}
# - 🌐 **Source:** {row['Job Portal']}
# - 🔗 [Open Job Posting]({row['Job URL']})
# """, unsafe_allow_html=True)


import pandas as pd
import streamlit as st
from datetime import datetime
import subprocess
import time
import os
import sys

# ---- Config ----
# SCRAPER_PATH = r"D:\SEMS\Repos\ai\Job-Portal\pipeline.py"
# VENV_PYTHON = r"D:\SEMS\Repos\ai\Scripts\python.exe"
# DATA_PATH = r"D:\SEMS\Repos\ai\Job-Portal\jobspresso_data\merged_jobs.csv"


BASE_DIR = os.getcwd()  # Use current working directory
SCRAPER_PATH = os.path.join(BASE_DIR, "pipeline.py")
VENV_PYTHON = sys.executable
DATA_PATH = os.path.join(BASE_DIR, "jobspresso_data", "merged_jobs.csv")

# AIRTABLE_API_KEY = "patVLoJbBE5kP0uqY"
# AIRTABLE_BASE_ID = "appGyohuKbC4Kzw6E"
# AIRTABLE_TABLE_NAME = "Job Listings"

# table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)

# ---- Streamlit Page Settings ----
st.set_page_config(page_title="Job Portal", layout="wide", initial_sidebar_state="collapsed")

# ---- Background Image ----
st.markdown("""
<style>
[data-testid="stExpander"] {
    background-color: #161b22 !important;
    border: 1px solid #30363d;
    border-radius: 10px;
}
.tag {
    background-color: #2ea44f;
    color: white;
    padding: 3px 10px;
    margin: 3px 4px;
    border-radius: 4px;
    font-size: 0.75em;
    display: inline-block;
}
[data-testid="stImage"] img {
    border-radius: 8px;
    background: #fff;
    padding: 4px;
}
[theme]
base = "dark"
primaryColor = "#2ea44f"               
backgroundColor = "#0d1117"            
secondaryBackgroundColor = "#161b22"   
textColor = "#c9d1d9"                  
font = "sans serif"

[server]
runOnSave = true

[client]
toolbarMode = "minimal"
showSidebarNavigation = false

[browser]
gatherUsageStats = false

</style>
""", unsafe_allow_html=True)

# ---- Load Data ----
@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Date Posted"])
    df["Date Posted"] = pd.to_datetime(df["Date Posted"], errors="coerce").dt.date
    df.dropna(subset=["Company"], inplace=True)
    return df

df = load_data()

# ---- Title & Summary ----
st.markdown("## 🚀 SDR / BDR Job Portal – Curated from Jobspresso, Naukri, Talent")
st.markdown(f"📊 **Total Jobs in Dataset:** `{len(df)}`")

# ---- Filters ----
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    search = st.text_input("🔍 Keyword")
with col2:
    experience = st.multiselect("💼 Experience", sorted(df["Experience Level"].dropna().unique()))
with col3:
    remote = st.multiselect("🏡 Remote", sorted(df["Remote"].dropna().unique()))
with col4:
    portal = st.multiselect("🌐 Portal", sorted(df["Job Portal"].dropna().unique()))
with col5:
    industries = st.multiselect("🏭 Industry", sorted(df["Industry Type"].dropna().unique()))

col6, col7, col8, col9 = st.columns([1.5, 1.5, 1, 1])
min_date = df["Date Posted"].min()
max_date = df["Date Posted"].max()
with col6:
    start_date = st.date_input("📅 From", value=min_date, min_value=min_date, max_value=max_date)
with col7:
    end_date = st.date_input("📅 To", value=max_date, min_value=start_date, max_value=max_date)
with col8:
    refreshed = st.checkbox("🆕 Posted This Week")
with col9:
    cooldown = 600
    now = time.time()
    if "last_scrape_time" not in st.session_state:
        st.session_state.last_scrape_time = 0
    time_since = now - st.session_state.last_scrape_time
    if time_since >= cooldown:
        if st.button("🔄 Refresh Jobs Now"):
            subprocess.Popen([VENV_PYTHON, SCRAPER_PATH])
            st.session_state.last_scrape_time = time.time()
            st.success("✅ Refresh started.")
    else:
        st.button("🔄 Refresh Jobs Now", disabled=True)
        remaining = int(cooldown - time_since)
        st.info(f"⏳ {remaining//60}m {remaining%60}s until refresh")


# ---- Apply Filters ----
filtered = df.copy()
if search:
    s = search.lower()
    filtered = filtered[
        df["Job Title"].str.lower().str.contains(s) |
        df["Company"].str.lower().str.contains(s) |
        df["Tools Tags"].str.lower().str.contains(s, na=False)
    ]
if industries:
    filtered = filtered[filtered["Industry Type"].isin(industries)]
if experience:
    filtered = filtered[filtered["Experience Level"].isin(experience)]
if remote:
    filtered = filtered[filtered["Remote"].isin(remote)]
if portal:
    filtered = filtered[filtered["Job Portal"].isin(portal)]
if refreshed:
    filtered = filtered[filtered["Refreshed This Week"] == True]
filtered = filtered[(filtered["Date Posted"] >= start_date) & (filtered["Date Posted"] <= end_date)]

st.markdown(f"🎯 **Jobs Matching Filters:** `{len(filtered)}`")

# ---- Show Jobs ----
if filtered.empty:
    st.warning("No jobs matched your filters.")
else:
    for _, row in filtered.iterrows():
        # ✅ Step 1: Determine experience level color
        exp_level = str(row['Experience Level']).strip().lower()
        if "entry" in exp_level:
            exp_color = "#3fb950"   # Green
        elif "mid" in exp_level:
            exp_color = "#d29922"   # Yellow
        elif "senior" in exp_level:
            exp_color = "#f0f6fc"   # White
        else:
            exp_color = "#9da5b4"   # Default gray

        # ✅ Step 2: Build styled header HTML
        header_html = f"""
        <div style='display: flex; justify-content: space-between; align-items: flex-start; width: 100%; padding: 6px 0;'>
            <div style='display: flex; flex-direction: column;'>
                <span style='font-weight: 700; font-size: 1.3rem; color: #e6edf3;'>💠 {row['Job Title']} @ {row['Company']}</span>
                <span style='font-size: 1rem; color: {exp_color};'>🧳 {row['Experience Level']}</span>
            </div>
            <div style='text-align: right; font-size: 1rem; line-height: 1.4;'>
                <span style='color: #58a6ff;'>📍 {row['Remote']}</span><br>
                <span style='color: #8b949e;'>🌐 {row['Job Portal']}</span>
            </div>
        </div>
        """

        # ✅ Step 3: Render custom header
        st.markdown(header_html, unsafe_allow_html=True)

        # ✅ Step 4: Show details inside expander
        with st.expander("🔎 Show Job Details"):
            cols = st.columns([1, 5])
            with cols[0]:
                if pd.notna(row["Logo URL"]) and row["Logo URL"] != "N/A":
                    st.image(row["Logo URL"], width=80)
            with cols[1]:
                # Style tool tags as pill badges
                tags = " ".join(
                    [f"<span class='tag'>{t.strip()}</span>" for t in str(row['Tools Tags']).split(',') if t.strip()]
                )
                st.markdown(f"""
    - 📍 **Location:** {row['Location']}
    - 💼 **Experience:** {row['Experience Level']}
    - 🛠️ **Tools:** {tags}
    - 🏢 **Industry:** {row['Industry Type']}
    - 📅 **Posted:** {row['Date Posted']}
    - 🔗 [**View Job Posting**]({row['Job URL']})
    """, unsafe_allow_html=True)