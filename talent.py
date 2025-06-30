# import requests
# from bs4 import BeautifulSoup
# import csv
# import time

# def debug(msg):
#     print(f"DEBUG: {msg}")

# def extract_job_details(job_url):
#     """Fetch individual job listing and extract extra info."""
#     debug(f"Visiting job URL: {job_url}")
#     try:
#         res = requests.get(job_url)
#         debug(f"Detail page status code: {res.status_code}")

#         if res.status_code != 200:
#             debug("Failed to load job detail page.")
#             return {"Location (Detail)": "N/A", "Posted": "N/A", "Company (Detail)": "N/A"}

#         soup = BeautifulSoup(res.text, "html.parser")
#         debug("Parsed job detail HTML.")

#         location_tag = soup.find("span", class_="sc-4cea4a13-10 sc-4cea4a13-11 kAib gsDmFP")
#         date_tag = soup.find("span", class_="sc-4cea4a13-5 sc-4cea4a13-6 vSwDq gItdiZ")
#         company_tag = soup.find("span", class_="sc-4cea4a13-10 sc-4cea4a13-12 iHlvBU sahpA")

#         if location_tag:
#             debug(f"Found location detail: {location_tag.text.strip()}")
#         else:
#             debug("Location detail not found.")

#         if date_tag:
#             debug(f"Found posted date: {date_tag.text.strip()}")
#         else:
#             debug("Posted date not found.")

#         if company_tag:
#             debug(f"Found company detail: {company_tag.text.strip()}")
#         else:
#             debug("Company detail not found.")

#         return {
#             "Location (Detail)": location_tag.text.strip() if location_tag else "N/A",
#             "Posted": date_tag.text.strip() if date_tag else "N/A",
#             "Company (Detail)": company_tag.text.strip() if company_tag else "N/A"
#         }

#     except Exception as e:
#         debug(f"Error during detail page scraping: {e}")
#         return {"Location (Detail)": "N/A", "Posted": "N/A", "Company (Detail)": "N/A"}


# def scrape_talent_jobs(keyword="sales development representative", location="united states", pages=1):
#     debug(f"Starting job scrape for keyword: '{keyword}', location: '{location}', pages: {pages}")
#     base_url = "https://www.talent.com/jobs"
#     all_jobs = []

#     for page in range(1, pages + 1):
#         debug(f"\n--- Scraping page {page} ---")
#         params = {
#             "k": keyword.replace(" ", "+"),
#             "l": location.replace(" ", "+"),
#             "p": page
#         }

#         debug(f"Sending request to: {base_url} with params {params}")
#         response = requests.get(base_url, params=params)
#         debug(f"Page {page} status code: {response.status_code}")

#         if response.status_code != 200:
#             debug(f"Skipping page {page} due to failed load.")
#             continue

#         soup = BeautifulSoup(response.text, "html.parser")
#         debug("Parsed page HTML.")

#         job_cards = soup.find_all("section", class_="sc-8e83a395-1")
#         debug(f"Found {len(job_cards)} job cards on page {page}")

#         for idx, card in enumerate(job_cards):
#             debug(f"\nProcessing job card #{idx+1} on page {page}")
#             title_tag = card.find("h2")
#             link_tag = card.find("a", href=True)

#             if title_tag:
#                 debug(f"Found title: {title_tag.text.strip()}")
#             else:
#                 debug("Title not found.")

#             if link_tag and link_tag.get("href"):
#                 job_url = "https://www.talent.com" + link_tag['href']
#                 debug(f"Found job link: {job_url}")
#             else:
#                 job_url = None
#                 debug("Job link not found.")

#             base_info = {
#                 "Title": title_tag.text.strip() if title_tag else "N/A",
#                 "Link": job_url if job_url else "N/A"
#             }

#             if job_url:
#                 debug("Extracting job detail info...")
#                 detail_info = extract_job_details(job_url)
#                 base_info.update(detail_info)
#                 time.sleep(2)  # ⏳ Increased wait time
#                 debug("Job detail extraction complete.")
#             else:
#                 debug("Skipping job detail extraction due to missing link.")

#             all_jobs.append(base_info)
#             debug(f"Job #{idx+1} collected.")

#     debug(f"\nTotal jobs scraped: {len(all_jobs)}")
#     return all_jobs


