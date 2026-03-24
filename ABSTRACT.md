# Abstract

## Project Title

Cypher: A High-Performance University Results Scraping and Analysis System

## Overview

Cypher is an open-source web application designed to retrieve, parse, and analyze student academic results from university portals that use the CampX platform. The system replaces slow, fragile browser automation approaches with direct API communication, delivering a significant performance improvement while offering a structured analytics layer and a modern browser-based interface for end users.

The project is built for educational purposes and is intended for use only against portals for which the user has authorized access.

## Motivation

University result portals typically expose their data through web interfaces that are difficult to programmatically interact with. Students and academic staff who want to perform bulk lookups, trend analysis, or export data for further processing face repetitive manual work or are forced to rely on brittle browser automation tools. Cypher addresses this by identifying and calling the underlying REST API endpoints directly, eliminating the overhead of browser rendering and achieving retrieval times that are orders of magnitude faster than browser-driven approaches.

## System Architecture

The system follows a three-tier, service-oriented architecture:

- **Frontend**: A single-page web application built with HTML5, CSS3, and vanilla JavaScript (ES6+). It communicates with the backend over HTTP and renders results dynamically using Chart.js for performance visualizations.

- **Backend**: A Python 3.8+ Flask application exposing a REST API. The backend is organized into a core configuration and logging layer, a business services layer, and an input validation utility layer.

- **External Integration**: The backend communicates directly with the CampX university portal API using the Requests library, passing required HTTP headers such as institution code and tenant identifier.

The backend is organized around four discrete service classes, each with a single responsibility:

- **CampXScraper**: Handles all outbound HTTP communication with the university portal API, manages authentication headers, applies request timeouts, and returns raw JSON responses.
- **ResultsParser**: Transforms the raw API JSON into structured Python data models, extracting student identity information, per-semester result records, subject-level details (codes, credits, grades, marks, pass/fail status), and exam metadata.
- **AnalyticsEngine**: Consumes the structured result data and produces derived metrics including cumulative GPA, semester-wise GPA trends, grade distribution counts, earned versus attempted credit summaries, pass/fail subject lists, overall percentage, and a qualitative performance classification.
- **ResultsExporter**: Serializes the parsed and analyzed data to CSV or multi-sheet Excel files with timestamped filenames, creating the export directory if it does not already exist.

## Key Features

- Direct REST API integration with the CampX university portal, bypassing browser automation
- Modular Flask backend with clearly separated concerns across scraping, parsing, analytics, and export layers
- Comprehensive academic analytics: CGPA, SGPA trends, grade distribution, credit summaries, and performance level classification
- Export to CSV and multi-sheet Excel (student information, summary statistics, subject records, grade distribution)
- Input validation and sanitization for all user-supplied values (hall ticket format, exam type, view type)
- Environment-variable-driven configuration with no hardcoded credentials
- Responsive single-page frontend with dynamic result rendering and Chart.js trend visualization
- Gunicorn-based production deployment configuration
- CI/CD pipeline via GitHub Actions with GitHub Pages deployment for the static frontend
- Render.com deployment descriptor for cloud hosting of the backend service
- Comprehensive test suite covering unit-level component tests and end-to-end integration tests

## Technology Stack

| Layer | Technology |
|---|---|
| Backend language | Python 3.8+ |
| Web framework | Flask 3.0 |
| HTTP client | Requests 2.31 |
| Data processing | Pandas 2.2, OpenPyXL 3.1 |
| CORS handling | Flask-CORS 4.0 |
| Environment management | python-dotenv 1.0 |
| Production server | Gunicorn 21.2 |
| Frontend markup | HTML5 |
| Frontend styling | CSS3 |
| Frontend scripting | Vanilla JavaScript ES6+ |
| Chart rendering | Chart.js |
| Testing framework | pytest 7.0+ |
| Deployment platform | Render.com, GitHub Pages |
| CI/CD | GitHub Actions |

## Data Flow

1. The user enters a student hall ticket number in the web interface and submits the form.
2. The frontend sends a POST request to the `/api/fetch-results` backend endpoint.
3. The backend validates and sanitizes all input fields.
4. `CampXScraper` issues an authenticated HTTP request to the CampX API and returns the JSON payload.
5. `ResultsParser` extracts structured student and subject records from the payload.
6. `AnalyticsEngine` computes performance metrics from the structured records.
7. The combined data is returned to the frontend as a JSON response.
8. The frontend renders the student summary, subject table, and GPA trend chart.
9. Optionally, the user may request a CSV or Excel export, which the backend generates and returns as a downloadable file.

## Security Considerations

All user-supplied input is validated against expected formats (alphanumeric hall ticket numbers of 5 to 20 characters, enumerated exam types, enumerated view types) and sanitized to remove shell-injectable and HTML-injectable characters before any processing occurs. Application credentials and portal URLs are stored exclusively in environment variables and are never committed to version control. The `.env.example` file documents the required variable names without including real values. Error responses log sufficient detail for debugging while avoiding the exposure of internal configuration or stack traces to the client.

## Performance

Direct API integration removes the overhead associated with browser instantiation, page rendering, and DOM traversal. Benchmarks documented in the project indicate retrieval times approximately 67 times faster than equivalent browser-automation approaches.

## Project Status

Cypher is a functional, documented, and tested educational project. It includes a setup script for local development, a contributing guide covering coding standards and pull request workflow, and full API documentation. The codebase consists of approximately 1,500 lines of backend Python and 600 lines of frontend code across HTML, CSS, and JavaScript.

## Disclaimer

This project is intended solely for educational purposes. It must only be used to access university portals for which the user has explicit authorization. The authors do not condone unauthorized access to computer systems.
