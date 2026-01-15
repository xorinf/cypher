# Tests Directory

This directory contains all test files and fixtures for the Cypher application.

## Structure

```
tests/
├── __init__.py
├── test_scraper.py       # Scraper unit tests
├── fixtures/
│   ├── __init__.py
│   ├── mock_results.html # Mock HTML results page
│   └── mock_results.json # Mock parsed JSON data
└── README.md            # This file
```

## Running Tests

### Prerequisites
- Ensure the virtual environment is activated
- Install test dependencies: `pip install pytest` (optional, for advanced testing)

### Run Scraper Tests

```bash
# From project root
source venv/bin/activate
cd backend
python ../tests/test_scraper.py
```

### Environment Setup

Before running tests, create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Then edit `.env` and set:
- `CAMPX_BASE_URL` to your university's results portal URL
- Other configuration as needed

> **Note**: You'll need a valid hallticket number to test the scraper with real data.

## Mock Data

The `fixtures/` directory contains sanitized mock data for testing without accessing real university systems:

- **mock_results.html**: Sample HTML result page with fictional student data
- **mock_results.json**: Sample parsed JSON output

These fixtures can be used to test the parser logic without running the full scraper.

## Creating Your Own Test Data

1. **For Testing Parser Only**:
   - Modify `mock_results.html` with different grades/subjects
   - Run parser tests to verify it handles various formats

2. **For Testing Full Scraper**:
   - Update `.env` with your university's URL
   - Use your own hallticket in `test_scraper.py`
   - Run the scraper test

## Security Note

⚠️ **Never commit real student data or personal information to this repository!**

- Use mock data for testing
- Keep your `.env` file private (already in `.gitignore`)
- Replace any real data with placeholders before committing

## Test Output Files

Test runs may generate output files like:
- `test_output.html`
- `test_output.json`

These are automatically ignored by `.gitignore` and should not be committed.
