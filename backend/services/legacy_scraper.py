"""
Legacy CampX Web Scraper Service (Selenium)
Handles form submission and result retrieval from CampX system via Browser Automation
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os

# Add parent directory to path to allow imports if running as script
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from core.config import Config
from core.logger import setup_logger

logger = setup_logger(__name__ + "_legacy")

class LegacyCampXScraper:
    """Web scraper for CampX results page"""
    
    def __init__(self):
        self.base_url = Config.CAMPX_BASE_URL
        if not self.base_url:
            logger.error("CAMPX_BASE_URL is not configured")
            raise ValueError("CAMPX_BASE_URL environment variable is not set")
            
        self.driver = None
    
    def _init_driver(self):
        """Initialize Selenium WebDriver with Chrome"""
        chrome_options = Options()
        if Config.HEADLESS_MODE:
            chrome_options.add_argument('--headless')
            
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Anti-detection measures
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            logger.info("ChromeDriver initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing ChromeDriver: {str(e)}")
            raise
    
    def _close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.debug("WebDriver closed")
    
    def fetch_results(self, hall_ticket, exam_type='', view_type='All Semesters'):
        """
        Fetch results by submitting the form on CampX
        """
        try:
            self._init_driver()
            
            logger.info(f"Navigating to {self.base_url}")
            self.driver.get(self.base_url)
            
            wait = WebDriverWait(self.driver, 10)
            
            # Fill hall ticket
            self._fill_hall_ticket(wait, hall_ticket)
            
            # Handle dropdowns
            if exam_type:
                self._select_dropdown(wait, 'examType', exam_type)
            
            if view_type:
                self._select_dropdown(wait, 'viewType', view_type)
            
            # Submit
            self._click_submit(wait)
            
            # Validate results
            return self._get_page_content()
            
        except TimeoutException:
            logger.error("Timeout while waiting for page elements")
            return None
        except Exception as e:
            logger.error(f"Error during legacy scraping: {str(e)}")
            return None
        finally:
            self._close_driver()

    def _fill_hall_ticket(self, wait, hall_ticket):
        hall_ticket_input = wait.until(
            EC.presence_of_element_located((By.ID, 'rollNo'))
        )
        hall_ticket_input.clear()
        hall_ticket_input.send_keys(hall_ticket)
        logger.info(f"Entered hall ticket: {hall_ticket}")

    def _select_dropdown(self, wait, element_id, value):
        try:
            # Click dropdown
            dropdown = wait.until(EC.element_to_be_clickable((By.ID, element_id)))
            dropdown.click()
            time.sleep(0.5) # Animation wait
            
            # Map values
            target_text = self._map_dropdown_value(element_id, value)
            
            # Click option
            option = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    f"//li[@role='option' and contains(text(), '{target_text}')]"
                ))
            )
            option.click()
            logger.info(f"Selected {element_id}: {target_text}")
            
        except Exception as e:
            logger.warning(f"Failed to select {element_id} '{value}': {str(e)}")

    def _map_dropdown_value(self, element_id, value):
        val_lower = value.lower()
        if element_id == 'examType':
            if val_lower in ['regular', 'general']: return 'General'
            if val_lower in ['honors', 'minors']: return 'Honors and Minors'
        elif element_id == 'viewType':
            if val_lower in ['all semesters']: return 'All Semesters'
            if val_lower in ['current semester', 'single semester']: return 'Single Semester'
        return value

    def _click_submit(self, wait):
        btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Get Result')]"))
        )
        btn.click()
        logger.info("Clicked 'Get Result' button")
        
        # Wait for results to load (SPA needs time to fetch from API)
        # Look for table or result container to appear
        try:
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//table | //div[contains(@class, 'MuiTableContainer')]"))
            )
            time.sleep(2)  # Extra time for all data to render
            logger.info("Results table loaded")
        except TimeoutException:
            logger.warning("Results table did not load within timeout")
            time.sleep(3)  # Fallback wait

    def _get_page_content(self):
        page_source = self.driver.page_source
        
        # Check for actual error messages or empty states
        page_lower = page_source.lower()
        
        # Look for positive indicators first
        has_table = '<table' in page_lower or 'muitable' in page_lower
        has_student_info = 'hall ticket' in page_lower or 'student name' in page_lower
        
        # Check for negative indicators
        has_error = 'no records found' in page_lower or 'invalid hall ticket' in page_lower or 'error' in page_lower
        
        if has_error and not (has_table or has_student_info):
            logger.warning("Error message detected or no results found - returning anyway for debug")
            return page_source  # Temporarily return for debugging
        
        if has_table or has_student_info:
            logger.info("Results retrieved successfully")
            return page_source
        
        logger.warning("Unable to determine if results were loaded successfully")
        return page_source  # Return anyway and let parser handle it
