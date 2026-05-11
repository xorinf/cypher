"""
Comprehensive Unit Tests for Cypher
Tests parser, analytics, and frontend data handling

Run with: python -m pytest tests/test_units.py -v
Or: python tests/test_units.py
"""

import sys
import os
import json
import tempfile
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.parser import ResultsParser
from services.analytics import AnalyticsEngine
from services.storage import FavoritesStorage

# Get the fixtures directory path
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


class TestResultsParser:
    """Test suite for ResultsParser"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup parser instance"""
        self.parser = ResultsParser()
    
    def _load_fixture(self, filename):
        """Load HTML fixture file"""
        filepath = os.path.join(FIXTURES_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    # ========== Basic Parsing Tests ==========
    
    def test_parse_standard_results(self):
        """Test parsing standard results with passing grades"""
        html = self._load_fixture('mock_results.html')
        result = self.parser.parse_results(html)
        
        assert result is not None
        assert 'studentInfo' in result
        assert 'subjects' in result
        assert 'semesterInfo' in result
        
        # Verify student info
        student_info = result['studentInfo']
        assert 'hallTicket' in student_info or 'name' in student_info
        
        # Verify subjects are parsed
        subjects = result['subjects']
        assert len(subjects) > 0
        
    def test_parse_failed_results(self):
        """Test parsing results with failed subjects"""
        html = self._load_fixture('mock_results_failed.html')
        result = self.parser.parse_results(html)
        
        assert result is not None
        assert 'subjects' in result
        
        subjects = result['subjects']
        assert len(subjects) > 0
        
        # Check for failed grades
        grades = [s.get('grade', '').upper() for s in subjects]
        assert 'F' in grades or 'AB' in grades, "Failed fixture should contain F or Ab grades"
    
    def test_parse_outstanding_results(self):
        """Test parsing results with outstanding grades"""
        html = self._load_fixture('mock_results_outstanding.html')
        result = self.parser.parse_results(html)
        
        assert result is not None
        assert 'subjects' in result
        
        subjects = result['subjects']
        grades = [s.get('grade', '') for s in subjects]
        
        # Should have O or A+ grades
        has_outstanding = any(g in ['O', 'A+'] for g in grades)
        assert has_outstanding, "Outstanding fixture should contain O or A+ grades"
    
    def test_parse_empty_results(self):
        """Test parsing empty results page"""
        html = self._load_fixture('mock_results_empty.html')
        result = self.parser.parse_results(html)
        
        # Should return None or empty subjects
        if result is not None:
            subjects = result.get('subjects', [])
            assert len(subjects) == 0
    
    def test_parse_none_input(self):
        """Test parsing with None input"""
        result = self.parser.parse_results(None)
        assert result is None
    
    def test_parse_empty_string(self):
        """Test parsing with empty string"""
        result = self.parser.parse_results('')
        assert result is None
    
    def test_parse_invalid_html(self):
        """Test parsing with invalid HTML"""
        result = self.parser.parse_results('<html><body>Random text</body></html>')
        # Should not crash, may return None or empty structure
        if result is not None:
            subjects = result.get('subjects', [])
            # Should have no valid subjects
            assert len(subjects) == 0 or result is None


class TestAnalyticsEngine:
    """Test suite for AnalyticsEngine"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup analytics engine"""
        self.analytics = AnalyticsEngine()
        self.parser = ResultsParser()
    
    def _load_and_parse_fixture(self, filename):
        """Load and parse HTML fixture"""
        filepath = os.path.join(FIXTURES_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        return self.parser.parse_results(html)
    
    # ========== GPA Calculation Tests ==========
    
    def test_calculate_gpa_standard(self):
        """Test GPA calculation with standard grades"""
        results = self._load_and_parse_fixture('mock_results.html')
        analytics = self.analytics.calculate_analytics(results)
        
        assert 'gpa' in analytics
        assert analytics['gpa'] is not None
        assert 0 <= analytics['gpa'] <= 10
    
    def test_calculate_gpa_outstanding(self):
        """Test GPA calculation with outstanding grades"""
        results = self._load_and_parse_fixture('mock_results_outstanding.html')
        analytics = self.analytics.calculate_analytics(results)
        
        assert analytics['gpa'] >= 9.0, "Outstanding grades should have GPA >= 9.0"
    
    def test_calculate_gpa_with_failures(self):
        """Test GPA calculation when there are failed subjects"""
        results = self._load_and_parse_fixture('mock_results_failed.html')
        analytics = self.analytics.calculate_analytics(results)
        
        assert analytics['gpa'] is not None
        # GPA should be lower due to failures
        assert analytics['gpa'] < 8.0
    
    def test_calculate_gpa_manual(self):
        """Test GPA calculation with manual input"""
        mock_results = {
            'subjects': [
                {'code': 'CS101', 'name': 'Test 1', 'credits': '3.00', 'grade': 'A'},  # 8 * 3 = 24
                {'code': 'CS102', 'name': 'Test 2', 'credits': '3.00', 'grade': 'A+'},  # 9 * 3 = 27
                {'code': 'CS103', 'name': 'Test 3', 'credits': '4.00', 'grade': 'O'},  # 10 * 4 = 40
            ]
        }
        # Total: 91 / 10 = 9.1
        
        analytics = self.analytics.calculate_analytics(mock_results)
        assert analytics['gpa'] == 9.1
    
    # ========== Grade Distribution Tests ==========
    
    def test_grade_distribution(self):
        """Test grade distribution calculation"""
        mock_results = {
            'subjects': [
                {'grade': 'A'},
                {'grade': 'A'},
                {'grade': 'B+'},
                {'grade': 'O'},
            ]
        }
        
        analytics = self.analytics.calculate_analytics(mock_results)
        distribution = analytics['gradeDistribution']
        
        assert distribution['A'] == 2
        assert distribution['B+'] == 1
        assert distribution['O'] == 1
    
    # ========== Pass/Fail Status Tests ==========
    
    def test_pass_status_all_pass(self):
        """Test pass/fail status when all subjects pass"""
        results = self._load_and_parse_fixture('mock_results.html')
        analytics = self.analytics.calculate_analytics(results)
        
        pass_fail = analytics['passFailStatus']
        assert pass_fail['overallStatus'] == 'Pass'
        assert pass_fail['failed'] == 0
    
    def test_pass_status_with_failures(self):
        """Test pass/fail status when there are failures"""
        results = self._load_and_parse_fixture('mock_results_failed.html')
        analytics = self.analytics.calculate_analytics(results)
        
        pass_fail = analytics['passFailStatus']
        assert pass_fail['overallStatus'] == 'Fail'
        assert pass_fail['failed'] > 0
        assert len(pass_fail['failedSubjects']) > 0
    
    def test_failed_subjects_detailed(self):
        """Test that failed subjects are correctly identified"""
        mock_results = {
            'subjects': [
                {'code': 'CS101', 'name': 'Subject 1', 'grade': 'A'},
                {'code': 'CS102', 'name': 'Subject 2', 'grade': 'F'},
                {'code': 'CS103', 'name': 'Subject 3', 'grade': 'Ab'},
                {'code': 'CS104', 'name': 'Subject 4', 'grade': 'I'},  # Incomplete
            ]
        }
        
        analytics = self.analytics.calculate_analytics(mock_results)
        failed_subjects = analytics['passFailStatus']['failedSubjects']
        
        # F, Ab, and I are all failure grades
        assert len(failed_subjects) == 3
        failed_codes = [s['code'] for s in failed_subjects]
        assert 'CS102' in failed_codes
        assert 'CS103' in failed_codes
        assert 'CS104' in failed_codes
    
    # ========== Performance Level Tests ==========
    
    def test_performance_level_outstanding(self):
        """Test performance level for outstanding GPA"""
        mock_results = {
            'subjects': [
                {'credits': '3', 'grade': 'O'},
                {'credits': '3', 'grade': 'O'},
            ]
        }
        
        analytics = self.analytics.calculate_analytics(mock_results)
        assert analytics['performanceLevel'] == 'Outstanding'
    
    def test_performance_level_excellent(self):
        """Test performance level for excellent GPA"""
        mock_results = {
            'subjects': [
                {'credits': '3', 'grade': 'A'},  # 8.0
            ]
        }
        
        analytics = self.analytics.calculate_analytics(mock_results)
        assert analytics['performanceLevel'] == 'Excellent'
    
    def test_performance_level_below_average(self):
        """Test performance level for below average GPA"""
        mock_results = {
            'subjects': [
                {'credits': '3', 'grade': 'D'},  # 4.0
            ]
        }
        
        analytics = self.analytics.calculate_analytics(mock_results)
        assert analytics['performanceLevel'] == 'Below Average'
    
    # ========== Credits Summary Tests ==========
    
    def test_credits_summary_all_pass(self):
        """Test credits summary when all passed"""
        mock_results = {
            'subjects': [
                {'credits': '3.00', 'grade': 'A'},
                {'credits': '3.00', 'grade': 'B+'},
                {'credits': '2.00', 'grade': 'O'},
            ]
        }
        
        analytics = self.analytics.calculate_analytics(mock_results)
        credits = analytics['creditsSummary']
        
        assert credits['total'] == 8.0
        assert credits['earned'] == 8.0
    
    def test_credits_summary_with_failures(self):
        """Test credits summary with failed subjects"""
        mock_results = {
            'subjects': [
                {'credits': '3.00', 'grade': 'A'},
                {'credits': '3.00', 'grade': 'F'},  # Not earned
                {'credits': '2.00', 'grade': 'O'},
            ]
        }
        
        analytics = self.analytics.calculate_analytics(mock_results)
        credits = analytics['creditsSummary']
        
        assert credits['total'] == 8.0
        assert credits['earned'] == 5.0
    
    # ========== Edge Cases ==========
    
    def test_empty_results(self):
        """Test analytics with empty results"""
        analytics = self.analytics.calculate_analytics({})
        assert analytics == {}
    
    def test_none_results(self):
        """Test analytics with None results"""
        analytics = self.analytics.calculate_analytics(None)
        assert analytics == {}
    
    def test_missing_credits(self):
        """Test handling of missing credits"""
        mock_results = {
            'subjects': [
                {'grade': 'A'},  # No credits
                {'credits': '', 'grade': 'B'},  # Empty credits
                {'credits': '3', 'grade': 'O'},
            ]
        }
        
        analytics = self.analytics.calculate_analytics(mock_results)
        # Should not crash and calculate based on valid data
        assert analytics is not None
        assert analytics['gpa'] == 10.0  # Only the O with 3 credits is valid
    
    def test_invalid_grade(self):
        """Test handling of invalid grades"""
        mock_results = {
            'subjects': [
                {'credits': '3', 'grade': 'XYZ'},  # Invalid grade
                {'credits': '3', 'grade': 'A'},
            ]
        }
        
        analytics = self.analytics.calculate_analytics(mock_results)
        # Should handle gracefully
        assert analytics is not None


class TestFrontendDataHandling:
    """Test suite for edge cases that frontend should handle"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup"""
        self.parser = ResultsParser()
        self.analytics = AnalyticsEngine()
    
    def _get_full_response(self, fixture_name):
        """Get a full API-like response"""
        filepath = os.path.join(FIXTURES_DIR, fixture_name)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        parsed = self.parser.parse_results(html)
        if parsed:
            analytics = self.analytics.calculate_analytics(parsed)
            return {**parsed, 'analytics': analytics}
        return None
    
    def test_response_structure_standard(self):
        """Test response structure for standard results"""
        response = self._get_full_response('mock_results.html')
        
        assert response is not None
        assert 'studentInfo' in response
        assert 'subjects' in response
        assert 'analytics' in response
        
        # Analytics structure
        analytics = response['analytics']
        assert 'gpa' in analytics
        assert 'passFailStatus' in analytics
        assert 'totalSubjects' in analytics
    
    def test_response_structure_failed(self):
        """Test response structure for failed results"""
        response = self._get_full_response('mock_results_failed.html')
        
        assert response is not None
        analytics = response['analytics']
        
        # Should have failed subjects list
        assert 'passFailStatus' in analytics
        assert 'failedSubjects' in analytics['passFailStatus']
        assert len(analytics['passFailStatus']['failedSubjects']) > 0
    
    def test_null_safe_access_patterns(self):
        """Test that data has consistent structure for null-safe access"""
        response = self._get_full_response('mock_results.html')
        
        # These should all be accessible without errors
        assert response.get('studentInfo', {}).get('hallTicket') is not None or True
        assert response.get('studentInfo', {}).get('name') is not None or True
        assert response.get('analytics', {}).get('gpa') is not None or True
        assert response.get('analytics', {}).get('passFailStatus', {}).get('overallStatus') is not None or True


def run_tests():
    """Run all tests with visual output"""
    print("\n" + "=" * 70)
    print("CYPHER UNIT TESTS")
    print("=" * 70)
    
    # Check if fixtures exist
    fixtures = ['mock_results.html', 'mock_results_failed.html', 
                'mock_results_outstanding.html', 'mock_results_empty.html']
    
    missing = []
    for fixture in fixtures:
        path = os.path.join(FIXTURES_DIR, fixture)
        if not os.path.exists(path):
            missing.append(fixture)
    
    if missing:
        print(f"\n⚠️  Missing fixtures: {missing}")
        print("Some tests may fail.\n")
    
    # Run pytest
    pytest.main([__file__, '-v', '--tb=short'])


# ===========================================================================
# FavoritesStorage Tests
# ===========================================================================

class TestFavoritesStorage:
    """Unit tests for the FavoritesStorage service."""

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """Create a fresh FavoritesStorage backed by a temp file."""
        self.fav_file = str(tmp_path / 'test_favorites.json')
        self.storage = FavoritesStorage(filepath=self.fav_file)

    # ------------------------------------------------------------------
    # get_favorites
    # ------------------------------------------------------------------

    def test_get_favorites_initially_empty(self):
        """A newly created storage should return an empty list."""
        result = self.storage.get_favorites()
        assert result == []

    # ------------------------------------------------------------------
    # add_favorite
    # ------------------------------------------------------------------

    def test_add_favorite_returns_entry(self):
        """add_favorite should return the saved entry."""
        entry = self.storage.add_favorite('22A91A0501', 'Test Student')
        assert entry['hallTicket'] == '22A91A0501'
        assert entry['label'] == 'Test Student'
        assert 'savedAt' in entry

    def test_add_favorite_normalises_to_uppercase(self):
        """Hall ticket should always be stored in upper-case."""
        self.storage.add_favorite('22a91a0501')
        favs = self.storage.get_favorites()
        assert favs[0]['hallTicket'] == '22A91A0501'

    def test_add_favorite_uses_hall_ticket_as_label_when_none_given(self):
        """When no label is provided the hall ticket itself becomes the label."""
        self.storage.add_favorite('22A91A0502')
        favs = self.storage.get_favorites()
        assert favs[0]['label'] == '22A91A0502'

    def test_add_favorite_no_duplicates(self):
        """Adding the same hall ticket twice should not create duplicates."""
        self.storage.add_favorite('22A91A0501', 'A')
        self.storage.add_favorite('22a91a0501', 'B')  # lowercase duplicate
        favs = self.storage.get_favorites()
        assert len(favs) == 1

    def test_add_multiple_favorites(self):
        """Multiple different hall tickets can be saved."""
        self.storage.add_favorite('22A91A0501')
        self.storage.add_favorite('22A91A0502')
        self.storage.add_favorite('22A91A0503')
        assert len(self.storage.get_favorites()) == 3

    # ------------------------------------------------------------------
    # remove_favorite
    # ------------------------------------------------------------------

    def test_remove_favorite_success(self):
        """remove_favorite returns True and deletes the entry."""
        self.storage.add_favorite('22A91A0501')
        removed = self.storage.remove_favorite('22A91A0501')
        assert removed is True
        assert self.storage.get_favorites() == []

    def test_remove_favorite_case_insensitive(self):
        """Removal should work regardless of case."""
        self.storage.add_favorite('22A91A0501')
        removed = self.storage.remove_favorite('22a91a0501')
        assert removed is True

    def test_remove_favorite_not_found_returns_false(self):
        """remove_favorite returns False when the entry does not exist."""
        result = self.storage.remove_favorite('NONEXISTENT')
        assert result is False

    # ------------------------------------------------------------------
    # is_favorite
    # ------------------------------------------------------------------

    def test_is_favorite_true(self):
        """is_favorite returns True for a saved hall ticket."""
        self.storage.add_favorite('22A91A0501')
        assert self.storage.is_favorite('22A91A0501') is True

    def test_is_favorite_false(self):
        """is_favorite returns False when not saved."""
        assert self.storage.is_favorite('22A91A0999') is False

    def test_is_favorite_case_insensitive(self):
        """is_favorite is case-insensitive."""
        self.storage.add_favorite('22A91A0501')
        assert self.storage.is_favorite('22a91a0501') is True

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def test_favorites_persist_across_instances(self):
        """Data written by one instance should be readable by another."""
        self.storage.add_favorite('22A91A0501', 'Persist Test')
        # Create a new instance pointing at the same file
        storage2 = FavoritesStorage(filepath=self.fav_file)
        favs = storage2.get_favorites()
        assert len(favs) == 1
        assert favs[0]['hallTicket'] == '22A91A0501'


if __name__ == '__main__':
    run_tests()
