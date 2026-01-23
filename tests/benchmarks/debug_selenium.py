"""
Debug script to see what Selenium is actually capturing
"""

import time
import os
import sys

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, '.env'))

from backend.services.legacy_scraper import LegacyCampXScraper
from backend.core.config import Config

def debug_legacy_scraper():
    hall_ticket = Config.EX_HTN
    if not hall_ticket:
        print("EX_HTN not found in environment")
        return

    print(f"Testing Legacy Scraper for: {hall_ticket}")
    
    scraper = LegacyCampXScraper()
    html_content = scraper.fetch_results(hall_ticket)
    
    if html_content:
        # Save the HTML for inspection
        output_path = os.path.join(project_root, 'generated', 'debug_selenium_output.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✅ HTML saved to: {output_path}")
        print(f"HTML Length: {len(html_content)} characters")
        
        # Check for key indicators
        print("\n--- Content Analysis ---")
        print(f"Contains '<table': {'YES' if '<table' in html_content.lower() else 'NO'}")
        print(f"Contains 'hall ticket': {'YES' if 'hall ticket' in html_content.lower() else 'NO'}")
        print(f"Contains 'student name': {'YES' if 'student name' in html_content.lower() else 'NO'}")
        print(f"Contains 'error': {'YES' if 'error' in html_content.lower() else 'NO'}")
        print(f"Contains 'no records': {'YES' if 'no records' in html_content.lower() else 'NO'}")
    else:
        print("❌ No HTML content returned")

if __name__ == "__main__":
    debug_legacy_scraper()
