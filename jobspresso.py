from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
from time import sleep, time
from random import randint

from datetime import datetime, timedelta

# # Setup headless browser
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# url = "https://jobspresso.co/remote-sales-jobs/"
# driver.get(url)
# sleep(2)

# # Limit to 10 clicks max
# click_limit = 10
# click_count = 0

# while click_count < click_limit:
#     try:
#         load_more = driver.find_element(By.CLASS_NAME, "load_more_jobs")
#         driver.execute_script("arguments[0].click();", load_more)
#         click_count += 1
#         sleep(randint(2, 4))
#     except NoSuchElementException:
#         print("No more listings to load.")
#         break
#     except ElementClickInterceptedException:
#         sleep(2)
#         continue

# # Parse loaded content
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# driver.quit()

# # Keywords to match job titles
# KEYWORDS = ['SDR', 'BDR', 'Sales Development Representative', 'Business Development Representative', 'Account', 'Accounts', 'Sales', 'Finance', 'Financial']
# seen_links = set()
# jobs = []

# for job_card in soup.find_all('li', class_='job_listing'):
#     title_elem = job_card.find('h3')
#     if not title_elem:
#         continue
#     title = title_elem.text.strip()

#     if not any(k.lower() in title.lower() for k in KEYWORDS):
#         continue

#     link_elem = job_card.find('a', href=True)
#     job_url = link_elem['href'] if link_elem else None
#     if not job_url or job_url in seen_links:
#         continue
#     seen_links.add(job_url)

#     company_elem = job_card.find('div', class_='job_listing-company')
#     company_name = company_elem.find('strong') if company_elem and company_elem.find('strong') else None
#     location_elem = job_card.find('div', class_='job_listing-location')
#     logo_elem = job_card.find('img')
#     logo_url = logo_elem['src'] if logo_elem and logo_elem.has_attr('src') else None

#     jobs.append({
#         'Job Title': title,
#         'Company': company_name.text.strip() if company_name else None,
#         'Location': location_elem.text.strip() if location_elem else 'Remote',
#         'Link': job_url,
#         'Logo URL': logo_url
#     })

# # Save to CSV
# df = pd.DataFrame(jobs)


# # Drop duplicate jobs based on 'Link'
# df = df.drop_duplicates(subset='Link')
# df = df.drop_duplicates(subset=['Job Title', 'Company'])

# df.to_csv("sdr_bdr_jobspresso_jobs.csv", index=False)
# # Optionally also by 'Job Title' + 'Company'
# print(f"✅ Scraped {len(df)} SDR/BDR jobs (max 10 loads). Saved to 'sdr_bdr_jobspresso_jobs.csv'")


