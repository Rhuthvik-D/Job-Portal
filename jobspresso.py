from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint

# Setup headless browser
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

url = "https://jobspresso.co/remote-sales-jobs/"
driver.get(url)
sleep(2)

# Limit to 10 clicks max
click_limit = 10
click_count = 0

while click_count < click_limit:
    try:
        load_more = driver.find_element(By.CLASS_NAME, "load_more_jobs")
        driver.execute_script("arguments[0].click();", load_more)
        click_count += 1
        sleep(randint(2, 4))
    except NoSuchElementException:
        print("No more listings to load.")
        break
    except ElementClickInterceptedException:
        sleep(2)
        continue

# Parse loaded content
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Keywords to match job titles
KEYWORDS = ['SDR', 'BDR', 'Sales Development Representative', 'Business Development Representative', 'Account', 'Accounts', 'Sales', 'Finance', 'Financial']
seen_links = set()
jobs = []

for job_card in soup.find_all('li', class_='job_listing'):
    title_elem = job_card.find('h3')
    if not title_elem:
        continue
    title = title_elem.text.strip()

    if not any(k.lower() in title.lower() for k in KEYWORDS):
        continue

    link_elem = job_card.find('a', href=True)
    job_url = link_elem['href'] if link_elem else None
    if not job_url or job_url in seen_links:
        continue
    seen_links.add(job_url)

    company_elem = job_card.find('div', class_='job_listing-company')
    company_name = company_elem.find('strong') if company_elem and company_elem.find('strong') else None
    location_elem = job_card.find('div', class_='job_listing-location')
    logo_elem = job_card.find('img')
    logo_url = logo_elem['src'] if logo_elem and logo_elem.has_attr('src') else None

    jobs.append({
        'Job Title': title,
        'Company': company_name.text.strip() if company_name else None,
        'Location': location_elem.text.strip() if location_elem else 'Remote',
        'Link': job_url,
        'Logo URL': logo_url
    })

# Save to CSV
df = pd.DataFrame(jobs)


# Drop duplicate jobs based on 'Link'
df = df.drop_duplicates(subset='Link')
df = df.drop_duplicates(subset=['Job Title', 'Company'])

df.to_csv("sdr_bdr_jobspresso_jobs.csv", index=False)
# Optionally also by 'Job Title' + 'Company'
print(f"✅ Scraped {len(df)} SDR/BDR jobs (max 10 loads). Saved to 'sdr_bdr_jobspresso_jobs.csv'")