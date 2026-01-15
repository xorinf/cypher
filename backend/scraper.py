"""
CampX Web Scraper
Handles form submission and result retrieval from CampX system
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time


class CampXScraper:
    """Web scraper for CampX results page"""
    
    def __init__(self):
        self.base_url = os.getenv('CAMPX_BASE_URL', 'https://aupulse.campx.in/aupulse/ums/results')
        self.driver = None
    
    def _init_driver(self):
        """Initialize Selenium WebDriver with Chrome"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
    
    def _close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def fetch_results(self, hall_ticket, exam_type='', view_type='All Semesters'):
        """
        Fetch results by submitting the form on CampX
        
        Args:
            hall_ticket (str): Student hall ticket number
            exam_type (str): Exam type selection (optional)
            view_type (str): View type (default: 'All Semesters')
            
        Returns:
            str: HTML content of the results page, or None if failed
        """
        try:
            self._init_driver()
            
            # Navigate to the results page
            print(f"Navigating to {self.base_url}")
            self.driver.get(self.base_url)
            
            # Wait for the page to load
            wait = WebDriverWait(self.driver, 10)
            
            # Fill in hall ticket number
            hall_ticket_input = wait.until(
                EC.presence_of_element_located((By.ID, 'rollNo'))
            )
            hall_ticket_input.clear()
            hall_ticket_input.send_keys(hall_ticket)
            print(f"Entered hall ticket: {hall_ticket}")
            
            # Select exam type if provided
            if exam_type:
                try:
                    exam_type_select = Select(self.driver.find_element(By.ID, 'examType'))
                    exam_type_select.select_by_visible_text(exam_type)
                    print(f"Selected exam type: {exam_type}")
                except NoSuchElementException:
                    print("Exam type dropdown not found or exam type not available")
            
            # Select view type
            try:
                view_type_select = Select(self.driver.find_element(By.ID, 'viewType'))
                view_type_select.select_by_visible_text(view_type)
                print(f"Selected view type: {view_type}")
            except NoSuchElementException:
                print("View type dropdown not found")
            
            # Click the "Get Result" button
            get_result_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Get Result')]"))
            )
            get_result_button.click()
            print("Clicked 'Get Result' button")
            
            # Wait for results to load (adjust timeout as needed)
            time.sleep(3)
            
            # Check if results loaded or if there's an error
            page_source = self.driver.page_source
            
            # Basic validation - check if we got a results page
            if 'no records' in page_source.lower() or 'invalid' in page_source.lower():
                print("No results found or invalid hall ticket")
                return None
            
            print("Results retrieved successfully")
            return page_source
            
        except TimeoutException:
            print("Timeout while waiting for elements to load")
            return None
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            return None
        finally:
            self._close_driver()
