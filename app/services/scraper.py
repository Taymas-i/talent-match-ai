import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.models import Job
import time
import random

class JobScraper:
    def __init__(self, db: Session):
        self.db = db
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def scrape_pythone_org(self):
        url = "https://www.python.org/jobs/"
        print(f"Scraping {url}...")

        try:
            response = requests.get(url,headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            job_list = soup.find('ol', class_ = 'list-recent-jobs')
            if not job_list:
                print("No job listings found on python.org")
                return
            
            jobs = job_list.find_all('li')
            added_count = 0

            for job in jobs:
                title_elem = job.find('h2', class_='listing-company')
                if not title_elem:
                    continue

                title_link = title_elem.find('a')
                title = title_link.text.strip()
                link = "https://www.python.org" + title_link['href']

                #company
                company_name = title_elem.contents[-1].strip()
                if company_name.startswith(","):
                    company_name = company_name[1:].strip()

                #location
                location_elem = job.find('span', class_='listing-location')
                location = location_elem.text.strip() if location_elem else "unknown"

                # control for duplicates based on the unique link (critical to prevent data pollution)
                existing_job = self.db.query(Job).filter(Job.link == link).first()
                if existing_job:
                    continue

                new_job = Job(
                    title=title,
                    company=company_name,
                    location=location,
                    description="Detaylar linkte", 
                    link=link,
                    source="Python.org"
                )
                self.db.add(new_job)
                added_count += 1

                time.sleep(random.uniform(0.1, 0.5))

            self.db.commit()
            print(f"Added {added_count} new jobs from python.org")

        except Exception as e:
            print(f"Error scraping python.org: {e}")
            self.db.rollback()
