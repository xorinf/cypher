"""
CampX API Scraper Service
Handles direct API communication to fetch results
"""

import requests
import json
import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from core.config import Config
from core.logger import setup_logger

logger = setup_logger(__name__)

class CampXScraper:
    """API Client for CampX results"""
    
    def __init__(self):
        # Use API URL from config
        self.api_url = Config.CAMPX_API_URL
        if not self.api_url:
            raise ValueError("CAMPX_API_URL not set in config")
        
        # Derive generic referer or use base url
        referer = Config.CAMPX_BASE_URL
        if not referer:
             raise ValueError("CAMPX_BASE_URL not set in config")
        if not referer.endswith('/'):
            referer += '/'
            
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Referer": referer,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-api-version": "2",
            "x-institution-code": Config.CAMPX_INSTITUTION_CODE,
            "x-tenant-id": Config.CAMPX_TENANT_ID
        }
    
    def fetch_results(self, hall_ticket, exam_type='general', view_type='All Semesters'):
        """
        Fetch results directly from API
        Returns: Dict (JSON response) or None
        """
        try:
            params = {
                'examType': exam_type.lower() if exam_type else 'general',
                'rollNo': hall_ticket
            }
            
            logger.info(f"Fetching results from API for {hall_ticket}")
            
            response = requests.get(
                self.api_url, 
                params=params, 
                headers=self.headers, 
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("API request successful")
                return response.json()
            elif response.status_code == 404:
                logger.warning(f"No results found for {hall_ticket}")
                return None
            else:
                logger.error(f"API request failed with status {response.status_code}: {response.text}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Network error during API fetch: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error fetching results: {str(e)}")
            return None
