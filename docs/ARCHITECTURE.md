# Cypher Architecture

## Overview
Cypher is a university results scraping and analysis system built with Flask backend and modern frontend.

## System Architecture

```
┌─────────────┐
│   Frontend  │
│  (React/JS) │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────────────────────────┐
│      Flask API Server          │
│  (backend/app.py)              │
└────────┬────────────────────────┘
         │
         ├──► Core Services
         │    ├── Config Management
         │    └── Logger
         │
         ├──► Business Services
         │    ├── Scraper (API)
         │    ├── Legacy Scraper (Selenium)
         │    ├── Parser (HTML/JSON)
         │    ├── Analytics Engine
         │    └── Exporter (CSV/Excel)
         │
         └──► External APIs
              ├── University Portal (Web)
              └── University API (REST)
```

## Directory Structure

### Backend (`backend/`)
- **app.py**: Flask application entry point, API routes
- **core/**: Core utilities and configuration
  - `config.py`: Environment-based configuration
  - `logger.py`: Centralized logging
- **services/**: Business logic layer
  - `scraper.py`: Direct API scraper (primary)
  - `legacy_scraper.py`: Selenium browser automation (fallback)
  - `parser.py`: HTML/JSON parsing logic
  - `analytics.py`: GPA calculation, performance analysis
  - `exporter.py`: CSV/Excel export functionality
- **utils/**: Helper utilities
  - `validators.py`: Input validation and sanitization

### Tests (`tests/`)
- **unit/**: Unit tests for individual components
- **integration/**: End-to-end integration tests
- **benchmarks/**: Performance comparison tests
- **fixtures/**: Test data and mocks

### Frontend (`frontend/`)
- Modern web interface for results display

### Generated (`generated/`)
- Output files from tests and exports
- `*.html`, `*.json`,`*.csv`, `*.xlsx`

## Data Flow

### Primary Flow (API Method)
```
User Request
    ↓
API Endpoint (/api/fetch-results)
    ↓
CampXScraper (HTTP Request)
    ↓
External API (JSON Response)
    ↓
ResultsParser.parse_api_response()
    ↓
AnalyticsEngine.calculate_analytics()
    ↓
JSON Response → User
```

### Fallback Flow (Selenium Method)
```
User Request
    ↓
API Endpoint
    ↓
LegacyCampXScraper (Browser Automation)
    ↓
Web Portal (HTML Response)
    ↓
ResultsParser.parse_results()
    ↓
AnalyticsEngine
    ↓
JSON Response → User
```

## Key Design Decisions

### 1. Dual Scraping Strategy
- **Primary**: Direct API calls (63x faster)
- **Fallback**: Selenium automation (for UI-only portals)
- Both methods maintained for reliability

### 2. Environment-Based Configuration
All sensitive data in `.env`:
- URLs (CAMPX_BASE_URL, CAMPX_API_URL)
- Credentials (CAMPX_INSTITUTION_CODE, CAMPX_TENANT_ID)
- Test data (EX_HTN)

### 3. Modular Service Layer
- Each service handles one responsibility
- Easy to test, modify, replace
- Clear interfaces between components

### 4. Parser Flexibility
- Handles both HTML (from Selenium) and JSON (from API)
- Unified output format for consistency
- Easy to add new parsing methods

## Security Considerations

1. **Input Validation**: All user inputs validated and sanitized
2. **No Hardcoded Secrets**: All credentials from environment
3. **Error Handling**: Detailed logging without exposing sensitive data
4. **CORS**: Configured for frontend communication

## Performance

| Component | Performance | Notes |
|-----------|-------------|-------|
| API Scraper | ~0.15s | Direct HTTP, no browser overhead |
| Selenium Scraper | ~9.66s | Full browser automation |
| Parser | <0.01s | Fast HTML/JSON parsing |
| Analytics | <0.01s | In-memory calculations |
| Export | 0.1-0.5s | Depends on data size |

## Scalability

### Current Capacity
- Single-threaded Flask app
- Handles ~100 requests/minute
- Suitable for small to medium institutions

### Scaling Options
1. **Horizontal**: Deploy multiple Flask instances behind load balancer
2. ** Caching**: Redis for frequently accessed results
3. **Async**: Convert to async/await for higher throughput
4. **Queue**: Celery for background result processing

## Error Handling

1. **Network Errors**: Retry with exponential backoff
2. **Parsing Errors**: Log and return partial data if possible
3. **API Errors**: Fall back to Selenium method
4. **Validation Errors**: Clear user-facing messages

## Testing Strategy

- **Unit Tests**: Test each service in isolation
- **Integration Tests**: Test full API-to-database flow
- **Benchmarks**: Compare performance of different approaches
- **Fixtures**: Reusable test data for consistency

## Future Enhancements

1. User authentication and authorization
2. Result caching and history
3. Batch processing for multiple students
4. Real-time notifications
5. Mobile app integration
