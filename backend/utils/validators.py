"""
Validation utilities for Cypher
"""

import re
from typing import Optional


def validate_hall_ticket(hall_ticket: str) -> tuple[bool, Optional[str]]:
    """
    Validate hall ticket format
    
    Args:
        hall_ticket: Hall ticket number to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not hall_ticket:
        return False, "Hall ticket cannot be empty"
    
    if not isinstance(hall_ticket, str):
        return False, "Hall ticket must be a string"
    
    hall_ticket = hall_ticket.strip()
    
    if len(hall_ticket) < 5:
        return False, "Hall ticket must be at least 5 characters"
    
    if len(hall_ticket) > 20:
        return False, "Hall ticket cannot exceed 20 characters"
    
    # Basic alphanumeric check
    if not re.match(r'^[A-Za-z0-9]+$', hall_ticket):
        return False, "Hall ticket must contain only letters and numbers"
    
    return True, None


def validate_exam_type(exam_type: str) -> tuple[bool, Optional[str]]:
    """
    Validate exam type
    
    Args:
        exam_type: Exam type to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_types = ['general', 'regular', 'honors', 'minors', 'supplementary']
    
    if not exam_type:
        return True, None  # Optional parameter
    
    if exam_type.lower() not in valid_types:
        return False, f"Exam type must be one of: {', '.join(valid_types)}"
    
    return True, None


def validate_view_type(view_type: str) -> tuple[bool, Optional[str]]:
    """
    Validate view type
    
    Args:
        view_type: View type to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_types = ['all semesters', 'single semester', 'current semester']
    
    if not view_type:
        return True, None  # Optional parameter
    
    if view_type.lower() not in valid_types:
        return False, f"View type must be one of: {', '.join(valid_types)}"
    
    return True, None


def sanitize_input(text: str, max_length: int = 100) -> str:
    """
    Sanitize user input by removing dangerous characters
    
    Args:
        text: Text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove any potentially dangerous characters
    sanitized = re.sub(r'[<>\"\';&|`$()]', '', text)
    
    # Trim to max length
    sanitized = sanitized[:max_length]
    
    return sanitized.strip()
