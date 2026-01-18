# Cypher - University Results Analyzer

> **⚠️ Educational Project Disclaimer**
> 
> This is a personal learning project created for educational purposes. It demonstrates web scraping, data parsing, and analytics techniques. This project is not officially affiliated with any university or portal system. Use responsibly and only with proper authorization for your own academic data.

## Overview

Cypher is a web application that automates university examination result retrieval and analysis. It scrapes result data from portals, parses student information and grades, and generates performance analytics.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)
![Status](https://img.shields.io/badge/Status-v1.0-success?style=for-the-badge)

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

# Edit .env with your portal URL
nano .env  # or use any text editor
```

Set your university portal URL:
```env
CAMPX_BASE_URL=https://your-university-portal.edu/results
```

### Step 3: Run

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
cd backend && python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend && python3 -m http.server 8080
```

**Open:** http://localhost:8080

---

## 📖 Usage

1. Enter your **Hall Ticket Number**
2. Select **Exam Type** (Regular/Supplementary)
3. Choose **View Type** (All Semesters/Current)
4. Click **Get Results**
5. View analytics and **Export** as CSV/Excel

---

## 🧪 Testing

```bash
# Activate virtual environment
source venv/bin/activate

# Run unit tests (27 tests)
python -m pytest tests/test_units.py -v

# Run real results test (generates HTML report)
python tests/test_real_results.py
# Report saved to: generated/results_report.html
```

---

## 🎯 Features

- **📊 Automated Scraping** - Selenium-based result fetching
- **📈 GPA Analytics** - Automatic grade point calculation
- **📑 Export Options** - Download as CSV or Excel
- **🎨 Modern UI** - Dark theme with responsive design
- **🔒 Secure** - Environment-based configuration

---

## 📁 Project Structure

```
cypher/
├── backend/           # Flask API + Scraper
│   ├── app.py         # API server
│   ├── scraper.py     # Selenium scraper  
│   ├── parser.py      # HTML parser
│   ├── analytics.py   # GPA calculations
│   └── exporter.py    # CSV/Excel export
├── frontend/          # Web UI
│   ├── index.html     # Main page
│   ├── styles.css     # Styling
│   └── app.js         # Frontend logic
├── tests/             # Test suite
│   ├── test_units.py  # Unit tests
│   └── fixtures/      # Mock data
├── generated/         # Test outputs (gitignored)
├── .env.example       # Config template
└── README.md          # This file
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.8+, Flask 3.0 |
| Scraping | Selenium 4.16, BeautifulSoup 4.12 |
| Data | Pandas 2.1, OpenPyXL 3.1 |
| Frontend | HTML5, CSS3, JavaScript |

---

## 🔒 Security

- All URLs configured via `.env` (never hardcoded)
- Personal data processed locally only
- Test fixtures use sanitized mock data
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
