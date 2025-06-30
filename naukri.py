
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# from bs4 import BeautifulSoup
# import pandas as pd

# # Setup headless Chrome
# options = Options()
# options.add_argument('--headless=new')
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# # Go to Naukri SDR jobs page
# driver.get("https://www.naukri.com/sdr-jobs?k=sdr")

# # Wait for job links to load
# WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.title')))
# job_elems = driver.find_elements(By.CSS_SELECTOR, 'a.title')

# job_weblinks = []
# for elem in job_elems:
#     href = elem.get_attribute("href")
#     if href:
#         job_weblinks.append(href)

# # Wait for company info
# WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.comp-dtls-wrap')))
# company_tags = driver.find_elements(By.CSS_SELECTOR, 'span.comp-dtls-wrap')

# company_names = []
# for tag in company_tags:
#     if tag.text.strip():
#         company_names.append(tag.text.strip().split('\n')[0])
#     else:
#         company_names.append("")

# driver.quit()

# # Visit individual job pages
# job_titles = []
# locations = []
# logo_urls = []
# job_links = []
# company_final = []

# for i, url in enumerate(job_weblinks[:len(company_names)]):
#     print(f"Scraping job {i+1}: {url}")
#     options = Options()
#     options.add_argument('--headless=new')
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
#     driver.get(url)
#     time.sleep(2)

#     # Job Title
#     try:
#         title_elem = driver.find_element(By.XPATH, "//h1[contains(@class, 'styles_jd-header-title__')]")
#         job_titles.append(title_elem.text.strip())
#     except:
#         job_titles.append("N/A")

#     # Location
#     try:
#         location_elem = driver.find_element(By.CLASS_NAME, "styles_jhc__loc___Du2H")
#         locations.append(location_elem.text.strip())
#     except:
#         locations.append("N/A")

#     # Logo URL
#     try:
#         logo_elem = driver.find_element(By.CLASS_NAME, "styles_jhc__comp-banner__ynBvr")
#         logo_url = logo_elem.get_attribute("src")
#         logo_urls.append(logo_url)
#     except:
#         logo_urls.append("N/A")

#     job_links.append(url)
#     company_final.append(company_names[i] if i < len(company_names) else "N/A")

#     driver.quit()

# # Create DataFrame
# df = pd.DataFrame({
#     "Job Title": job_titles,
#     "Company": company_final,
#     "Location": locations,
#     "Job URL": job_links,
#     "Logo URL": logo_urls
# })

# df = df.drop_duplicates(subset='Job URL')
# df = df.drop_duplicates(subset=['Job Title', 'Company'])

# df.to_csv("sdr_jobs_final.csv", index=False)
# print("✅ Scraped and saved to sdr_jobs_final.csv")



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from datetime import datetime, timedelta

def debug(msg):
    print(f"[DEBUG] {msg}")

# Setup headless Chrome
options = Options()
options.add_argument('--headless=new')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

debug("Navigating to Naukri SDR jobs page...")
driver.get("https://www.naukri.com/sdr-jobs?k=sdr")

debug("Waiting for job titles to load...")
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.title')))
job_elems = driver.find_elements(By.CSS_SELECTOR, 'a.title')

job_weblinks = []
for elem in job_elems:
    href = elem.get_attribute("href")
    if href:
        job_weblinks.append(href)
debug(f"Found {len(job_weblinks)} job links.")

debug("Waiting for company names to load...")
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.comp-dtls-wrap')))
company_tags = driver.find_elements(By.CSS_SELECTOR, 'span.comp-dtls-wrap')

company_names = []
for tag in company_tags:
    if tag.text.strip():
        company_names.append(tag.text.strip().split('\n')[0])
    else:
        company_names.append("")
debug(f"Captured {len(company_names)} company names.")

driver.quit()

job_titles = []
locations = []
logo_urls = []
job_links = []
company_final = []
experience_levels = []
outreach_tools_in_job_descriptions_ordered = [
        "Salesforce", "HubSpot", "Outreach.io", "SalesLoft", "LinkedIn Sales Navigator", "Apollo.io", "Pipedrive",
        "Yesware", "Woodpecker", "Reply.io", "Saleshandy", "Lemlist", "Mailshake", "ZoomInfo", "Freshsales",
        "ActiveCampaign", "Close.io", "Groove", "Instantly.ai", "Skylead", "Outplay", "Zendesk Sell", "Zoho CRM",
        "Keap", "Mailchimp", "Constant Contact", "GetResponse", "AWeber", "SendinBlue", "Mixmax", "PersistIQ",
        "Kixie", "Callingly", "RingCentral", "Aircall", "Dialpad", "JustCall", "Five9", "Talkdesk"
    ]
industry_tag = []
date_posted_list = []
refreshed_this_week_list = []

