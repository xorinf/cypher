"""
Cypher Backend - Flask Application
Main API server for CampX results retrieval and analysis
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os

# Ensure backend directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from core.config import Config
from core.logger import setup_logger
from services.scraper import CampXScraper
from services.parser import ResultsParser
from services.analytics import AnalyticsEngine
from services.exporter import ResultsExporter

# Initialize logger
logger = setup_logger('api')

def create_app():
    """Application factory"""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for frontend communication
    
    # Initialize components
    # We initialize them here to ensure they pick up environment config at runtime
    scraper = CampXScraper()
    parser = ResultsParser()
    analytics = AnalyticsEngine()
    exporter = ResultsExporter()
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        logger.info("Health check requested")
        return jsonify({
            'status': 'healthy', 
            'service': 'Cypher API',
            'version': '1.0.1'
        })

    @app.route('/api/fetch-results', methods=['POST'])
    def fetch_results():
        """Fetch results from CampX"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Invalid JSON body'}), 400
                
            hall_ticket = data.get('hallTicket')
            exam_type = data.get('examType', '')
            view_type = data.get('viewType', 'All Semesters')
            
            if not hall_ticket:
                logger.warning("Fetch request missing hall ticket")
                return jsonify({'error': 'Hall ticket number is required'}), 400
            
            logger.info(f"Fetching results for {hall_ticket}")
            
            # Scrape
            html_content = scraper.fetch_results(hall_ticket, exam_type, view_type)
            if not html_content:
                return jsonify({'error': 'Failed to retrieve results. Please check hall ticket.'}), 404
            
            # Parse
            results_data = parser.parse_results(html_content)
            if not results_data:
                return jsonify({'error': 'Unable to parse results from response.'}), 404
            
            # Analyze
            analytics_data = analytics.calculate_analytics(results_data)
            
            # Response
            response = {
                **results_data,
                'analytics': analytics_data
            }
            
            return jsonify(response), 200
            
        except Exception as e:
            logger.error(f"API Error: {str(e)}")
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    @app.route('/api/export', methods=['POST'])
    def export_results():
        """Export results to CSV or Excel"""
        try:
            data = request.get_json()
            results_data = data.get('data')
            export_format = data.get('format', 'csv')
            
            if not results_data:
                return jsonify({'error': 'No data provided'}), 400
            
            logger.info(f"Export requested for format: {export_format}")
            
            file_path = exporter.export(results_data, export_format)
            
            if not file_path or not os.path.exists(file_path):
                return jsonify({'error': 'Failed to generate export file'}), 500
            
            return send_file(
                file_path,
                as_attachment=True,
                download_name=os.path.basename(file_path)
            )
            
        except Exception as e:
            logger.error(f"Export Error: {str(e)}")
            return jsonify({'error': f'Export failed: {str(e)}'}), 500
            
    return app

if __name__ == '__main__':
    # Validate config on startup
    try:
        Config.validate()
        app = create_app()
        logger.info(f"Starting Cypher API on port {Config.FLASK_PORT}")
        app.run(
            debug=Config.FLASK_DEBUG, 
            port=Config.FLASK_PORT, 
            host='0.0.0.0'
        )
    except Exception as e:
        logger.critical(f"Failed to start application: {str(e)}")
        sys.exit(1)
