"""
Unit tests for validators
"""

import pytest
from backend.utils.validators import (
    validate_hall_ticket,
    validate_exam_type,
    validate_view_type,
    sanitize_input
)


class TestValidateHallTicket:
    
    def test_valid_hall_ticket(self):
        """Test validation of valid hall ticket"""
        is_valid, error = validate_hall_ticket("ABC12345XY")
        assert is_valid is True
        assert error is None
    
    def test_empty_hall_ticket(self):
        """Test validation of empty hall ticket"""
        is_valid, error = validate_hall_ticket("")
        assert is_valid is False
        assert "cannot be empty" in error
    
    def test_short_hall_ticket(self):
        """Test validation of too short hall ticket"""
        is_valid, error = validate_hall_ticket("123")
        assert is_valid is False
        assert "at least 5 characters" in error
    
    def test_long_hall_ticket(self):
        """Test validation of too long hall ticket"""
        is_valid, error = validate_hall_ticket("A" * 25)
        assert is_valid is False
        assert "cannot exceed 20 characters" in error
    
    def test_invalid_characters(self):
        """Test validation with invalid characters"""
        is_valid, error = validate_hall_ticket("22EG-107B45")
        assert is_valid is False
        assert "letters and numbers" in error


class TestValidateExamType:
    
    def test_valid_exam_type(self):
        """Test validation of valid exam types"""
        valid_types = ['general', 'regular', 'honors', 'minors']
        for exam_type in valid_types:
            is_valid, error = validate_exam_type(exam_type)
            assert is_valid is True
            assert error is None
    
    def test_empty_exam_type(self):
        """Test validation of empty exam type (optional)"""
        is_valid, error = validate_exam_type("")
        assert is_valid is True
    
    def test_invalid_exam_type(self):
        """Test validation of invalid exam type"""
        is_valid, error = validate_exam_type("invalid")
        assert is_valid is False
        assert "must be one of" in error


class TestSanitizeInput:
    
    def test_sanitize_dangerous_characters(self):
        """Test removal of dangerous characters"""
        input_text = "test<script>alert('xss')</script>"
        sanitized = sanitize_input(input_text)
        assert "<" not in sanitized
        assert ">" not in sanitized
        assert "script" in sanitized  # Text remains but tags removed
    
    def test_sanitize_max_length(self):
        """Test maximum length enforcement"""
        input_text = "A" * 200
        sanitized = sanitize_input(input_text, max_length=50)
        assert len(sanitized) == 50
    
    def test_sanitize_empty_input(self):
        """Test sanitization of empty input"""
        sanitized = sanitize_input("")
        assert sanitized == ""
