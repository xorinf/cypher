"""
Results Exporter Service
Generates CSV and Excel files from results data
"""

import os
import csv
import pandas as pd
import sys
from datetime import datetime

# Path hack
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from core.config import Config
from core.logger import setup_logger

logger = setup_logger(__name__)

class ResultsExporter:
    """Exports results data to CSV or Excel format"""
    
    def __init__(self):
        self.export_dir = Config.EXPORT_DIR
        self._ensure_export_dir()
    
    def _ensure_export_dir(self):
        """Create export directory if it doesn't exist"""
        if not os.path.exists(self.export_dir):
            try:
                os.makedirs(self.export_dir)
                logger.info(f"Created export directory: {self.export_dir}")
            except Exception as e:
                logger.error(f"Failed to create export directory: {str(e)}")
    
    def export(self, results_data: dict, format: str = 'csv') -> str:
        """Export results to specified format"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            hall_ticket = results_data.get('studentInfo', {}).get('hallTicket', 'unknown')
            
            if format.lower() == 'excel':
                filename = f"results_{hall_ticket}_{timestamp}.xlsx"
                filepath = self._export_excel(results_data, filename)
            else:
                filename = f"results_{hall_ticket}_{timestamp}.csv"
                filepath = self._export_csv(results_data, filename)
                
            logger.info(f"Exported results to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            return None
    
    def _export_csv(self, results_data: dict, filename: str) -> str:
        """Export to CSV format"""
        filepath = os.path.join(self.export_dir, filename)
        
        student_info = results_data.get('studentInfo', {})
        subjects = results_data.get('subjects', [])
        analytics = results_data.get('analytics', {})
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write student information
            writer.writerow(['STUDENT INFORMATION'])
            writer.writerow(['Hall Ticket', student_info.get('hallTicket', 'N/A')])
            writer.writerow(['Name', student_info.get('name', 'N/A')])
            writer.writerow(['Program', student_info.get('program', 'N/A')])
            writer.writerow([])
            
            # Write analytics summary
            writer.writerow(['PERFORMANCE SUMMARY'])
            writer.writerow(['GPA', analytics.get('gpa', 'N/A')])
            writer.writerow(['Performance Level', analytics.get('performanceLevel', 'N/A')])
            writer.writerow(['Total Subjects', analytics.get('totalSubjects', 0)])
            
            pass_fail = analytics.get('passFailStatus', {})
            writer.writerow(['Passed Subjects', pass_fail.get('passed', 0)])
            writer.writerow(['Failed Subjects', pass_fail.get('failed', 0)])
            writer.writerow(['Overall Status', pass_fail.get('overallStatus', 'N/A')])
            writer.writerow([])
            
            # Write subject details
            writer.writerow(['SUBJECT-WISE RESULTS'])
            if subjects:
                # Header
                headers = ['Subject Code', 'Subject Name', 'Credits', 'Grade', 'Marks']
                writer.writerow(headers)
                
                # Subjects
                for subject in subjects:
                    writer.writerow([
                        subject.get('code', ''),
                        subject.get('name', ''),
                        subject.get('credits', ''),
                        subject.get('grade', ''),
                        subject.get('marks', '')
                    ])
        
        return filepath
    
    def _export_excel(self, results_data: dict, filename: str) -> str:
        """Export to Excel format with multiple sheets"""
        filepath = os.path.join(self.export_dir, filename)
        
        student_info = results_data.get('studentInfo', {})
        subjects = results_data.get('subjects', [])
        analytics = results_data.get('analytics', {})
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Sheet 1: Student Information
            student_df = pd.DataFrame([
                {'Field': 'Hall Ticket', 'Value': student_info.get('hallTicket', 'N/A')},
                {'Field': 'Name', 'Value': student_info.get('name', 'N/A')},
                {'Field': 'Program', 'Value': student_info.get('program', 'N/A')},
            ])
            student_df.to_excel(writer, sheet_name='Student Info', index=False)
            
            # Sheet 2: Performance Summary
            pass_fail = analytics.get('passFailStatus', {})
            summary_df = pd.DataFrame([
                {'Metric': 'GPA', 'Value': analytics.get('gpa', 'N/A')},
                {'Metric': 'Performance Level', 'Value': analytics.get('performanceLevel', 'N/A')},
                {'Metric': 'Total Subjects', 'Value': analytics.get('totalSubjects', 0)},
                {'Metric': 'Passed Subjects', 'Value': pass_fail.get('passed', 0)},
                {'Metric': 'Failed Subjects', 'Value': pass_fail.get('failed', 0)},
                {'Metric': 'Overall Status', 'Value': pass_fail.get('overallStatus', 'N/A')},
            ])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Sheet 3: Subject Details
            if subjects:
                subjects_df = pd.DataFrame(subjects)
                # Reorder columns for better readability
                column_order = ['code', 'name', 'credits', 'grade', 'marks']
                columns = [col for col in column_order if col in subjects_df.columns]
                subjects_df = subjects_df[columns]
                subjects_df.to_excel(writer, sheet_name='Subjects', index=False)
            
            # Sheet 4: Grade Distribution
            grade_dist = analytics.get('gradeDistribution', {})
            if grade_dist:
                dist_df = pd.DataFrame([
                    {'Grade': grade, 'Count': count}
                    for grade, count in sorted(grade_dist.items())
                ])
                dist_df.to_excel(writer, sheet_name='Grade Distribution', index=False)
        
        return filepath
