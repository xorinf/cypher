import json
import os
import sys

# Path hack for sibling imports if run directly
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from core.logger import setup_logger

logger = setup_logger(__name__)

class ResultsParser:
    """Parser for extracting student results from API response"""

    def parse_api_response(self, api_data):
        """
        Parse JSON response from CampX API
        """
        if not api_data:
            logger.warning("Received empty API data")
            return None
            
        try:
            # 1. Student Info
            student = api_data.get('student', {})
            program = api_data.get('program', {})
            student_info = {
                'hallTicket': student.get('rollNo'),
                'name': student.get('fullName'),
                'photo': student.get('photo'),
                'batch': student.get('batch'),
                'program': program.get('branchDisplay') or program.get('branchName')
            }
            
            # 2. Results (Grouped by Semester)
            # We will return list of semesters, each with summary and subjects
            results_list = api_data.get('results', [])
            semesters_data = []
            
            # Also keep a flat list for analytics compatibility if needed, 
            # but ideally analytics should handle structure. 
            # Let's provide both or ensure analytics can handle it.
            # For now, let's keep 'subjects' flat list for backward compat with current analytics,
            # and add 'semesters' for UI.
            all_subjects = []
            
            for sem in results_list:
                sem_no = sem.get('semNo')
                sem_subjects = []
                
                for sub_res in sem.get('subjectsResults', []):
                    sub = sub_res.get('subject', {})
                    grade_info = sub_res.get('consideredGrade', {})
                    
                    code = sub.get('subjectCode')
                    if not code: continue
                    
                    subject_entry = {
                        'code': code,
                        'name': sub.get('name'),
                        'credits': grade_info.get('credits'),
                        'grade': grade_info.get('grade'),
                        'gradePoints': grade_info.get('gradePoints'),
                        'marks': sub.get('total'), # Extract Total Marks for calculation
                        'examMonth': grade_info.get('monthYear'), # New Field
                        'type': sub.get('subjectTypeId'), 
                        'status': {
                            'passed': grade_info.get('passed', False),
                            'absent': grade_info.get('isAbsent', False),
                            'malpractice': grade_info.get('isMalPracticed', False)
                        },
                        'maxMarks': {
                            'internal': sub.get('intMax'),
                            'external': sub.get('extMax')
                        },
                        'semester': sem_no
                    }
                    sem_subjects.append(subject_entry)
                    all_subjects.append(subject_entry)
                
                semesters_data.append({
                    'semester': sem_no,
                    'sgpa': sem.get('sgpa'),
                    'subjects': sem_subjects
                })
            
            # 3. Summary Block (Richer data)
            summary = api_data.get('summary', {})
            
            # 4. Overall Info
            cgpa = api_data.get('cgpa')
            
            semester_info = {
                'cgpa': cgpa if cgpa else 0.0,
                'semesters': sorted(semesters_data, key=lambda x: x['semester'] or 0)
            }
            
            return {
                'studentInfo': student_info,
                'subjects': all_subjects, # Flattened for analytics
                'semesterInfo': semester_info, # Structured for UI
                'summary': {
                    'marks': summary.get('marksObtained', {}),
                    'credits': summary.get('creditsObtained', {}),
                    'backlogs': summary.get('subjectDue', {})
                }
            }
            
        except Exception as e:
            logger.error(f"Error parsing API data: {str(e)}")
            return None

