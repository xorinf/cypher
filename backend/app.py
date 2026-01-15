"""
Cypher Backend - Flask Application
Main API server for CampX results retrieval and analysis
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import os
from scraper import CampXScraper
from parser import ResultsParser
from analytics import AnalyticsEngine
from exporter import ResultsExporter

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize components
scraper = CampXScraper()
parser = ResultsParser()
analytics = AnalyticsEngine()
exporter = ResultsExporter()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Cypher API'})


@app.route('/api/fetch-results', methods=['POST'])
def fetch_results():
    """
    Fetch results from CampX
    Expected JSON body:
    {
        "hallTicket": "string",
        "examType": "string",
        "viewType": "string"
    }
    """
    try:
        data = request.get_json()
        hall_ticket = data.get('hallTicket')
        exam_type = data.get('examType', '')
        view_type = data.get('viewType', 'All Semesters')
        
        if not hall_ticket:
            return jsonify({'error': 'Hall ticket number is required'}), 400
        
        # Scrape results from CampX
        html_content = scraper.fetch_results(hall_ticket, exam_type, view_type)
        
        if not html_content:
            return jsonify({'error': 'Failed to retrieve results. Please check hall ticket and try again.'}), 404
        
        # Parse the HTML to extract data
        results_data = parser.parse_results(html_content)
        
        if not results_data:
            return jsonify({'error': 'No results found or unable to parse results.'}), 404
        
        # Generate analytics
        analytics_data = analytics.calculate_analytics(results_data)
        
        # Combine results with analytics
        response = {
            **results_data,
            'analytics': analytics_data
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/export', methods=['POST'])
def export_results():
    """
    Export results to CSV or Excel
    Expected JSON body:
    {
        "data": {...},
        "format": "csv" or "excel"
    }
    """
    try:
        data = request.get_json()
        results_data = data.get('data')
        export_format = data.get('format', 'csv')
        
        if not results_data:
            return jsonify({'error': 'No data provided for export'}), 400
        
        # Generate export file
        file_path = exporter.export(results_data, export_format)
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Failed to generate export file'}), 500
        
        # Send file to client
        return send_file(
            file_path,
            as_attachment=True,
            download_name=os.path.basename(file_path)
        )
        
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(debug=debug, port=port, host='0.0.0.0')
