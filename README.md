# Cypher - University Results Analyzer

> **⚠️ Educational Project Disclaimer**
> 
> This is a personal learning project created for educational purposes. It demonstrates web scraping, data parsing, and analytics techniques. This project is not officially affiliated with any university or portal system. Use responsibly and only with proper authorization for your own academic data.

## Overview

Cypher is a web application that automates university examination result retrieval and analysis. It scrapes result data from portals, parses student information and grades, and generates performance analytics.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)
![Status](https://img.shields.io/badge/Status-v1.1-success?style=for-the-badge)

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+
- Google Chrome browser
- pip package manager

### Step 1: Clone & Setup

```bash
# Clone the repository
git clone https://github.com/xorinf/cypher.git
cd cypher

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Step 2: Configure

```bash
# Copy example config
cp .env.example .env
```

Edit `.env` with your details:
```env
# University Portal URL
CAMPX_BASE_URL=https://your-university-portal.edu/results

# Testing Hall Ticket (Required for Integration Tests)
EX_HTN=YOUR_HALLTICKET_NUMBER
```

### Step 3: Run

**Backend API:**
```bash
# From project root
source venv/bin/activate
python backend/app.py
```

**Frontend:**
```bash
cd frontend && python3 -m http.server 8080
```

**Open:** http://localhost:8080

---

## 🧪 Testing

The project includes a comprehensive test suite.

```bash
# Activate virtual environment
source venv/bin/activate

# 1. Run Unit Tests (Parser, Analytics, API logic)
python -m pytest tests/test_units.py -v

# 2. Run Scraper Integration Test (Uses Mock Data)
python tests/test_scraper.py
# (Select Option 1 for Mock Data)

# 3. Run Real Results Integration Test (Requires .env configuration)
python tests/test_real_results.py
```

**Test Reports:**
Integration tests generate reports in the `generated/` directory:
- `generated/results_report.html` (Visual Report)
- `generated/real_results.json` (Parsed Data)

---

## 🎯 Features

- **📊 Automated Scraping** - Robust Selenium-based scraping with `webdriver-manager`
- **📈 Advanced Analytics** - GPA calculation, credit summary, and performance classification
- **📑 Export Options** - Download results as CSV or Excel
- **🎨 Modern UI** - Dark theme with responsive design
- **🔒 Secure** - Environment-based configuration and clean architecture

---

## 📁 Project Structure (Refactored)

```
cypher/
├── backend/                   # Backend Application
│   ├── app.py                 # Flask App Entry Point
│   ├── core/                  # Core Systems
│   │   ├── config.py          # Configuration Management
│   │   └── logger.py          # Structured Logging
│   ├── services/              # Business Logic Services
│   │   ├── scraper.py         # Selenium Scraper
│   │   ├── parser.py          # HTML Parser (BS4)
│   │   ├── analytics.py       # GPA Logic
│   │   └── exporter.py        # File Exporter
│   └── requirements.txt       # Dependencies
│
├── frontend/                  # Web UI
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── tests/                     # Test Suite
│   ├── fixtures/              # Mock Data
│   ├── test_units.py          # Unit Tests
│   ├── test_scraper.py        # Scraper Tests
│   └── test_real_results.py   # Full Integration Test
│
├── generated/                 # Test Outputs (gitignored)
├── legacy/                    # Archived Codebase
├── .env.example               # Config Template
└── README.md                  # This file
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.8+, Flask 3.0 |
| Automation | Selenium 4.16, WebDriver Manager |
| Parsing | BeautifulSoup 4.12, lxml |
| Data | Pandas 2.1, OpenPyXL 3.1 |
| Architecture | Modular Service-Based |

---

## 🔒 Security

- All sensitive URLs and IDs configured via `.env`
- No hardcoded credentials
- Structured logging prevents sensitive data leakage
- `.env` is gitignored

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📝 License

Educational project - use responsibly with proper authorization.

---

**Made with ❤️ for easier academic result tracking**
