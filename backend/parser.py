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
        
        # Try to extract from MUI structure (h6 label + p value)
        try:
            # Find all h6 elements (these are typically labels in MUI)
            h6_elements = soup.find_all('h6')
            
            for h6 in h6_elements:
                label_text = h6.get_text(strip=True).lower()
                
                # Find the next sibling p element which contains the value
                next_p = h6.find_next_sibling('p')
                if next_p:
                    value = next_p.get_text(strip=True)
                    
                    if 'hallticket' in label_text or 'roll' in label_text or 'student id' in label_text:
                        info['hallTicket'] = value
                    elif 'student name' in label_text or (label_text == 'name'):
                        info['name'] = value
                    elif 'program' in label_text or 'course' in label_text or 'branch' in label_text:
                        info['program'] = value
            
            # Fallback: Try old pattern with text search
            if not info.get('hallTicket'):
                hall_ticket_elem = soup.find(string=re.compile(r'Hall Ticket|Roll No|Student ID', re.I))
                if hall_ticket_elem:
                    parent = hall_ticket_elem.find_parent()
                    if parent:
                        next_elem = parent.find_next_sibling()
                        if next_elem:
                            info['hallTicket'] = next_elem.get_text(strip=True)
                            
        except Exception as e:
            print(f"Error extracting student info: {str(e)}")
        
        return info
    
    def _extract_subjects(self, soup):
        """Extract subject-wise grades and marks"""
        subjects = []
        
        # Try to find results table
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            
            # Try to identify header row
            headers = []
            header_indices = {}  # Map of field type to column index
            
            for row in rows:
                cells = row.find_all(['th', 'td'])
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                
                # Check if this looks like a header row
                header_text_lower = ' '.join(cell_texts).lower()
                if any(keyword in header_text_lower 
                       for keyword in ['subject', 'course', 'code', 'grade', 'marks', 'credits']):
                    headers = cell_texts
                    
                    # Build header index map
                    for i, h in enumerate(headers):
                        h_lower = h.lower()
                        if 'code' in h_lower:
                            header_indices['code'] = i
                        elif 'name' in h_lower or ('course' in h_lower and 'code' not in h_lower) or ('subject' in h_lower and 'code' not in h_lower):
                            header_indices['name'] = i
                        elif 'grade' in h_lower:
                            header_indices['grade'] = i
                        elif 'credit' in h_lower:
                            header_indices['credits'] = i
                        elif 'mark' in h_lower or 'score' in h_lower:
                            header_indices['marks'] = i
                    continue
                
                # If we have headers, try to parse data rows
                if headers and len(cells) > 0:
                    subject_data = {}
                    
                    # Use header indices for reliable extraction
                    if 'code' in header_indices and header_indices['code'] < len(cells):
                        subject_data['code'] = cells[header_indices['code']].get_text(strip=True)
                    if 'name' in header_indices and header_indices['name'] < len(cells):
                        subject_data['name'] = cells[header_indices['name']].get_text(strip=True)
                    if 'grade' in header_indices and header_indices['grade'] < len(cells):
                        subject_data['grade'] = cells[header_indices['grade']].get_text(strip=True)
                    if 'credits' in header_indices and header_indices['credits'] < len(cells):
                        subject_data['credits'] = cells[header_indices['credits']].get_text(strip=True)
                    if 'marks' in header_indices and header_indices['marks'] < len(cells):
                        subject_data['marks'] = cells[header_indices['marks']].get_text(strip=True)
                    
                    # Only add if we have at least code or name
                    if subject_data.get('code') or subject_data.get('name'):
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