# def save_to_csv(jobs, filename="talent_jobs.csv"):
#     debug(f"Saving {len(jobs)} jobs to CSV: {filename}")
#     if not jobs:
#         debug("No jobs to save.")
#         return

#     try:
#         with open(filename, mode="w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
#             writer.writeheader()
#             writer.writerows(jobs)
#         debug("CSV saved successfully.")
#     except Exception as e:
#         debug(f"Failed to save CSV: {e}")

# # Run
# if __name__ == "__main__":
#     debug("Script started.")
#     jobs = scrape_talent_jobs()
#     save_to_csv(jobs)
#     debug("Script finished.")


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timedelta
import re

def debug(msg):
    print(f"DEBUG: {msg}")

def scrape_and_save_jobs(keyword="sales development representative", location="united states", pages=1, filename="talent_jobs.csv"):
    base_url = "https://www.talent.com/jobs"

    # Lists to populate
    job_titles = []
    company_final = []
    locations = []
    job_links = []
    logo_urls = []
    remote_status_list = []
    experience_levels = []
    industry_tag = []
    tools_mentioned_str = []
    date_posted_list = []
    refreshed_this_week_list = []
    outreach_tools_in_job_descriptions_ordered = [    "Salesforce",     "HubSpot",      "Outreach.io",     "SalesLoft",     "LinkedIn Sales Navigator",     "Apollo.io",     "Pipedrive",      "Yesware",      "Woodpecker",      "Reply.io",     "Saleshandy",     "Lemlist",      "Mailshake",     "ZoomInfo",     "Freshsales",     "ActiveCampaign",     "Close.io",      "Groove",     "Instantly.ai",     "Skylead",    "Outplay",    "Zendesk Sell",    "Zoho CRM",    "Keap",    "Mailchimp",    "Constant Contact",    "GetResponse",    "AWeber",    "SendinBlue",    "Mixmax",    "PersistIQ",    "Kixie",    "Callingly","RingCentral","Aircall","Dialpad","JustCall","Five9","Talkdesk"]


    for page in range(1, pages + 1):
        debug(f"\n--- Scraping page {page} ---")
        params = {
            "k": keyword.replace(" ", "+"),
            "l": location.replace(" ", "+"),
            "p": page
        }

        response = requests.get(base_url, params=params)
        #get full URL for debugging
        full_url = response.url
        debug(f"Status code: {response.status_code} from {full_url} with params {params}")
        if response.status_code != 200:
            debug(f"Skipping page {page}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("section", class_="sc-8e83a395-1")
        debug(f"Found {len(job_cards)} job cards on page {page}")

        for idx, card in enumerate(job_cards):
            debug(f"Processing card #{idx+1}")

            title_tag = card.find("h2")
            link_tag = card.find("a", href=True)
            job_url = "https://www.talent.com" + link_tag['href'] if link_tag else "N/A"
            job_title = title_tag.text.strip() if title_tag else "N/A"

            # --- Fetch individual job detail page ---
            comp_name = "N/A"
            loc_detail = "N/A"
            date_posted = "N/A"
            logo_url = "N/A"
            experience_level = "N/A"
            tools_for_job = "N/A"
            parsed_date = None
            refreshed_this_week = False
            remote_status = "On-site"

            if job_url != "N/A":
                try:
                    detail_res = requests.get(job_url)
                    detail_soup = BeautifulSoup(detail_res.text, "html.parser")

                    # Adjust class names as needed
                    location_tag = detail_soup.find("span", class_="sc-4cea4a13-10 sc-4cea4a13-11 kAib gsDmFP")
                    date_tag = detail_soup.find("span", class_="sc-4cea4a13-5 sc-4cea4a13-6 vSwDq gItdiZ")
                    company_tag = detail_soup.find("span", class_="sc-4cea4a13-10 sc-4cea4a13-12 iHlvBU sahpA")
                    logo_tag = detail_soup.find("img")
                    desc_div = detail_soup.find("div", class_="sc-4cea4a13-10 sc-4cea4a13-11 sc-6cde2aa1-10 juWayN gsDmFP bEMPBB")


                    loc_detail = location_tag.text.strip() if location_tag else "N/A"
                    # date_posted = date_tag.text.strip() if date_tag else "N/A"
                    comp_name = company_tag.text.strip() if company_tag else "N/A"
                    logo_url = logo_tag['src'] if logo_tag and logo_tag.has_attr('src') else "N/A"

                    debug(f"Location: {loc_detail}, Date Posted: {date_posted}, Company: {comp_name}")
                    time.sleep(2)


                    if desc_div:
                        full_text = desc_div.get_text(separator=' ', strip=True).lower()
                        debug(f"Full description text length: {len(full_text)}")
                        match = re.search(r'(\d+)\s*(?:-|to)?\s*(\d+)?\s*[\+]?[\s\-]*(years|yrs)', full_text)
                        debug(f"Match found: {match}")
                        if match:
                            min_yrs = int(match.group(1))
                            #if min_yrs is only less than 11, proceed to determine experience level
                            if min_yrs < 11:
                                if min_yrs <= 2:
                                    experience_level = "Entry-level"
                                elif 3 <= min_yrs <= 5:
                                    experience_level = "Mid-level"
                                else:
                                    experience_level = "Senior-level"
                            debug(f"Experience level determined: {experience_level}")
                        else:
                            debug(f"No match found for years pattern in {job_url}")
                        mentioned_tools = [tool for tool in outreach_tools_in_job_descriptions_ordered if tool.lower() in full_text]
                        tools_for_job = ", ".join(mentioned_tools) if mentioned_tools else "None"
                        debug(f"Tools mentioned: {tools_for_job}")

                        text_block = desc_div.get_text(separator=' ', strip=True).lower()
                        if "remote" in text_block:
                            remote_status = "Remote"
                        elif "hybrid" in text_block:
                            remote_status = "Hybrid"
                        else: 
                            remote_status = "On-site"
                    else:
                        debug(f"No description div found in {job_url}")
                        tools_for_job = "None"

                    if date_tag:
                        raw_date = date_tag.text.strip().lower()
                        today = datetime.today()

                        try:
                            if "hour" in raw_date:
                                num = int(re.search(r"\d+", raw_date).group())
                                parsed_date = today - timedelta(hours=num)
                            elif "day" in raw_date:
                                num = int(re.search(r"\d+", raw_date).group())
                                parsed_date = today - timedelta(days=num)
                            elif "week" in raw_date:
                                num = int(re.search(r"\d+", raw_date).group())
                                parsed_date = today - timedelta(weeks=num)
                            elif "month" in raw_date:
                                num = int(re.search(r"\d+", raw_date).group())
                                parsed_date = today - timedelta(weeks=4 * num)
                            else:
                                parsed_date = today

                            refreshed_this_week = (today - parsed_date).days <= 7
                            debug(f"Parsed Date: {parsed_date.strftime('%Y-%m-%d')}, Refreshed This Week: {refreshed_this_week}")

                        except Exception as e:
                            debug(f"Failed to parse date: {e}")
                            parsed_date = None
                            refreshed_this_week = False
                    else:
                        parsed_date = None
                        refreshed_this_week = False

                except Exception as e:
                    debug(f"Error in detail scrape: {e}")

            # Append to lists
            job_titles.append(job_title)
            company_final.append(comp_name)
            locations.append(loc_detail)
            remote_status_list.append(remote_status) 
            job_links.append(job_url)
            logo_urls.append(logo_url)
            experience_levels.append(experience_level)  # Placeholder
            tools_mentioned_str.append(tools_for_job)  # Placeholder
            industry_tag.append("N/A")  # not available on Talent
            date_posted_list.append(parsed_date)
            refreshed_this_week_list.append(refreshed_this_week)  # Placeholder

    # Final DataFrame
    df = pd.DataFrame({
        "Job Title": job_titles,
        "Company": company_final,
        "Location": locations,
        "Remote": remote_status_list,
        "Job URL": job_links,
        "Logo URL": logo_urls,
        "Experience Level": experience_levels,
        "Tools Tags": tools_mentioned_str,
        "Industry Type": industry_tag,
        "Date Posted": date_posted_list,
        "Refreshed This Week": refreshed_this_week_list,
        "Job Portal": ["Talent"] * len(job_titles)
    })
    df["Date Posted"] = pd.to_datetime(df["Date Posted"], errors="coerce").dt.date
    df.to_csv(filename, index=False)
    debug(f"Saved CSV to {filename}")

# Run it
if __name__ == "__main__":
    scrape_and_save_jobs()