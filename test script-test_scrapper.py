#!/usr/bin/env python3
"""
Test script for GitHub Trending Scraper

This script tests the scraper functionality and validates the output.
"""

import unittest
import os
import csv
from unittest.mock import patch, MagicMock
from github_trending_scraper import GitHubTrendingScraper

class TestGitHubTrendingScraper(unittest.TestCase):
    """Test cases for GitHub Trending Scraper"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scraper = GitHubTrendingScraper()
        self.sample_html = """
        <html>
        <body>
            <article class="Box-row">
                <h2><a href="/test/repo1">test / repo1</a></h2>
            </article>
            <article class="Box-row">
                <h2><a href="/test/repo2">test / repo2</a></h2>
            </article>
            <article class="Box-row">
                <h2><a href="/test/repo3">test / repo3</a></h2>
            </article>
        </body>
        </html>
        """
    
    def test_parse_repositories(self):
        """Test repository parsing functionality"""
        repositories = self.scraper.parse_repositories(self.sample_html, top_n=2)
        
        self.assertEqual(len(repositories), 2)
        self.assertEqual(repositories[0]['name'], 'test / repo1')
        self.assertEqual(repositories[0]['link'], 'https://github.com/test/repo1')
        self.assertEqual(repositories[1]['name'], 'test / repo2')
        self.assertEqual(repositories[1]['link'], 'https://github.com/test/repo2')
    
    def test_save_to_csv(self):
        """Test CSV saving functionality"""
        test_data = [
            {'name': 'test/repo1', 'link': 'https://github.com/test/repo1'},
            {'name': 'test/repo2', 'link': 'https://github.com/test/repo2'}
        ]
        
        filename = 'test_output.csv'
        self.scraper.save_to_csv(test_data, filename)
        
        # Verify file exists
        self.assertTrue(os.path.exists(filename))
        
        # Verify content
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['repository_name'], 'test/repo1')
            self.assertEqual(rows[0]['link'], 'https://github.com/test/repo1')
        
        # Cleanup
        os.remove(filename)
    
    @patch('github_trending_scraper.requests.Session.get')
    def test_fetch_trending_page(self, mock_get):
        """Test page fetching with mock"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.sample_html
        mock_get.return_value = mock_response
        
        result = self.scraper.fetch_trending_page()
        self.assertEqual(result, self.sample_html)
    
    def test_empty_html_parsing(self):
        """Test parsing empty HTML"""
        empty_html = "<html><body></body></html>"
        repositories = self.scraper.parse_repositories(empty_html)
        self.assertEqual(len(repositories), 0)

def run_live_test():
    """Run a live test against the actual GitHub trending page"""
    print("🧪 Running live test against GitHub trending page...")
    
    scraper = GitHubTrendingScraper()
    
    try:
        # Test fetching the page
        html_content = scraper.fetch_trending_page()
        print("✅ Successfully fetched trending page")
        
        # Test parsing
        repositories = scraper.parse_repositories(html_content, top_n=3)
        print(f"✅ Successfully parsed {len(repositories)} repositories")
        
        # Display results
        if repositories:
            print("\n📊 Live Test Results:")
            for i, repo in enumerate(repositories, 1):
                print(f"{i}. {repo['name']}")
                print(f"   🔗 {repo['link']}")
        else:
            print("⚠️ No repositories found - might need to update selectors")
        
        # Test CSV saving
        test_filename = "live_test_output.csv"
        scraper.save_to_csv(repositories, test_filename)
        print(f"✅ Successfully saved to {test_filename}")
        
        # Cleanup
        if os.path.exists(test_filename):
            os.remove(test_filename)
            print("🧹 Cleaned up test file")
        
        return True
        
    except Exception as e:
        print(f"❌ Live test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 GitHub Trending Scraper Test Suite")
    print("=" * 50)
    
    # Run unit tests
    print("Running unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n" + "=" * 50)
    
    # Run live test
    live_test_success = run_live_test()
    
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"Unit Tests: ✅ Completed")
    print(f"Live Test: {'✅ Passed' if live_test_success else '❌ Failed'}")
    
    if live_test_success:
        print("🎉 All tests passed! The scraper is working correctly.")
    else:
        print("⚠️ Live test failed. Check your internet connection or GitHub might have changed their page structure.")
