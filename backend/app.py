"""
Cypher Backend - Flask Application
Main API server for CampX results retrieval and analysis
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import csv
import io
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
from services.storage import FavoritesStorage

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
    favorites_storage = FavoritesStorage()
    
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
            
            # Import and use validators
            from utils.validators import validate_hall_ticket, validate_exam_type, sanitize_input
            
            # Sanitize inputs
            hall_ticket = sanitize_input(hall_ticket, max_length=20)
            
            # Validate inputs
            is_valid, error_msg = validate_hall_ticket(hall_ticket)
            if not is_valid:
                logger.warning(f"Invalid hall ticket: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            if exam_type:
                is_valid, error_msg = validate_exam_type(exam_type)
                if not is_valid:
                    logger.warning(f"Invalid exam type: {error_msg}")
                    return jsonify({'error': error_msg}), 400
            
            logger.info(f"Fetching results for {hall_ticket}")
            
            # Scrape
            api_data = scraper.fetch_results(hall_ticket, exam_type, view_type)
            if not api_data:
                return jsonify({'error': 'Failed to retrieve results. Please check hall ticket.'}), 404
            
            # Parse
            results_data = parser.parse_api_response(api_data)
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
            
    @app.route('/api/batch-fetch', methods=['POST'])
    def batch_fetch():
        """
        Fetch results for multiple roll numbers at once.

        Accepts either:
        - JSON body: { "rollNumbers": ["HT001", "HT002", ...], "examType": "" }
        - Multipart form with a CSV file upload (field name: "file")
          The CSV may be a single column of hall tickets or have a header row.
        """
        from utils.validators import validate_hall_ticket, validate_exam_type, sanitize_input

        roll_numbers = []
        exam_type = ''

        content_type = request.content_type or ''
        if 'multipart/form-data' in content_type:
            # CSV file upload
            uploaded_file = request.files.get('file')
            if not uploaded_file:
                return jsonify({'error': 'No file provided'}), 400

            exam_type = request.form.get('examType', '')
            stream = io.TextIOWrapper(uploaded_file.stream, encoding='utf-8-sig')
            reader = csv.reader(stream)
            for row in reader:
                if not row:
                    continue
                # Accept the first non-empty column value
                value = row[0].strip().upper()
                if value and not value.lower().startswith('hall') and not value.lower().startswith('roll'):
                    roll_numbers.append(value)
        else:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Invalid request body'}), 400
            roll_numbers = [str(r).strip().upper() for r in data.get('rollNumbers', []) if r]
            exam_type = data.get('examType', '')

        if not roll_numbers:
            return jsonify({'error': 'No roll numbers provided'}), 400

        if len(roll_numbers) > 50:
            return jsonify({'error': 'Maximum 50 roll numbers per batch request'}), 400

        if exam_type:
            is_valid, error_msg = validate_exam_type(exam_type)
            if not is_valid:
                return jsonify({'error': error_msg}), 400

        results = []
        errors = []

        for ht in roll_numbers:
            ht = sanitize_input(ht, max_length=20)
            is_valid, error_msg = validate_hall_ticket(ht)
            if not is_valid:
                errors.append({'hallTicket': ht, 'error': error_msg})
                continue

            try:
                logger.info(f"Batch fetching: {ht}")
                api_data = scraper.fetch_results(ht, exam_type)
                if not api_data:
                    errors.append({'hallTicket': ht, 'error': 'Result not found'})
                    continue

                parsed = parser.parse_api_response(api_data)
                if not parsed:
                    errors.append({'hallTicket': ht, 'error': 'Unable to parse results'})
                    continue

                analytics_data = analytics.calculate_analytics(parsed)
                results.append({**parsed, 'analytics': analytics_data})

            except Exception as exc:
                logger.error(f"Batch error for {ht}: {exc}")
                errors.append({'hallTicket': ht, 'error': str(exc)})

        # Identify top performer by CGPA
        top_performer = None
        if results:
            top_performer = max(
                results,
                key=lambda r: r.get('analytics', {}).get('gpa') or 0
            ).get('studentInfo', {}).get('hallTicket')

        return jsonify({
            'results': results,
            'errors': errors,
            'topPerformer': top_performer,
            'summary': {
                'requested': len(roll_numbers),
                'succeeded': len(results),
                'failed': len(errors),
            }
        }), 200

    # ------------------------------------------------------------------
    # Favorites endpoints
    # ------------------------------------------------------------------

    @app.route('/api/favorites', methods=['GET'])
    def get_favorites():
        """Return all saved favorite hall tickets."""
        return jsonify({'favorites': favorites_storage.get_favorites()}), 200

    @app.route('/api/favorites', methods=['POST'])
    def add_favorite():
        """Add a hall ticket to favorites."""
        from utils.validators import validate_hall_ticket, sanitize_input

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON body'}), 400

        hall_ticket = sanitize_input(data.get('hallTicket', ''), max_length=20)
        label = sanitize_input(data.get('label', ''), max_length=60)

        is_valid, error_msg = validate_hall_ticket(hall_ticket)
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        entry = favorites_storage.add_favorite(hall_ticket, label)
        return jsonify({'favorite': entry}), 200

    @app.route('/api/favorites/<hall_ticket>', methods=['DELETE'])
    def remove_favorite(hall_ticket):
        """Remove a hall ticket from favorites."""
        from utils.validators import sanitize_input
        hall_ticket = sanitize_input(hall_ticket.upper(), max_length=20)
        removed = favorites_storage.remove_favorite(hall_ticket)
        if not removed:
            return jsonify({'error': 'Favorite not found'}), 404
        return jsonify({'message': f'{hall_ticket} removed from favorites'}), 200

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
