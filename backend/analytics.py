"""
Analytics Engine
Calculates GPA, grades, and performance metrics
"""

import statistics
from typing import Dict, List


class AnalyticsEngine:
    """Analyzes academic results and generates insights"""
    
    # Grade to grade point mapping (standard 10-point scale)
    GRADE_POINTS = {
        'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6,
        'C': 5, 'D': 4, 'F': 0, 'Ab': 0, 'I': 0
    }
    
    def calculate_analytics(self, results_data: Dict) -> Dict:
        """
        Calculate comprehensive analytics from results
        
        Args:
            results_data: Parsed results containing subjects and grades
            
        Returns:
            Dictionary with analytics including GPA, grade distribution, etc.
        """
        if not results_data or 'subjects' not in results_data:
            return {}
        
        subjects = results_data.get('subjects', [])
        
        analytics = {
            'totalSubjects': len(subjects),
            'gpa': self._calculate_gpa(subjects),
            'gradeDistribution': self._grade_distribution(subjects),
            'passFailStatus': self._pass_fail_status(subjects),
            'creditsSummary': self._credits_summary(subjects),
            'performanceLevel': None
        }
        
        # Determine performance level
        if analytics['gpa']:
            analytics['performanceLevel'] = self._get_performance_level(analytics['gpa'])
        
        return analytics
    
    def _calculate_gpa(self, subjects: List[Dict]) -> float:
        """Calculate GPA based on grades and credits"""
        total_grade_points = 0
        total_credits = 0
        
        for subject in subjects:
            grade = subject.get('grade', '').upper()
            credits_str = subject.get('credits', '0')
            
            try:
                credits = float(credits_str) if credits_str else 0
            except (ValueError, TypeError):
                credits = 0
            
            if grade in self.GRADE_POINTS and credits > 0:
                grade_point = self.GRADE_POINTS[grade]
                total_grade_points += grade_point * credits
                total_credits += credits
        
        if total_credits == 0:
            return 0.0
        
        gpa = total_grade_points / total_credits
        return round(gpa, 2)
    
    def _grade_distribution(self, subjects: List[Dict]) -> Dict:
        """Calculate distribution of grades"""
        distribution = {}
        
        for subject in subjects:
            grade = subject.get('grade', 'N/A').upper()
            distribution[grade] = distribution.get(grade, 0) + 1
        
        return distribution
    
    def _pass_fail_status(self, subjects: List[Dict]) -> Dict:
        """Determine pass/fail status"""
        failed_subjects = []
        passed = 0
        failed = 0
        
        for subject in subjects:
            grade = subject.get('grade', '').upper()
            subject_name = subject.get('name', 'Unknown Subject')
            
            if grade in ['F', 'Ab', 'I']:
                failed += 1
                failed_subjects.append({
                    'name': subject_name,
                    'code': subject.get('code', ''),
                    'grade': grade
                })
            elif grade in self.GRADE_POINTS:
                passed += 1
        
        return {
            'passed': passed,
            'failed': failed,
            'failedSubjects': failed_subjects,
            'overallStatus': 'Pass' if failed == 0 else 'Fail'
        }
    
    def _credits_summary(self, subjects: List[Dict]) -> Dict:
        """Calculate total credits"""
        total_credits = 0
        earned_credits = 0
        
        for subject in subjects:
            grade = subject.get('grade', '').upper()
            credits_str = subject.get('credits', '0')
            
            try:
                credits = float(credits_str) if credits_str else 0
            except (ValueError, TypeError):
                credits = 0
            
            total_credits += credits
            
            # Credits earned only if not failed
            if grade not in ['F', 'Ab', 'I']:
                earned_credits += credits
        
        return {
            'total': round(total_credits, 1),
            'earned': round(earned_credits, 1)
        }
    
    def _get_performance_level(self, gpa: float) -> str:
        """Classify performance based on GPA"""
        if gpa >= 9.0:
            return 'Outstanding'
        elif gpa >= 8.0:
            return 'Excellent'
        elif gpa >= 7.0:
            return 'Very Good'
        elif gpa >= 6.0:
            return 'Good'
        elif gpa >= 5.0:
            return 'Average'
        else:
            return 'Below Average'
