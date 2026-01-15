# Cypher - Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2026-01-15

### Fixed
- **Python 3.13 Compatibility**: Updated dependencies for Python 3.13 support
  - Updated `pandas` from 2.1.4 to `>=2.2.0`
  - Updated `lxml` from 4.9.3 to `>=5.0.0`
  - Fixed compilation errors with older package versions

### Changed
- **Port Configuration**: Changed default Flask port from 5000 to 5001
  - Avoids conflict with macOS AirPlay Receiver
  - Updated `.env` configuration
  - Updated frontend API base URL in `app.js`

### Verified
- Backend server running successfully on port 5001
- Frontend interface loads correctly
- API health check endpoint responding
- All dependencies installed without errors

## [1.0.0] - 2026-01-15

### Added
- **Initial Release**: Complete Cypher application
- **Backend**: Python Flask API with REST endpoints
  - Web scraper using Selenium for CampX automation
  - HTML parser with BeautifulSoup for data extraction
  - Analytics engine for GPA and performance calculations
  - Data exporter supporting CSV and Excel formats
- **Frontend**: Premium dark-themed UI
  - Glassmorphism design with gradient accents
  - Responsive form for hall ticket input
  - Dynamic results rendering
  - Export functionality for CSV/Excel downloads
- **Documentation**: Comprehensive README with setup instructions
- **Setup Script**: Automated environment setup via `setup.sh`
- **Configuration**: Environment variables via `.env` file
- **Disclaimer**: Added compliance notice for educational use

### Features
- Automated result retrieval from CampX system
- Real-time GPA calculation
- Grade distribution analysis
- Pass/fail status tracking
- Subject-wise performance breakdown
- Multi-format export (CSV/Excel)
- Error handling and validation
