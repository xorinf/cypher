"""
Unit tests for CampXScraper (API method)
"""

import pytest
from unittest.mock import Mock, patch
from backend.services.scraper import CampXScraper


class TestCampXScraper:
    
    def test_init_with_valid_config(self):
        """Test scraper initialization with valid configuration"""
        scraper = CampXScraper()
        assert scraper.api_url is not None
        assert scraper.headers is not None
        assert 'x-institution-code' in scraper.headers
        assert 'x-tenant-id' in scraper.headers
    
    @patch('backend.services.scraper.requests.get')
    def test_fetch_results_success(self, mock_get):
        """Test successful result fetching"""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'student': {'rollNo': '12345', 'fullName': 'Test Student'},
            'results': []
        }
        mock_get.return_value = mock_response
        
        scraper = CampXScraper()
        result = scraper.fetch_results('12345')
        
        assert result is not None
        assert 'student' in result
        assert result['student']['rollNo'] == '12345'
    
    @patch('backend.services.scraper.requests.get')
    def test_fetch_results_not_found(self, mock_get):
        """Test fetching results with invalid hall ticket"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        scraper = CampXScraper()
        result = scraper.fetch_results('INVALID')
        
        assert result is None
    
    @patch('backend.services.scraper.requests.get')
    def test_fetch_results_network_error(self, mock_get):
        """Test handling of network errors"""
        mock_get.side_effect = Exception("Network error")
        
        scraper = CampXScraper()
        result = scraper.fetch_results('12345')
        
        assert result is None
    
    def test_headers_contain_required_fields(self):
        """Test that headers contain all required fields"""
        scraper = CampXScraper()
        
        required_headers = [
            'Accept',
            'Referer',
            'User-Agent',
            'x-api-version',
            'x-institution-code',
            'x-tenant-id'
        ]
        
        for header in required_headers:
            assert header in scraper.headers
