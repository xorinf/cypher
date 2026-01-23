import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.parser import ResultsParser
from backend.services.analytics import AnalyticsEngine

def verify_sample(file_path):
    print(f"Verifying {file_path}...")
    try:
        with open(file_path, 'r') as f:
            raw_data = json.load(f)
        
        # 1. Test Parsing
        parser = ResultsParser()
        parsed = parser.parse_api_response(raw_data)
        
        if not parsed:
            print("❌ Parsing failed (returned None)")
            return False
            
        student = parsed.get('studentInfo', {})
        print(f"   ✓ Student: {student.get('name')} ({student.get('hallTicket')})")
        print(f"   ✓ Photo URL: {student.get('photo')}")
        print(f"   ✓ Batch: {student.get('batch')}")
        
        sem_info = parsed.get('semesterInfo', {})
        semesters = sem_info.get('semesters', [])
        print(f"   ✓ Semesters Found: {len(semesters)}")
        
        if semesters:
            print(f"   ✓ First Sem SGPA: {semesters[0].get('sgpa')}")
            
        # 2. Test Analytics
        analytics_engine = AnalyticsEngine()
        analytics = analytics_engine.calculate_analytics(parsed)
        
        trends = analytics.get('trends', {})
        print(f"   ✓ Trends Data Points: {len(trends.get('data', []))}")
        
        passed_status = analytics.get('passFailStatus', {})
        print(f"   ✓ Overall Status: {passed_status.get('overallStatus')}")
        
        print("✅ Validation Successful!\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    base_path = "tests/generated/"
    samples = ["sample1.json", "sample2.json", "sample4.json"]
    
    success = True
    for s in samples:
        path = os.path.join(base_path, s)
        if os.path.exists(path):
            if not verify_sample(path):
                success = False
        else:
            print(f"⚠️ File not found: {path}")
            
    if success:
        print("All samples verified successfully.")
        sys.exit(0)
    else:
        sys.exit(1)
