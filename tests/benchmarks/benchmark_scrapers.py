
"""
Benchmark Script: Legacy (Selenium) vs New (Direct API)
"""

import time
import os
import sys
import json
import logging

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, '.env'))

from backend.services.scraper import CampXScraper
from backend.services.legacy_scraper import LegacyCampXScraper
from backend.services.parser import ResultsParser
from backend.core.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Benchmark")

def run_benchmark():
    hall_ticket = Config.EX_HTN
    if not hall_ticket:
        logger.error("EX_HTN not found in environment")
        return

    logger.info(f"Starting benchmark for Hall Ticket: {hall_ticket}")
    
    parser = ResultsParser()
    
    # --- TEST 1: New API Scraper ---
    logger.info("\n--- Testing New API Scraper ---")
    start_time_api = time.time()
    try:
        api_scraper = CampXScraper()
        api_data = api_scraper.fetch_results(hall_ticket)
        api_duration = time.time() - start_time_api
        
        if api_data:
            parsed_api = parser.parse_api_response(api_data)
            status_api = "SUCCESS"
            subject_count_api = len(parsed_api.get('subjects', []))
        else:
            status_api = "FAILED"
            subject_count_api = 0
            
    except Exception as e:
        api_duration = time.time() - start_time_api
        status_api = f"ERROR: {str(e)}"
        subject_count_api = 0

    logger.info(f"API Method: {status_api} in {api_duration:.2f}s (Subjects: {subject_count_api})")

    # --- TEST 2: Legacy Selenium Scraper ---
    logger.info("\n--- Testing Legacy Selenium Scraper ---")
    start_time_legacy = time.time()
    try:
        legacy_scraper = LegacyCampXScraper()
        html_content = legacy_scraper.fetch_results(
            hall_ticket=hall_ticket,
            exam_type='General',  # Must provide exam type
            view_type='All Semesters'
        )
        legacy_duration = time.time() - start_time_legacy
        
        if html_content:
            parsed_legacy = parser.parse_results(html_content)
            status_legacy = "SUCCESS"
            subject_count_legacy = len(parsed_legacy.get('subjects', []))
        else:
            status_legacy = "FAILED"
            subject_count_legacy = 0
            
    except Exception as e:
        legacy_duration = time.time() - start_time_legacy
        status_legacy = f"ERROR: {str(e)}"
        subject_count_legacy = 0
        
    logger.info(f"Legacy Method: {status_legacy} in {legacy_duration:.2f}s (Subjects: {subject_count_legacy})")
    
    # --- SUMMARY ---
    logger.info("\n" + "="*30)
    logger.info("BENCHMARK SUMMARY")
    logger.info("="*30)
    logger.info(f"API Time    : {api_duration:.2f}s")
    logger.info(f"Legacy Time : {legacy_duration:.2f}s")
    
    if api_duration > 0 and legacy_duration > 0:
        speedup = legacy_duration / api_duration
        logger.info(f"Speedup     : {speedup:.2f}x faster")
    
    logger.info(f"Data Match  : {'YES' if subject_count_api == subject_count_legacy else 'NO'}")
    logger.info("="*30)

if __name__ == "__main__":
    run_benchmark()
