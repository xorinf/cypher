"""
Cypher Analytics Engine
Computes GPA, trends, and summarizes performance data.
"""

from typing import List, Dict, Optional
import logging

logger = logging.getLogger('api')

class AnalyticsEngine:
    """Engine for processing parsed results and generating insights"""
    
    GRADE_POINTS = {
        'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'P': 4,
        'F': 0, 'AB': 0, 'I': 0, 'MALPRACTICE': 0
    }

    def calculate_analytics(self, results_data: Dict) -> Dict:
        """
        Main entry point for calculating student analytics.
        Uses API summary if available, otherwise calculates manually.
        """
        subjects = results_data.get('subjects', [])
        semester_info = results_data.get('semesterInfo', {})
        summary = results_data.get('summary', {})
        
        # Calculate Percentage (Use summary or calculate manual)
        marks_summary = summary.get('marks', {})
        if not marks_summary or marks_summary.get('total', 0) == 0:
            marks_summary = self._calculate_marks_summary(subjects)
            if 'marks' not in summary: summary['marks'] = {}
            summary['marks'].update(marks_summary)
             
        percentage = 0.0
        if marks_summary.get('total', 0) > 0:
            obtained = marks_summary.get('obtained', 0)
            total = marks_summary.get('total', 0)
            percentage = round((obtained / total) * 100, 2)
        
        analytics = {
            'totalSubjects': len(subjects),
            'gpa': self._calculate_gpa(subjects),
            'gradeDistribution': self._grade_distribution(subjects),
            'passFailStatus': self._pass_fail_status(subjects, summary.get('backlogs')),
            'creditsSummary': self._credits_summary(subjects, summary.get('credits')),
            'performanceLevel': None,
            'trends': self._calculate_trends(semester_info),
            'overallPercentage': percentage,
            'rawSummary': summary
        }
        
        # Determine performance level
        if analytics['gpa']:
            analytics['performanceLevel'] = self._get_performance_level(analytics['gpa'])
            
        return analytics

    def _calculate_gpa(self, subjects: List[Dict]) -> Optional[float]:
        """Calculate Cumulative GPA (CGPA)"""
        total_points = 0
        total_credits = 0
        
        for sub in subjects:
            grade = sub.get('grade', '').upper()
            credits_str = sub.get('credits', '0')
            
            try:
                credits = float(credits_str) if credits_str else 0
            except (ValueError, TypeError):
                credits = 0
                
            if grade in self.GRADE_POINTS:
                points = self.GRADE_POINTS[grade]
                total_points += (points * credits)
                total_credits += credits
        
        if total_credits == 0:
            return None
            
        return round(total_points / total_credits, 2)

    def _grade_distribution(self, subjects: List[Dict]) -> Dict:
        """Count occurrences of each grade"""
        distribution = {}
        for sub in subjects:
            grade = sub.get('grade', 'N/A')
            distribution[grade] = distribution.get(grade, 0) + 1
        return distribution
    
    def _pass_fail_status(self, subjects: List[Dict], backlog_summary: Dict = None) -> Dict:
        """Determine pass/fail status with soft wording"""
        failed_subjects = []
        passed = 0
        failed = 0
        
        # Manual count for subject list
        for subject in subjects:
            status = subject.get('status', {})
            is_passed = status.get('passed')
            grade = subject.get('grade', '').upper()
            
            if is_passed is None:
                is_failed = grade in ['F', 'AB', 'I', 'ABSENT', 'MALPRACTICE']
            else:
                is_failed = not is_passed
                
            if is_failed:
                failed += 1
                failed_subjects.append({
                    'name': subject.get('name', 'Unknown Subject'),
                    'code': subject.get('code', ''),
                    'grade': grade,
                    'semester': subject.get('semester')
                })
            else:
                passed += 1
        
        # Use official backlog count if available
        official_failed_count = backlog_summary.get('due', failed) if backlog_summary else failed
        
        return {
            'passed': passed,
            'failed': official_failed_count,
            'failedSubjects': failed_subjects,
            'overallStatus': 'All Clear' if official_failed_count == 0 else f'{official_failed_count} Active Backlog(s)'
        }
    
    def _credits_summary(self, subjects: List[Dict], credits_summary_data: Dict = None) -> Dict:
        """Calculate total credits or use official summary"""
        if credits_summary_data:
            return {
                'total': credits_summary_data.get('total', 0),
                'earned': credits_summary_data.get('obtained', 0)
            }

        total_credits = 0
        earned_credits = 0
        for sub in subjects:
            credits_str = sub.get('credits', '0')
            try:
                credits = float(credits_str) if credits_str else 0
            except:
                credits = 0
            total_credits += credits
            if sub.get('status', {}).get('passed'):
                earned_credits += credits
        
        return {
            'total': round(total_credits, 1),
            'earned': round(earned_credits, 1)
        }

    def _calculate_trends(self, semester_info: Dict) -> Dict:
        """Calculate SGPA per semester (Manual fallback if missing)"""
        semesters = semester_info.get('semesters', [])
        labels = []
        data = []
        
        for sem in semesters:
            sem_num = sem.get('semester')
            sgpa = sem.get('sgpa')
            
            # If API SGPA is missing/zero, calculate from subjects
            if not sgpa or sgpa == 0 or sgpa == '0':
                subjects = sem.get('subjects', [])
                total_points = 0
                total_credits = 0
                for sub in subjects:
                    points = sub.get('gradePoints')
                    credits = float(sub.get('credits', 0) or 0)
                    if points is not None:
                        total_points += float(points) * credits
                        total_credits += credits
                    else:
                        grade = sub.get('grade', '').upper()
                        if grade in self.GRADE_POINTS:
                            total_points += self.GRADE_POINTS[grade] * credits
                            total_credits += credits
                if total_credits > 0:
                    sgpa = round(total_points / total_credits, 2)
                    sem['sgpa'] = sgpa
            
            if sem_num and sgpa is not None:
                try:
                    val = float(sgpa)
                    labels.append(f"Sem {sem_num}")
                    data.append(val)
                except: continue
                
        return {'labels': labels, 'data': data}

    def _get_performance_level(self, gpa: float) -> str:
        if gpa >= 9.0: return 'Outstanding'
        elif gpa >= 8.0: return 'Excellent'
        elif gpa >= 7.0: return 'Very Good'
        elif gpa >= 6.0: return 'Good'
        elif gpa >= 5.0: return 'Average'
        else: return 'Needs Improvement'

    def _calculate_marks_summary(self, subjects: List[Dict]) -> Dict:
        total_obtained = 0
        total_max = 0
        for sub in subjects:
            max_marks = sub.get('maxMarks', {})
            int_max = float(max_marks.get('internal') or 0)
            ext_max = float(max_marks.get('external') or 0)
            marks_str = str(sub.get('marks', ''))
            try:
                obtained = float(marks_str) if marks_str.replace('.', '').isdigit() else 0
            except: obtained = 0
            subject_total = int_max + ext_max
            if subject_total > 0:
                total_max += subject_total
                total_obtained += obtained
        return {'obtained': int(total_obtained), 'total': int(total_max)}
