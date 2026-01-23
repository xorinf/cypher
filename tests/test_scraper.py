"""
Test script for CampX scraper
Tests if we can fetch results from the configured results portal

NOTE: This test requires:
1. A configured .env file with CAMPX_BASE_URL set to your university's portal
2. A valid hallticket number for your university
"""

import sys
import os

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.scraper import CampXScraper
from services.parser import ResultsParser
import json

def test_scraper_with_real_data():
    """
    Test the scraper with a real hallticket number
    
    IMPORTANT: Replace YOUR_HALLTICKET_HERE with your actual hallticket
    """
    
    # Initialize scraper and parser
    scraper = CampXScraper()
    parser = ResultsParser()
    
    # TODO: Replace with your actual hallticket number
    test_hallticket = "YOUR_HALLTICKET_HERE"
    
    if test_hallticket == "YOUR_HALLTICKET_HERE":
        print("\n" + "="*60)
        print("⚠️  CONFIGURATION NEEDED")
        print("="*60)
        print("Please update the test_hallticket variable in this script")
        print("with your actual hallticket number before running tests.")
        print("="*60 + "\n")
        return False
    
    print(f"\n{'='*60}")
    print(f"Testing CampX Scraper")
    print(f"{'='*60}")
    print(f"Hall Ticket: {test_hallticket}")
    print(f"Target URL: {scraper.base_url}")
    print(f"{'='*60}\n")
    
    # Fetch results
    print("Step 1: Fetching results from configured portal...")
    html_content = scraper.fetch_results(
        hall_ticket=test_hallticket,
        exam_type='General',
        view_type='All Semesters'
    )
    
    if not html_content:
        print("\n❌ Failed to fetch results!")
        print("Possible reasons:")
        print("  - Invalid hallticket number")
        print("  - CAMPX_BASE_URL not configured in .env")
        print("  - Network issue")
        print("  - ChromeDriver not installed or incompatible")
        print("  - Website structure changed")
        return False
    
    print(f"✅ Successfully fetched HTML content ({len(html_content)} characters)")
    
    # Save raw HTML for inspection (will be ignored by git)
    output_file = os.path.join(os.path.dirname(__file__), "..", "backend", "test_output.html")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ Saved raw HTML to {output_file}")
    
    # Parse the results
    print("\nStep 2: Parsing HTML content...")
    parsed_data = parser.parse_results(html_content)
    
    if not parsed_data:
        print("\n⚠️  No data could be parsed from HTML")
        print("Checking HTML content...")
        
        # Check for common error messages
        html_lower = html_content.lower()
        if 'no records' in html_lower:
            print("  → Found 'no records' message - hallticket may be invalid")
        elif 'invalid' in html_lower:
            print("  → Found 'invalid' message - hallticket may be invalid")
        elif 'error' in html_lower:
            print("  → Found 'error' message in response")
        else:
            print("  → HTML received but couldn't identify structure")
            print(f"  → HTML preview (first 500 chars):")
            print(f"     {html_content[:500]}")
        
        return False
    
    print("✅ Successfully parsed results!")
    
    # Display parsed data
    print(f"\n{'='*60}")
    print("PARSED DATA:")
    print(f"{'='*60}")
    print(json.dumps(parsed_data, indent=2))
    
    # Save parsed data (will be ignored by git)
    json_file = os.path.join(os.path.dirname(__file__), "..", "backend", "test_output.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=2)
    print(f"\n✅ Saved parsed data to {json_file}")
    
    return True


def test_parser_with_mock_data():
    """
    Test the parser with mock fixture data (no network/scraper needed)
    """
    parser = ResultsParser()
    
    print(f"\n{'='*60}")
    print(f"Testing Parser with Mock Data")
    print(f"{'='*60}\n")
    
    # Load mock HTML fixture
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "mock_results.html")
    
    if not os.path.exists(fixture_path):
        print(f"❌ Mock fixture not found at {fixture_path}")
        return False
    
    with open(fixture_path, 'r', encoding='utf-8') as f:
        mock_html = f.read()
    
    print(f"✅ Loaded mock HTML fixture ({len(mock_html)} characters)")
    
    # Parse the mock data
    parsed_data = parser.parse_results(mock_html)
    
    if not parsed_data:
        print("❌ Failed to parse mock data")
        return False
    
    print("✅ Successfully parsed mock data!")
    print(f"\n{'='*60}")
    print("PARSED MOCK DATA:")
    print(f"{'='*60}")
    print(json.dumps(parsed_data, indent=2))
    
    return True


if __name__ == "__main__":
    print("\n" + "="*60)
    print("CYPHER TEST SUITE")
    print("="*60)
    
    # Check if .env is configured
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "..", ".env")):
        print("\n⚠️  WARNING: .env file not found!")
        print("Please create a .env file from .env.example")
        print("and configure CAMPX_BASE_URL\n")
    
    choice = input("\nSelect test mode:\n1. Test with mock data (no network)\n2. Test with real data (requires hallticket)\n\nChoice (1-2): ")
    
    try:
        if choice == "1":
            success = test_parser_with_mock_data()
        elif choice == "2":
            success = test_scraper_with_real_data()
        else:
            print("Invalid choice")
            sys.exit(1)
        
        if success:
            print("\n✅ TEST PASSED")
        else:
            print("\n❌ TEST FAILED")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ TEST CRASHED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
