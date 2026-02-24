import requests
from bs4 import BeautifulSoup
import time
import random
from app.models import Job
from app.services.scrapers.base_scraper import BaseScraper

class WWRScraper(BaseScraper):
    def __init__(self, db):
        super().__init__(db)
        self.url = "https://weworkremotely.com/categories/remote-back-end-programming-jobs"
        self.source = "WeWorkRemotely"
    
    def scrape(self):
        print(f"[*] {self.url} data is being scraped...")
        added_count = 0

        try:
            response = requests.get(self.url, headers=self.get_headers())
            soup = BeautifulSoup(response.content, 'html.parser')

            job_listings = soup.select('li.new-listing-container')

            for job_item in job_listings:
                title_elem = job_item.select_one('h3.new-listing__header__title')
                company_elem = job_item.select_one('p.new-listing__company-name')
                link_elem = job_item.select_one('a[href*="/remote-jobs/"]')

                if title_elem and link_elem:
                    title = title_elem.text.strip()
                    company_name = company_elem.text.strip() if company_elem else "Unknown"
                    link = f"https://weworkremotely.com{link_elem['href']}"

                    if self.db.query(Job).filter(Job.link == link).first():
                        continue

                    print(f"scraping details for: {title} at {company_name}")

                    try:
                        time.sleep(random.uniform(1.5,3.0))
                        detail_response = requests.get(link,headers=self.get_headers())
                        detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

                        desc_div = detail_soup.select_one('div.lis-container__job__content__description')
                        if not desc_div:
                            desc_div = detail_soup.select_one('div#job-listing-show-container')

                            
                        full_description = desc_div.text.strip() if desc_div else "No description available."

                    except Exception as e:
                        full_description = "Error fetching description."
                        print(f"Error fetching details for {title}: {e}")
                    
                    new_job = Job(
                        title=title,
                        company=company_name,
                        location="Remote",
                        description=full_description,
                        link=link,
                        source=self.source
                    )  
                    self.db.add(new_job)
                    added_count += 1
            
            self.db.commit()
            print(f"[*] {added_count} new jobs added from {self.source}.")

        except Exception as e:
            print(f"Error scraping {self.source}: {e}")

                








