"""
Integration test to verify real results fetching from university portal
Uses the EX_HTN from .env file
Generates a formatted HTML report
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(project_root, '.env'))

from backend.services.scraper import CampXScraper
from backend.services.parser import ResultsParser
from backend.services.analytics import AnalyticsEngine


def generate_html_report(full_response, output_path):
    """Generate a formatted HTML report from the results data"""
    
    student_info = full_response.get('studentInfo', {})
    subjects = full_response.get('subjects', [])
    analytics = full_response.get('analytics', {})
    semester_info = full_response.get('semesterInfo', {})
    pass_fail = analytics.get('passFailStatus', {})
    
    # Determine status color
    status = pass_fail.get('overallStatus', 'Unknown')
    status_color = '#10b981' if status == 'Pass' else '#ef4444'
    
    # Build subjects table rows
    subject_rows = ''
    for i, sub in enumerate(subjects, 1):
        grade = sub.get('grade', 'N/A')
        grade_color = '#10b981' if grade not in ['F', 'Ab', 'I'] else '#ef4444'
        subject_rows += f'''
            <tr>
                <td style="text-align: center;">{i}</td>
                <td style="text-align: center;">{sub.get('code', 'N/A')}</td>
                <td>{sub.get('name', 'N/A')}</td>
                <td style="text-align: center;">{sub.get('credits', 'N/A')}</td>
                <td style="text-align: center;"><span style="color: {grade_color}; font-weight: bold;">{grade}</span></td>
            </tr>'''
    
    # Build failed subjects list
    failed_list = ''
    failed_subs = pass_fail.get('failedSubjects', [])
    if failed_subs:
        failed_list = '<h4 style="color: #ef4444; margin-top: 24px;">⚠️ Failed Subjects</h4><ul>'
        for sub in failed_subs:
            failed_list += f'<li><strong>{sub.get("code", "N/A")}</strong> - {sub.get("name", "Unknown")} (Grade: {sub.get("grade", "F")})</li>'
        failed_list += '</ul>'
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Results Report - {student_info.get('hallTicket', 'Unknown')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0e17 0%, #1a1825 100%);
            color: #ffffff;
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 2.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #a7a9be;
            font-size: 0.9rem;
        }}
        .card {{
            background: #242135;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.05);
        }}
        .card h3 {{
            color: #667eea;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }}
        .info-item label {{
            color: #a7a9be;
            font-size: 0.85rem;
            display: block;
            margin-bottom: 4px;
        }}
        .info-item span {{
            font-size: 1.1rem;
            font-weight: 600;
        }}
        .summary-card {{
            text-align: center;
            padding: 32px;
        }}
        .summary-card .gpa {{
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .summary-card .status {{
            font-size: 1.5rem;
            font-weight: 700;
            margin-top: 10px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-top: 24px;
        }}
        .stat-item {{
            text-align: center;
            padding: 16px;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 12px;
        }}
        .stat-item .value {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #667eea;
        }}
        .stat-item .label {{
            color: #a7a9be;
            font-size: 0.8rem;
            margin-top: 4px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }}
        th, td {{
            padding: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        th {{
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.5px;
        }}
        tr:hover {{
            background: rgba(255,255,255,0.02);
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #6e7191;
            font-size: 0.85rem;
        }}
        @media print {{
            body {{ background: white; color: black; }}
            .card {{ border: 1px solid #ddd; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Exam Results Report</h1>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <!-- Student Information -->
        <div class="card">
            <h3>👤 Student Information</h3>
            <div class="info-grid">
                <div class="info-item">
                    <label>Hall Ticket Number</label>
                    <span>{student_info.get('hallTicket', 'N/A')}</span>
                </div>
                <div class="info-item">
                    <label>Student Name</label>
                    <span>{student_info.get('name', 'N/A')}</span>
                </div>
                <div class="info-item">
                    <label>Program</label>
                    <span>{student_info.get('program', 'N/A')}</span>
                </div>
                <div class="info-item">
                    <label>Semester</label>
                    <span>{semester_info.get('semester', 'N/A')}</span>
                </div>
            </div>
        </div>
        
        <!-- Performance Summary -->
        <div class="card summary-card">
            <div class="gpa">{analytics.get('gpa', 'N/A')}</div>
            <div>Grade Point Average</div>
            <div class="status" style="color: {status_color};">
                {status} - {analytics.get('performanceLevel', 'N/A')}
            </div>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="value">{analytics.get('totalSubjects', 0)}</div>
                    <div class="label">Total Subjects</div>
                </div>
                <div class="stat-item">
                    <div class="value" style="color: #10b981;">{pass_fail.get('passed', 0)}</div>
                    <div class="label">Passed</div>
                </div>
                <div class="stat-item">
                    <div class="value" style="color: #ef4444;">{pass_fail.get('failed', 0)}</div>
                    <div class="label">Failed</div>
                </div>
            </div>
            {failed_list}
        </div>
        
        <!-- Subjects Table -->
        <div class="card">
            <h3>📚 Subject-wise Results</h3>
            <table>
                <thead>
                    <tr>
                        <th>S.No</th>
                        <th>Course Code</th>
                        <th>Course Name</th>
                        <th>Credits</th>
                        <th>Grade</th>
                    </tr>
                </thead>
                <tbody>
                    {subject_rows}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Generated by Cypher - University Results Analyzer</p>
        </div>
    </div>
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_path


def test_real_results():
    """Test fetching real results from the university portal"""
    
    # Get hall ticket from environment
    hall_ticket = os.getenv('EX_HTN')
    
    if not hall_ticket:
        print("❌ EX_HTN not found in .env file!")
        return False
    
    print("\n" + "=" * 70)
    print("REAL RESULTS INTEGRATION TEST")
    print("=" * 70)
    print(f"Hall Ticket: {hall_ticket}")
    print(f"Base URL: {os.getenv('CAMPX_BASE_URL')}")
    print("=" * 70 + "\n")
    
    # Initialize components
    scraper = CampXScraper()
    parser = ResultsParser()
    analytics = AnalyticsEngine()
    
    # Step 1: Fetch results
    print("Step 1: Fetching results from university portal...")
    print("-" * 50)
    
    try:
        api_data = scraper.fetch_results(
            hall_ticket=hall_ticket,
            exam_type='Regular',
            view_type='All Semesters'
        )
    except Exception as e:
        print(f"❌ Scraper error: {str(e)}")
        return False
    
    if not api_data:
        print("❌ Failed to fetch results - no data returned")
        return False
    
    print(f"✅ Fetched API data")
    
    # Save to generated folder
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'generated')
    os.makedirs(output_dir, exist_ok=True)
    
    raw_json_file = os.path.join(output_dir, 'real_results_raw.json')
    with open(raw_json_file, 'w', encoding='utf-8') as f:
        json.dump(api_data, f, indent=2)
    
    # Step 2: Parse the results
    print("\nStep 2: Parsing API data...")
    print("-" * 50)
    
    parsed_data = parser.parse_api_response(api_data)
    
    if not parsed_data:
        print("❌ Failed to parse results")
        return False
    
    print("✅ Successfully parsed results!")
    
    # Step 3: Generate analytics
    print("\nStep 3: Generating analytics...")
    print("-" * 50)
    
    analytics_data = analytics.calculate_analytics(parsed_data)
    
    # Combine results
    full_response = {
        **parsed_data,
        'analytics': analytics_data
    }
    
    # Save parsed data as JSON
    json_file = os.path.join(output_dir, 'real_results.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(full_response, f, indent=2)
    print(f"✅ Saved parsed data to {json_file}")
    
    # Step 4: Generate HTML Report
    print("\nStep 4: Generating HTML report...")
    print("-" * 50)
    
    report_path = os.path.join(output_dir, 'results_report.html')
    generate_html_report(full_response, report_path)
    print(f"✅ Generated HTML report: {report_path}")
    
    # Display summary
    student_info = parsed_data.get('studentInfo', {})
    subjects = parsed_data.get('subjects', [])
    pass_fail = analytics_data.get('passFailStatus', {})
    
    print("\n" + "=" * 70)
    print("✅ Test Results:")
    print("=" * 70)
    print(f"• Hall Ticket: {student_info.get('hallTicket', hall_ticket)}")
    print(f"• Name: {student_info.get('name', 'N/A')}")
    print(f"• Program: {student_info.get('program', 'N/A')}")
    print(f"• Total Subjects: {analytics_data.get('totalSubjects', 0)}")
    print(f"• GPA: {analytics_data.get('gpa', 'N/A')}")
    print(f"• Performance Level: {analytics_data.get('performanceLevel', 'N/A')}")
    print(f"• Status: {pass_fail.get('overallStatus', 'N/A')} ({pass_fail.get('failed', 0)} subject(s) failed)")
    print(f"• Passed: {pass_fail.get('passed', 0)} subjects")
    
    if pass_fail.get('failedSubjects'):
        print(f"\n⚠️  Failed Subjects:")
        for sub in pass_fail['failedSubjects']:
            print(f"   - {sub.get('code', 'N/A')}: {sub.get('name', 'Unknown')}")
    
    print("\n📚 Subjects:")
    for i, sub in enumerate(subjects, 1):
        grade = sub.get('grade', 'N/A')
        status_icon = '✅' if grade not in ['F', 'Ab', 'I'] else '❌'
        print(f"   {i}. {sub.get('code', 'N/A')} - {sub.get('name', 'N/A')} ({sub.get('credits', 'N/A')} cr) - {grade} {status_icon}")
    
    print("\n" + "=" * 70)
    print(f"📄 HTML Report: file://{os.path.abspath(report_path)}")
    print("=" * 70 + "\n")
    
    return True


if __name__ == '__main__':
    success = test_real_results()
    sys.exit(0 if success else 1)
