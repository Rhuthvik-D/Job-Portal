from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint

# Setup headless browser
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

url = "https://www.techcareers.com/jobs/search?k=sales+development+representative"
driver.get(url)
sleep(2)

# Simulate scrolls and wait for job cards to load
scroll_limit = 10
scroll_count = 0

while scroll_count < scroll_limit:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.job-search-results"))
        )
    except TimeoutException:
        print(f"⚠️ Timeout on scroll {scroll_count}, stopping early.")
        break
    scroll_count += 1
    sleep(randint(2, 4))

# Parse loaded content
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Keywords to match job titles
KEYWORDS = [
    'SDR', 'BDR',
    'Sales Development Representative',
    'Business Development Representative',
    'Account', 'Accounts', 'Sales', 'Finance', 'Financial'
]

seen_links = set()
jobs = []

for job_card in soup.find_all('li', class_='job-search-results'):
    title_elem = job_card.select_one('h2')
    if not title_elem:
        continue
    title = title_elem.text.strip()

    if not any(k.lower() in title.lower() for k in KEYWORDS):
        continue

    job_url = title_elem['href']
    if not job_url or job_url in seen_links:
        continue
    seen_links.add(job_url)

    company_elem = job_card.find('span', class_='job-title-company')
    location_elem = job_card.select_one('.location')
    logo_elem = job_card.find('img')
    logo_url = logo_elem['src'] if logo_elem and logo_elem.has_attr('src') else None

    jobs.append({
        'Job Title': title,
        'Company': company_elem.text.strip() if company_elem else None,
        'Location': location_elem.text.strip() if location_elem else 'Remote',
        'Link': job_url,
        'Logo URL': logo_elem['src'] if logo_elem and logo_elem.has_attr('src') else None
    })

# Save to CSV
df = pd.DataFrame(jobs)
df = df.drop_duplicates(subset='Link')
df = df.drop_duplicates(subset=['Job Title', 'Company'])

df.to_csv("sdr_bdr_techcareers_jobs.csv", index=False)
print(f"✅ Scraped {len(df)} SDR/BDR jobs (max 10 scrolls). Saved to 'sdr_bdr_techcareers_jobs.csv'")
