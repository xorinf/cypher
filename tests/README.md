# Tests Directory

This directory contains the comprehensive test suite for the Cypher application.

## 📁 Structure

```
tests/
├── __init__.py
├── unit/              # Unit tests for individual components
│   ├── test_validators.py
│   └── test_scraper.py
├── integration/       # End-to-end integration tests
│   └── test_real_results.py
├── benchmarks/        # Performance comparison tests
│   └── benchmark_scrapers.py (Removed/Legacy)
└── README.md          # This file
```

## 🚀 Running Tests

All tests should be run from the **project root directory**.

### 1. Unit Tests (Fast & Safe)
Runs all logic tests for validators and scraper configuration.
```bash
python -m pytest tests/unit/ -v
```

### 2. Integration Test (Real World)
Connects to the university portal, fetches results using the API, and generates an HTML report.
**Requires `.env` configuration.**
```bash
python tests/integration/test_real_results.py
```

**Output:**
- `generated/results_report.html` - Visual report of the results.
- `generated/real_results.json` - Raw parsed data.

## ⚙️ Configuration

To run integration tests, you must configure the `.env` file in the project root:

```env
# URL of the results portal (for Referer header)
CAMPX_BASE_URL=https://your-university-portal.edu/results

# API URL
CAMPX_API_URL=https://api.your-university-middleware.com/student-results/external

# Valid Hall Ticket Number for testing
EX_HTN=YOUR_HALLTICKET_NUMBER
```

## 📝 Best Practices

- Always run unit tests before pushing changes.
- Do not commit real student data (Hall Tickets) to the repository.
- Use `EX_HTN` in `.env` for local testing.
