# Cypher - University Results Analyzer

> **⚠️ Educational Project Disclaimer**
> 
> This is a personal learning project created for educational purposes only. Use responsibly and only with proper authorization for your own academic data.

## Overview

Cypher is a high-performance university results scraping and analysis system using direct API integration for maximum speed and efficiency.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)

## ✨ Features

### Core Functionality
- 🚀 **High-Performance API Scraping**
  - Direct API integration (63x faster than browser automation)
  - Lightweight and resource-efficient
- 📊 **Advanced Analytics**
  - GPA calculation and performance analysis
  - Grade distribution and trends
  - Pass/Fail status tracking
- 📁 **Export Capabilities**
  - CSV and Excel formats
  - HTML report generation
- 🔒 **Security First**
  - Input validation and sanitization
  - Environment-based configuration

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

```bash
# Clone repository
git clone https://github.com/xorinf/cypher.git
cd cypher

# Run automated setup
./setup.sh
```

### Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration
```

### Configuration (.env)

```env
# Portal URLs
CAMPX_BASE_URL=https://your-portal.edu/results
CAMPX_API_URL=https://api.your-portal.edu/student-results

# Authentication Headers
CAMPX_INSTITUTION_CODE=your_code
CAMPX_TENANT_ID=your_tenant

# Testing
EX_HTN=YOUR_HALL_TICKET
```

### Running

**Backend API:**
```bash
source venv/bin/activate
python backend/app.py
```

**Frontend:**
```bash
cd frontend && python3 -m http.server 8080
```

Access at: http://localhost:8080

## 📁 Project Structure

```
cypher/
├── backend/              # Flask API server
│   ├── app.py           # Entry point
│   ├── core/            # Config & logging
│   ├── services/        # Business logic
│   │   ├── scraper.py       # API scraper
│   │   ├── parser.py        # Data parsing
│   │   ├── analytics.py     # Analytics engine
│   │   └── exporter.py      # Export services
│   └── utils/           # Validators
│
├── tests/               # Test suite
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│
├── docs/               # Documentation
│   ├── API.md          # API reference
│   └── ARCHITECTURE.md # System design
│
├── frontend/           # Web interface
├── scripts/            # Utility scripts
└── generated/          # Auto-generated files
```

## 🧪 Testing

```bash
# Activate environment
source venv/bin/activate

# Unit tests
python -m pytest tests/unit/ -v

# Integration tests
python tests/integration/test_real_results.py

# Full verification
./scripts/verify.sh
```

## 📊 Performance

| Method | Time | Speedup |
|--------|------|---------|
| API Scraper | 0.15s | 67x faster |

## 🛠️ Tech Stack

 - **Backend**: Python 3.8+, Flask 3.0
 - **Scraping**: Requests (Direct API)
 - **Parsing**: Standard JSON
 - **Data**: Pandas 2.2+, OpenPyXL 3.1
 - **Testing**: pytest

## 📚 Documentation

- [API Documentation](docs/API.md) - API endpoints and usage
- [Architecture](docs/ARCHITECTURE.md) - System design and data flow

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📝 License

Educational project - use responsibly with proper authorization.

---

**Made with ❤️ for easier academic result tracking**
