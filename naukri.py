
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import pandas as pd

# Setup headless Chrome
options = Options()
options.add_argument('--headless=new')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Go to Naukri SDR jobs page
driver.get("https://www.naukri.com/sdr-jobs?k=sdr")

# Wait for job links to load
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.title')))
job_elems = driver.find_elements(By.CSS_SELECTOR, 'a.title')

job_weblinks = []
for elem in job_elems:
    href = elem.get_attribute("href")
    if href:
        job_weblinks.append(href)

# Wait for company info
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.comp-dtls-wrap')))
company_tags = driver.find_elements(By.CSS_SELECTOR, 'span.comp-dtls-wrap')

company_names = []
for tag in company_tags:
    if tag.text.strip():
        company_names.append(tag.text.strip().split('\n')[0])
    else:
        company_names.append("")

driver.quit()

# Visit individual job pages
job_titles = []
locations = []
logo_urls = []
job_links = []
company_final = []

for i, url in enumerate(job_weblinks[:len(company_names)]):
    print(f"Scraping job {i+1}: {url}")
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
    except:
        job_titles.append("N/A")

    # Location
    try:
        location_elem = driver.find_element(By.CLASS_NAME, "styles_jhc__loc___Du2H")
        locations.append(location_elem.text.strip())
    except:
        locations.append("N/A")

    # Logo URL
    try:
        logo_elem = driver.find_element(By.CLASS_NAME, "styles_jhc__comp-banner__ynBvr")
        logo_url = logo_elem.get_attribute("src")
        logo_urls.append(logo_url)
    except:
        logo_urls.append("N/A")

    job_links.append(url)
    company_final.append(company_names[i] if i < len(company_names) else "N/A")

    driver.quit()

# Create DataFrame
df = pd.DataFrame({
    "Job Title": job_titles,
    "Company": company_final,
    "Location": locations,
    "Job URL": job_links,
    "Logo URL": logo_urls
})

df = df.drop_duplicates(subset='Job URL')
df = df.drop_duplicates(subset=['Job Title', 'Company'])

df.to_csv("sdr_jobs_final.csv", index=False)
print("✅ Scraped and saved to sdr_jobs_final.csv")




