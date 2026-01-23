"""
HTML Parser for CampX Results
Extracts structured data from the results page HTML
"""

from bs4 import BeautifulSoup
import re
import sys
import os
import json

# Path hack for sibling imports if run directly
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from core.logger import setup_logger

logger = setup_logger(__name__)

class ResultsParser:
    """Parser for extracting student results from HTML"""
    
    def parse_results(self, html_content):
        """
        Parse HTML content to extract student data
        """
        if not html_content:
            logger.warning("Received empty HTML content")
            return None
        
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Extract student information
            student_info = self._extract_student_info(soup)
            
            # Extract subject-wise results
            subjects = self._extract_subjects(soup)
            
            # Extract semester/overall information
            semester_info = self._extract_semester_info(soup)
            
            if not student_info and not subjects:
                logger.warning("Parsed empty student info and subjects")
                return None
            
            logger.info(f"Successfully parsed results for student: {student_info.get('hallTicket', 'Unknown')}")
            
            return {
                'studentInfo': student_info,
                'subjects': subjects,
                'semesterInfo': semester_info
            }
            
        except Exception as e:
            logger.error(f"Error parsing results: {str(e)}")
            return None

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
                'program': program.get('branchDisplay') or program.get('branchName')
            }
            
            # 2. Subjects (Flatten all semesters)
            subjects = []
            results = api_data.get('results', [])
            
            for sem in results:
                # sem_no = sem.get('semNo')
                for sub_res in sem.get('subjectsResults', []):
                    sub = sub_res.get('subject', {})
                    grade_info = sub_res.get('consideredGrade', {})
                    
                    code = sub.get('subjectCode')
                    if not code: continue
                    
                    # Determine Internal/External marks if available or just use total?
                    # The HTML parser extracted 'marks' column if present. 
                    # The API has 'intMax', 'extMax' but maybe not actual marks in 'consideredGrade' except grade points?
                    # consideredGrade has: "grade": "F", "gradePoints": 0, "credits": "0.00"
                    
                    subjects.append({
                        'code': code,
                        'name': sub.get('name'),
                        'credits': grade_info.get('credits'),
                        'grade': grade_info.get('grade'),
                        'marks': '' # API might not expose raw marks in this endpoint, only grade
                    })
            
            # 3. Semester/Overall Info
            # API summary has 'creditsObtained', 'marksObtained'.
            # We need GPA. The API has 'cgpa' in 'student' (null in example) and 'sgpa' per sem.
            # We can calculate CGPA if it's missing or use what's available.
            # HTML parser extracted GPA from text.
            
            cgpa = api_data.get('cgpa')
            if cgpa is None:
                # Try to find overall GPA or just leave blank
                pass
                
            semester_info = {
                'gpa': cgpa if cgpa else 0.0, # Placeholder
                'semester': None 
            }
            
            # If we have results, maybe we can calculate GPA? 
            # Or just use the summary data.
            # For now, let's keep it simple.
            
            return {
                'studentInfo': student_info,
                'subjects': subjects,
                'semesterInfo': semester_info
            }
            
        except Exception as e:
            logger.error(f"Error parsing API data: {str(e)}")
            return None
    
    def _extract_student_info(self, soup):
        """Extract basic student information"""
        info = {}
        try:
            # Find all h6 elements (MUI labels)
            h6_elements = soup.find_all('h6')
            
            for h6 in h6_elements:
                label_text = h6.get_text(strip=True).lower()
                next_p = h6.find_next_sibling('p')
                
                if next_p:
                    value = next_p.get_text(strip=True)
                    if any(x in label_text for x in ['hallticket', 'roll', 'student id']):
                        info['hallTicket'] = value
                    elif 'student name' in label_text or label_text == 'name':
                        info['name'] = value
                    elif any(x in label_text for x in ['program', 'course', 'branch']):
                        info['program'] = value
            
            # Fallback
            if not info.get('hallTicket'):
                hall_ticket_elem = soup.find(string=re.compile(r'Hall Ticket|Roll No|Student ID', re.I))
                if hall_ticket_elem:
                    parent = hall_ticket_elem.find_parent()
                    if parent:
                        next_elem = parent.find_next_sibling()
                        if next_elem:
                            info['hallTicket'] = next_elem.get_text(strip=True)
                            
        except Exception as e:
            logger.error(f"Error extracting student info: {str(e)}")
        
        return info
    
    def _extract_subjects(self, soup):
        """Extract subject-wise grades and marks"""
        subjects = []
        
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            header_indices = {}
            headers_found = False
            
            # 1. Find Header
            for row in rows:
                cells = row.find_all(['th', 'td'])
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                header_text_lower = ' '.join(cell_texts).lower()
                
                if any(k in header_text_lower for k in ['subject', 'course', 'code', 'grade']):
                    # Check individual columns
                    for i, h in enumerate(cell_texts):
                        h_lower = h.lower()
                        if 'code' in h_lower: header_indices['code'] = i
                        elif 'name' in h_lower or 'subject' in h_lower: header_indices['name'] = i
                        elif 'grade' in h_lower: header_indices['grade'] = i
                        elif 'credit' in h_lower: header_indices['credits'] = i
                        elif 'mark' in h_lower: header_indices['marks'] = i
                    headers_found = True
                    continue # Start processing data rows
                
                # 2. Process Data Rows
                if headers_found and len(cells) > 0:
                    subject_data = {}
                    # Helper to safe get
                    def get_cell(key):
                        idx = header_indices.get(key)
                        return cells[idx].get_text(strip=True) if idx is not None and idx < len(cells) else None

                    code = get_cell('code')
                    name = get_cell('name')
                    
                    if code or name:
                        subject_data['code'] = code
                        subject_data['name'] = name
                        subject_data['grade'] = get_cell('grade')
                        subject_data['credits'] = get_cell('credits')
                        subject_data['marks'] = get_cell('marks')
                        subjects.append(subject_data)
        
        return subjects
    
    def _extract_semester_info(self, soup):
        info = {}
        try:
            # Updated to use string= instead of text= (BS4 deprecation fixed)
            gpa_elem = soup.find(string=re.compile(r'SGPA|GPA|CGPA', re.I))
            if gpa_elem and gpa_elem.parent:
                text = gpa_elem.parent.get_text(strip=True)
                gpa_match = re.search(r'(\d+\.?\d*)', text)
                if gpa_match:
                    info['gpa'] = float(gpa_match.group(1))
            
            sem_elem = soup.find(string=re.compile(r'Semester|Sem', re.I))
            if sem_elem and sem_elem.parent:
                text = sem_elem.parent.get_text(strip=True)
                sem_match = re.search(r'(\d+)', text)
                if sem_match:
                    info['semester'] = int(sem_match.group(1))
        except Exception as e:
            logger.error(f"Error extracting semester info: {str(e)}")
        
        return info
