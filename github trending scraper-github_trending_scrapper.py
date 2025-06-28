#!/usr/bin/env python3
"""
GitHub Trending Repository Scraper

This script scrapes the top 5 trending repositories from GitHub's trending page
and saves the results to a CSV file with repository names and links.

Author: GitHub Trending Scraper
Date: 2025
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GitHubTrendingScraper:
    """A scraper for GitHub trending repositories"""
    
    def __init__(self):
        self.base_url = "https://github.com"
        self.trending_url = "https://github.com/trending"
        self.session = requests.Session()
        
        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def fetch_trending_page(self):
        """Fetch the GitHub trending page content"""
        try:
            logger.info(f"Fetching trending page: {self.trending_url}")
            response = self.session.get(self.trending_url, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Successfully fetched page. Status code: {response.status_code}")
            return response.text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching page: {e}")
            raise
    
    def parse_repositories(self, html_content, top_n=5):
        """Parse the HTML content to extract repository information"""
        soup = BeautifulSoup(html_content, 'html.parser')
        repositories = []
        
        # Find repository containers - GitHub uses different selectors over time
        # Let's try multiple selectors to be robust
        selectors = [
            'article.Box-row',
            '.Box-row',
            'article[class*="Box-row"]',
            '.repo-list-item',
            '[data-testid="repository-item"]'
        ]
        
        repo_elements = []
        for selector in selectors:
            repo_elements = soup.select(selector)
            if repo_elements:
                logger.info(f"Found {len(repo_elements)} repositories using selector: {selector}")
                break
        
        if not repo_elements:
            # Fallback: look for h2 elements with repository links
            logger.warning("Standard selectors failed, trying fallback method")
            h2_elements = soup.find_all('h2', class_=lambda x: x and 'h3' in x)
            for h2 in h2_elements[:top_n]:
                link_elem = h2.find('a')
                if link_elem and link_elem.get('href'):
                    repo_name = link_elem.get_text(strip=True)
                    repo_link = self.base_url + link_elem['href']
                    repositories.append({
                        'name': repo_name,
                        'link': repo_link
                    })
        else:
            # Parse repository information from found elements
            for idx, element in enumerate(repo_elements[:top_n]):
                try:
                    # Try different ways to find the repository name and link
                    repo_link_elem = None
                    
                    # Method 1: Look for h2 with link
                    h2_elem = element.find('h2')
                    if h2_elem:
                        repo_link_elem = h2_elem.find('a')
                    
                    # Method 2: Look for direct link in the element
                    if not repo_link_elem:
                        repo_link_elem = element.find('a', href=lambda x: x and x.startswith('/'))
                    
                    # Method 3: Look for any link that looks like a repository
                    if not repo_link_elem:
                        all_links = element.find_all('a')
                        for link in all_links:
                            href = link.get('href', '')
                            if '/' in href and not href.startswith('http') and len(href.split('/')) >= 2:
                                repo_link_elem = link
                                break
                    
                    if repo_link_elem:
                        repo_name = repo_link_elem.get_text(strip=True)
                        # Clean up repository name (remove extra whitespace, newlines)
                        repo_name = ' '.join(repo_name.split())
                        
                        repo_href = repo_link_elem.get('href', '')
                        if repo_href.startswith('/'):
                            repo_link = self.base_url + repo_href
                        else:
                            repo_link = repo_href
                        
                        if repo_name and repo_link:
                            repositories.append({
                                'name': repo_name,
                                'link': repo_link
                            })
                            logger.info(f"Found repository {idx + 1}: {repo_name}")
                    
                except Exception as e:
                    logger.warning(f"Error parsing repository element {idx + 1}: {e}")
                    continue
        
        logger.info(f"Successfully parsed {len(repositories)} repositories")
        return repositories
    
    def save_to_csv(self, repositories, filename="trending_repositories.csv"):
        """Save repositories to CSV file"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['repository_name', 'link']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write repository data
                for repo in repositories:
                    writer.writerow({
                        'repository_name': repo['name'],
                        'link': repo['link']
                    })
            
            logger.info(f"Successfully saved {len(repositories)} repositories to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            raise
    
    def scrape_trending(self, top_n=5):
        """Main method to scrape trending repositories"""
        try:
            logger.info("Starting GitHub trending repositories scraper")
            logger.info(f"Target: Top {top_n} repositories")
            
            # Fetch the page
            html_content = self.fetch_trending_page()
            
            # Parse repositories
            repositories = self.parse_repositories(html_content, top_n)
            
            if not repositories:
                logger.error("No repositories found. The page structure might have changed.")
                return None
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trending_repositories_{timestamp}.csv"
            
            # Save to CSV
            saved_file = self.save_to_csv(repositories, filename)
            
            # Print results
            print(f"\n🎉 Successfully scraped {len(repositories)} trending repositories!")
            print(f"📁 Saved to: {saved_file}")
            print(f"📊 Results:")
            print("-" * 80)
            for i, repo in enumerate(repositories, 1):
                print(f"{i}. {repo['name']}")
                print(f"   🔗 {repo['link']}")
                print()
            
            return repositories
            
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            return None

def main():
    """Main function to run the scraper"""
    print("🚀 GitHub Trending Repository Scraper")
    print("=" * 50)
    
    scraper = GitHubTrendingScraper()
    
    try:
        # Scrape top 5 trending repositories
        repositories = scraper.scrape_trending(top_n=5)
        
        if repositories:
            print("✅ Scraping completed successfully!")
        else:
            print("❌ Scraping failed. Check the logs for more details.")
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        logger.error(f"Main execution failed: {e}")

if __name__ == "__main__":
    main()
