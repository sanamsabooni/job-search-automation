#!/usr/bin/env python3
"""
Job Scraper Module
Scans job boards and extracts job listings.
Can be used standalone or integrated with n8n via HTTP endpoint.
"""

import requests
import json
import os
from typing import List, Dict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JobScraper:
    """Job board scraper with support for multiple sources."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        })
    
    def scrape_greenhouse(self, company_id: str = None) -> List[Dict]:
        """Scrape jobs from Greenhouse job boards."""
        jobs = []
        try:
            if company_id:
                url = f"https://boards-api.greenhouse.io/v1/boards/{company_id}/jobs"
            else:
                # Example company
                url = "https://boards-api.greenhouse.io/v1/boards/example/jobs"
            
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            for job in data.get('jobs', []):
                jobs.append({
                    'title': job.get('title'),
                    'location': job.get('location', {}).get('name'),
                    'url': job.get('absolute_url'),
                    'department': job.get('departments', [{}])[0].get('name'),
                    'source': 'greenhouse'
                })
            
            logger.info(f"Scraped {len(jobs)} jobs from Greenhouse")
        except Exception as e:
            logger.error(f"Error scraping Greenhouse: {e}")
        
        return jobs
    
    def scrape_lever(self, company_name: str = None) -> List[Dict]:
        """Scrape jobs from Lever job boards."""
        jobs = []
        try:
            if company_name:
                url = f"https://api.lever.co/v0/postings/{company_name}"
            else:
                # Example company
                url = "https://api.lever.co/v0/postings/example"
            
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            for job in data:
                jobs.append({
                    'title': job.get('text'),
                    'location': job.get('categories', {}).get('location'),
                    'url': job.get('hostedUrl'),
                    'department': job.get('categories', {}).get('team'),
                    'source': 'lever'
                })
            
            logger.info(f"Scraped {len(jobs)} jobs from Lever")
        except Exception as e:
            logger.error(f"Error scraping Lever: {e}")
        
        return jobs
    
    def scrape_workable(self, company_name: str = None) -> List[Dict]:
        """Scrape jobs from Workable job boards."""
        jobs = []
        try:
            if company_name:
                url = f"https://apply.workable.com/api/v1/widget/accounts/{company_name}"
            else:
                url = "https://apply.workable.com/api/v1/widget/accounts/example"
            
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            for job in data.get('jobs', []):
                jobs.append({
                    'title': job.get('title'),
                    'location': job.get('location', {}).get('city'),
                    'url': f"https://apply.workable.com/{company_name}/j/{job.get('shortcode')}/",
                    'department': job.get('department'),
                    'source': 'workable'
                })
            
            logger.info(f"Scraped {len(jobs)} jobs from Workable")
        except Exception as e:
            logger.error(f"Error scraping Workable: {e}")
        
        return jobs
    
    def normalize_job_data(self, jobs: List[Dict]) -> List[Dict]:
        """Normalize job data with consistent fields."""
        normalized = []
        for job in jobs:
            normalized.append({
                'title': job.get('title', 'Unknown'),
                'company': job.get('company', 'Unknown'),
                'location': job.get('location', 'Remote'),
                'url': job.get('url', ''),
                'department': job.get('department', 'General'),
                'source': job.get('source', 'unknown'),
                'scraped_at': datetime.now().isoformat()
            })
        return normalized
    
    def save_to_json(self, jobs: List[Dict], filename: str = 'jobs.json'):
        """Save jobs to JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(jobs, f, indent=2)
            logger.info(f"Saved {len(jobs)} jobs to {filename}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")


def main():
    """
    Main execution function.
    """
    scraper = JobScraper()
    
    # Scrape from multiple sources
    all_jobs = []
    
    # Example: Scrape Greenhouse
    greenhouse_jobs = scraper.scrape_greenhouse()
    all_jobs.extend(greenhouse_jobs)
    
    # Example: Scrape Lever (add company names)
    # lever_jobs = scraper.scrape_lever('company-name')
    # all_jobs.extend(lever_jobs)
    
    # Normalize data
    normalized_jobs = scraper.normalize_job_data(all_jobs)
    
    # Save results
    scraper.save_to_json(normalized_jobs)
    
    print(f"\nTotal jobs scraped: {len(normalized_jobs)}")
    print(f"Sources: {set(job['source'] for job in normalized_jobs)}")


if __name__ == "__main__":
    main()
