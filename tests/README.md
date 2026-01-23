# Tests Directory

This directory contains the comprehensive test suite for the Cypher application.

## 📁 Structure

```
tests/
├── __init__.py
├── test_units.py          # Unit tests for Parser, Analytics, and API structures
├── test_scraper.py        # Scraper service tests (Mock & Real modes)
├── test_real_results.py   # Full integration test with HTML reporting
├── fixtures/              # Mock data for testing without network
│   ├── mock_results.html
│   ├── mock_results_failed.html
│   └── mock_results.json
└── README.md              # This file
```

## 🚀 Running Tests

All tests should be run from the **project root directory**.

### 1. Unit Tests (Fast & Safe)
Runs all logic tests for parsing and analytics using mock data.
```bash
python -m pytest tests/test_units.py -v
```

### 2. Scraper Tests (Interactive)
Tests the scraping service specifically. Can use Mock Data (fast) or Real Data (requires config).
```bash
python tests/test_scraper.py
```

### 3. Full Integration Test (Real World)
Connects to the university portal, fetches results, and generates an HTML report.
**Requires `.env` configuration.**
```bash
python tests/test_real_results.py
```

**Output:**
- `generated/results_report.html` - Visual report of the results.
- `generated/real_results.json` - Raw parsed data.

## ⚙️ Configuration

To run integration tests (`test_real_results.py` or `test_scraper.py` mode 2), you must configure the `.env` file in the project root:

```env
# URL of the results portal
CAMPX_BASE_URL=https://your-university-portal.edu/results

# Valid Hall Ticket Number for testing
EX_HTN=YOUR_HALLTICKET_NUMBER
```

## 🧪 Mock Data

The `fixtures/` directory contains sanitized HTML files that simulate various result scenarios:
- **Standard Pass**: `mock_results.html`
- **With Failures**: `mock_results_failed.html`
- **Outstanding**: `mock_results_outstanding.html`

These are used by `test_units.py` to ensure the parser handles different grade types and pass/fail logic correctly without hitting the real server.

## 📝 Best Practices

- Always run `test_units.py` before pushing changes.
- Do not commit real student data (Hall Tickets) to the repository.
- Use `EX_HTN` in `.env` for local testing.