debug("Starting individual job page scraping...")
for i, url in enumerate(job_weblinks[:len(company_names)]):
    print(f"Scraping job {i+1}/{len(company_names)}: {url}")
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(2)

    # Job Title
    try:
        title_elem = driver.find_element(By.XPATH, "//h1[contains(@class, 'styles_jd-header-title__')]")
        job_titles.append(title_elem.text.strip())
    except Exception as e:
        debug(f"Job title not found for {url}: {e}")
        job_titles.append("N/A")

    # Location
    try:
        location_elem = driver.find_element(By.CLASS_NAME, "styles_jhc__location__W_pVs")
        locations.append(location_elem.text.strip())
    except Exception as e:
        debug(f"Location not found for {url}: {e}")
        locations.append("N/A")

    # Logo URL
    try:
        logo_elem = driver.find_element(By.CLASS_NAME, "styles_jhc__comp-banner__ynBvr")
        logo_url = logo_elem.get_attribute("src")
        logo_urls.append(logo_url)
    except Exception as e:
        debug(f"Logo not found for {url}: {e}")
        logo_urls.append("N/A")

    # Experience Level
    try:
        exp_elem = driver.find_element(By.CLASS_NAME, "styles_jhc__exp__k_giM")
        exp_text = exp_elem.text.strip().replace('\n', ' ').replace('  ', ' ')
        debug(f"Raw experience string: {exp_text}")
        # Extract min years
        years = [int(s) for s in exp_text.split() if s.isdigit()]
        min_years = min(years) if years else None
        if min_years is not None:
            if min_years <= 2:
                experience_levels.append("Entry-level")
            elif min_years <= 5:
                experience_levels.append("Mid-level")
            else:
                experience_levels.append("Senior-level")
        else:
            experience_levels.append("N/A")
    except Exception as e:
        debug(f"Experience info not found for {url}: {e}")
        experience_levels.append("N/A")

    try:
        desc_div = driver.find_element(By.CLASS_NAME, "styles_JDC__dang-inner-html__h0K4t")
        desc_text = desc_div.text.lower()
        mentioned_tools = [tool for tool in outreach_tools_in_job_descriptions_ordered if tool.lower() in desc_text]
        tools_mentioned_str = ", ".join(mentioned_tools) if mentioned_tools else "None"
    except Exception as e:
        debug(f"Could not extract outreach tools from {url}: {e}")
        tools_mentioned_str = "N/A"

    try:
        details_divs = driver.find_elements(By.CLASS_NAME, "styles_details__Y424J")
        industry_type = "N/A"
        for div in details_divs:
            try:
                label = div.find_element(By.TAG_NAME, "label")
                if "industry type" in label.text.strip().lower():
                    industry_span = div.find_element(By.TAG_NAME, "span")
                    industry_type = industry_span.text.strip()
                    debug(f"Extracted Industry Type: {industry_type}")
                    break
            except Exception as inner:
                continue
    except Exception as e:
        debug(f"Could not extract Industry Type for {url}: {e}")
        industry_type = "N/A"
    
    try:
        stats_divs = driver.find_elements(By.CLASS_NAME, "styles_jhc__stat__PgY67")
        date_posted_text = None
        for div in stats_divs:
            label = div.find_element(By.TAG_NAME, "label").text.strip().lower()
            if "posted" in label:
                date_posted_text = div.find_element(By.TAG_NAME, "span").text.strip().lower().replace("+", "")
                break
        date_posted = datetime.today()
        if date_posted_text:
            if "hour" in date_posted_text:
                num_hours = int(date_posted_text.split()[0])
                date_posted = datetime.today() - timedelta(hours=num_hours)
            elif "day" in date_posted_text:
                num_days = int(date_posted_text.split()[0])
                date_posted = datetime.today() - timedelta(days=num_days)
            elif "week" in date_posted_text:
                num_weeks = int(date_posted_text.split()[0])
                date_posted = datetime.today() - timedelta(weeks=num_weeks)
            elif "month" in date_posted_text:
                num_months = int(date_posted_text.split()[0])
                date_posted = datetime.today() - timedelta(weeks=4 * num_months)
        
        refreshed_this_week = (datetime.today() - date_posted).days <= 7
        date_posted_list.append(date_posted)
        refreshed_this_week_list.append(refreshed_this_week)

        debug(f"Date posted: {date_posted.date()}, Refreshed this week? {refreshed_this_week}")
    
    except Exception as e:
        debug(f"Could not extract date posted for {url}: {e}")
        date_posted_list.append(None)
        refreshed_this_week_list.append(False)

                

    job_links.append(url)
    company_final.append(company_names[i] if i < len(company_names) else "N/A")
    industry_tag.append(industry_type)



    driver.quit()

# Create DataFrame
df = pd.DataFrame({
    "Job Title": job_titles,
    "Company": company_final,
    "Location": locations,
    "Remote": ["Remote" if "remote" in loc.lower() else "On-site" for loc in locations],
    "Job URL": job_links,
    "Logo URL": logo_urls,
    "Experience Level": experience_levels,
    "Tools Tags": tools_mentioned_str,
    "Industry Type": industry_tag,
    "Date Posted": date_posted_list,
    "Refreshed This Week": refreshed_this_week_list,
    "Job Portal": "Naukri"
})

df["Date Posted"] = pd.to_datetime(df["Date Posted"], errors='coerce').dt.date
df = df.drop_duplicates(subset='Job URL')
df = df.drop_duplicates(subset=['Job Title', 'Company'])

debug("Saving scraped data to CSV...")
df.to_csv("sdr_jobs_final.csv", index=False)
print("Scraped and saved to sdr_jobs_final.csv")

