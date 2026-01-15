"""
HTML Parser for CampX Results
Extracts structured data from the results page HTML
"""

from bs4 import BeautifulSoup
import re


class ResultsParser:
    """Parser for extracting student results from HTML"""
    
    def parse_results(self, html_content):
        """
        Parse HTML content to extract student data
        
        Args:
            html_content (str): Raw HTML from results page
            
        Returns:
            dict: Structured results data with student info and grades
        """
        if not html_content:
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
                return None
            
            return {
                'studentInfo': student_info,
                'subjects': subjects,
                'semesterInfo': semester_info
            }
            
        except Exception as e:
            print(f"Error parsing results: {str(e)}")
            return None
    
    def _extract_student_info(self, soup):
        """Extract basic student information"""
        info = {}
        
        # This is a placeholder - actual selectors will depend on the HTML structure
        # We'll need to inspect the actual results page to get correct selectors
        
        # Try common patterns for student information
        try:
            # Look for hall ticket/roll number
            hall_ticket_elem = soup.find(text=re.compile(r'Hall Ticket|Roll No|Student ID', re.I))
            if hall_ticket_elem:
                parent = hall_ticket_elem.find_parent()
                if parent:
                    info['hallTicket'] = parent.get_text(strip=True).split(':')[-1].strip()
            
            # Look for student name
            name_elem = soup.find(text=re.compile(r'Student Name|Name', re.I))
            if name_elem:
                parent = name_elem.find_parent()
                if parent:
                    info['name'] = parent.get_text(strip=True).split(':')[-1].strip()
            
            # Look for program/course
            program_elem = soup.find(text=re.compile(r'Program|Course|Branch', re.I))
            if program_elem:
                parent = program_elem.find_parent()
                if parent:
                    info['program'] = parent.get_text(strip=True).split(':')[-1].strip()
                    
        except Exception as e:
            print(f"Error extracting student info: {str(e)}")
        
        return info
    
    def _extract_subjects(self, soup):
        """Extract subject-wise grades and marks"""
        subjects = []
        
        # Try to find results table
        # This is a placeholder - needs actual HTML structure
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            
            # Try to identify header row
            headers = []
            for row in rows:
                cells = row.find_all(['th', 'td'])
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                
                # Check if this looks like a header row
                if any(keyword in ' '.join(cell_texts).lower() 
                       for keyword in ['subject', 'code', 'grade', 'marks', 'credits']):
                    headers = cell_texts
                    continue
                
                # If we have headers, try to parse data rows
                if headers and len(cells) > 0:
                    subject_data = {}
                    for i, cell in enumerate(cells):
                        if i < len(headers):
                            header = headers[i].lower()
                            value = cell.get_text(strip=True)
                            
                            if 'subject' in header and 'code' not in header:
                                subject_data['name'] = value
                            elif 'code' in header:
                                subject_data['code'] = value
                            elif 'grade' in header:
                                subject_data['grade'] = value
                            elif 'credit' in header:
                                subject_data['credits'] = value
                            elif 'mark' in header or 'score' in header:
                                subject_data['marks'] = value
                    
                    if subject_data:
                        subjects.append(subject_data)
        
        return subjects
    
    def _extract_semester_info(self, soup):
        """Extract semester GPA and other overall information"""
        info = {}
        
        try:
            # Look for GPA/CGPA information
            gpa_elem = soup.find(text=re.compile(r'SGPA|GPA|CGPA', re.I))
            if gpa_elem:
                parent = gpa_elem.find_parent()
                if parent:
                    text = parent.get_text(strip=True)
                    # Try to extract numeric GPA value
                    gpa_match = re.search(r'(\d+\.?\d*)', text)
                    if gpa_match:
                        info['gpa'] = float(gpa_match.group(1))
            
            # Look for semester
            sem_elem = soup.find(text=re.compile(r'Semester|Sem', re.I))
            if sem_elem:
                parent = sem_elem.find_parent()
                if parent:
                    text = parent.get_text(strip=True)
                    sem_match = re.search(r'(\d+)', text)
                    if sem_match:
                        info['semester'] = int(sem_match.group(1))
                        
        except Exception as e:
            print(f"Error extracting semester info: {str(e)}")
        
        return info