def scrape_jobspresso():

    # Setup headless browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    url = "https://jobspresso.co/remote-sales-jobs/"
    driver.get(url)
    sleep(2)

    for _ in range(10):
        try:
            load_more = driver.find_element(By.CLASS_NAME, "load_more_jobs")
            driver.execute_script("arguments[0].click();", load_more)
            sleep(2)
        except NoSuchElementException:
            break

    # Parse loaded content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Keywords to match job titles
    KEYWORDS = ['SDR', 'BDR', 'Sales Development Representative', 'Business Development Representative', 'Account', 'Accounts', 'Sales', 'Finance', 'Financial']
    outreach_tools_in_job_descriptions_ordered = [    "Salesforce",     "HubSpot",      "Outreach.io",     "SalesLoft",     "LinkedIn Sales Navigator",     "Apollo.io",     "Pipedrive",      "Yesware",      "Woodpecker",      "Reply.io",     "Saleshandy",     "Lemlist",      "Mailshake",     "ZoomInfo",     "Freshsales",     "ActiveCampaign",     "Close.io",      "Groove",     "Instantly.ai",     "Skylead",    "Outplay",    "Zendesk Sell",    "Zoho CRM",    "Keap",    "Mailchimp",    "Constant Contact",    "GetResponse",    "AWeber",    "SendinBlue",    "Mixmax",    "PersistIQ",    "Kixie",    "Callingly","RingCentral","Aircall","Dialpad","JustCall","Five9","Talkdesk"]
    seen_links = set()

    try:
        old_df = pd.read_csv("sdr_bdr_jobspresso_jobs.csv")
        seen_links = set(old_df['Job URL'].dropna())
    except FileNotFoundError:
        old_df = pd.DataFrame()

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
        company = company_elem.find('strong').text.strip() if company_elem and company_elem.find('strong') else None
        location_elem = job_card.find('div', class_='job_listing-location')
        logo_elem = job_card.find('img')
        logo_url = logo_elem['src'] if logo_elem and logo_elem.has_attr('src') else None

        experience_level = "N/A"
        try:
            resp = requests.get(job_url, headers={"User-Agent": "Mozilla/5.0"})
            job_soup = BeautifulSoup(resp.text, 'html.parser')
            desc_div = job_soup.find('div', class_='job_listing-description')
            tools_mentioned_str = "N/A"
            date_posted_obj = None
            refreshed_this_week = False

            if desc_div:
                full_text = desc_div.get_text(separator=' ', strip=True).lower()
                print(f"[DEBUG] Extracted job description text from {job_url}")

                # Experience level detection
                match = re.search(r'(\d+)\s*(?:-|to)?\s*(\d+)?\s*[\+]?[\s\-]*(years|yrs)', full_text)
                print(f"[DEBUG] Regex match result: {match}")
                if match:
                    min_yrs = int(match.group(1))
                    print(f"[DEBUG] Parsed minimum years: {min_yrs}")
                    if min_yrs <= 2:
                        experience_level = "Entry-level"
                    elif 3 <= min_yrs <= 5:
                        experience_level = "Mid-level"
                    else:
                        experience_level = "Senior-level"
                    print(f"[DEBUG] Final experience level: {experience_level}")
                else:
                    print(f"[DEBUG] No match found for years pattern in {job_url}")

                # Outreach tools detection
                mentioned_tools = [tool for tool in outreach_tools_in_job_descriptions_ordered if tool.lower() in full_text]
                tools_mentioned_str = ", ".join(mentioned_tools) if mentioned_tools else "None"
                print(f"[DEBUG] Tools mentioned in {job_url}: {tools_mentioned_str}")
            else:
                print(f"[DEBUG] No job description section found for {job_url}")

            # Date posted extraction
            date_posted_li = job_soup.find('li', class_='date-posted')
            if date_posted_li:
                date_tag = date_posted_li.find('date')
                if date_tag:
                    raw_date_text = date_tag.text.strip().replace("Posted", "").strip()
                    raw_date_text = re.sub(r"[^\w\s]", "", raw_date_text)  # Remove punctuation
                    try:
                        parsed_date = datetime.strptime(raw_date_text, "%B %d")
                        today = datetime.today()
                        year = today.year if parsed_date.month <= today.month else today.year - 1
                        date_posted_obj = datetime.strptime(f"{raw_date_text} {year}", "%B %d %Y")
                        refreshed_this_week = (today - date_posted_obj) <= timedelta(days=7)
                        print(f"[DEBUG] Date posted for {job_url}: {date_posted_obj} | Refreshed this week: {refreshed_this_week}")
                    except Exception as e:
                        print(f"[DEBUG] Couldn't parse date for {job_url}: {e}")
                else:
                    print(f"[DEBUG] <date> tag not found in date-posted for {job_url}")
            else:
                print(f"[DEBUG] No date-posted section found for {job_url}")
        except Exception as e:
            print(f"[DEBUG] Error processing job at {job_url}: {e}")
        
        

        jobs.append({
            'Job Title': title,
            'Company': company,
            'Location': location_elem.text.strip() if location_elem else 'Remote',
            'Remote': (
                "Remote" if location_elem and ('Anywhere in US' in location_elem.text or "Anywhere" in location_elem.text)
                 else "On-site" if location_elem
                 else "N/A"
            ),
            'Job URL': job_url,
            'Logo URL': logo_url,
            'Experience Level': experience_level,
            'Tools Tags': tools_mentioned_str,
            'Industry Type': 'Not specified on Jobspresso',
            'Date Posted': date_posted_obj,
            'Refreshed This Week': refreshed_this_week,
            'Job Portal': 'Jobspresso'
        })
        print(f"[DEBUG] Added job: {title}")

    new_df = pd.DataFrame(jobs)
    final_df = pd.concat([old_df, new_df], ignore_index=True)
    final_df.drop_duplicates(subset='Job URL', inplace=True)
    final_df["Date Posted"] = pd.to_datetime(final_df["Date Posted"], errors='coerce')
    final_df.to_csv("sdr_bdr_jobspresso_jobs.csv", index=False)

if __name__ == "__main__":
    scrape_jobspresso()
    print("Scraped SDR/BDR jobs from Jobspresso and saved to 'sdr_bdr_jobspresso_jobs.csv'")