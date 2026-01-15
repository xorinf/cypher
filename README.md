# Cypher - University Results Analyzer

> **⚠️ Educational Project Disclaimer**
> 
> This is a personal learning project created for educational purposes. It demonstrates web scraping, data parsing, and analytics techniques. This project is not officially affiliated with any university or portal system. Use responsibly and only with proper authorization for your own academic data.

## Overview

Cypher is a web application designed to automate the retrieval and analysis of university examination results. It provides tools for fetching result data from university portals, parsing structured information, and generating analytics on academic performance.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

---

## 🎯 Features

### Core Functionality
- **📊 Automated Data Retrieval**: Web scraping with Selenium for result fetching
- **📈 Advanced Analytics**: GPA calculation, grade distribution, and performance insights
- **📑 Export Options**: Download results as CSV or Excel with detailed formatting
- **🎨 Modern UI**: Premium dark theme with smooth animations and responsive design
- **🔒 Secure Configuration**: Environment-based configuration for sensitive URLs

### Analytics Dashboard
- Real-time GPA calculation
- Subject-wise performance analysis
- Pass/fail status tracking
- Grade distribution visualization  
- Performance level classification

---

## 🏗️ Architecture

### Backend (Python + Flask)
- **Flask API Server** ([backend/app.py](file:///Users/yashhwanth/Documents/cypher/backend/app.py))
- **Web Scraper** ([backend/scraper.py](file:///Users/yashhwanth/Documents/cypher/backend/scraper.py)) - Selenium-based automation
- **HTML Parser** ([backend/parser.py](file:///Users/yashhwanth/Documents/cypher/backend/parser.py)) - BeautifulSoup data extraction
- **Analytics Engine** ([backend/analytics.py](file:///Users/yashhwanth/Documents/cypher/backend/analytics.py)) - Performance calculations
- **Data Exporter** ([backend/exporter.py](file:///Users/yashhwanth/Documents/cypher/backend/exporter.py)) - CSV/Excel generation

### Frontend (HTML + CSS + JavaScript)
- **Responsive UI** ([frontend/index.html](file:///Users/yashhwanth/Documents/cypher/frontend/index.html))
- **Premium Styling** ([frontend/styles.css](file:///Users/yashhwanth/Documents/cypher/frontend/styles.css)) - Dark theme with gradients
- **Dynamic Rendering** ([frontend/app.js](file:///Users/yashhwanth/Documents/cypher/frontend/app.js)) - API integration and state management

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Chrome browser (for Selenium)
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/xorinf/cypher.git
   cd cypher
   ```

2. **Set up Python virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

4. **Install ChromeDriver** (will be handled automatically by webdriver-manager)
   The application uses `webdriver-manager` which automatically downloads the correct ChromeDriver version.

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and set:
   ```env
   # Replace with your university's results portal URL
   CAMPX_BASE_URL=https://your-university-portal.edu/results
   FLASK_PORT=5000
   FLASK_DEBUG=True
   EXPORT_DIR=./exports
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   source venv/bin/activate
   cd backend
   python app.py
   ```
   Server will run on `http://localhost:5000`

2. **Open the frontend**
   Open `frontend/index.html` in your browser, or use a local server:
   ```bash
   cd frontend
   python -m http.server 8080
   ```
   Navigate to `http://localhost:8080`

---

## 📖 Usage

1. **Configure Your Portal**: Edit `.env` with your university's results portal URL
2. **Enter Hall Ticket Number**: Input your student hall ticket number
3. **Select Options**: Choose examination type and semester view
4. **Fetch Results**: Click "Get Results" to retrieve your data
5. **View Analytics**: Review your GPA, grades, and performance summary
6. **Export Data**: Download results as CSV or Excel

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.8+, Flask 3.0 |
| **Web Scraping** | Selenium 4.16, BeautifulSoup 4.12 |
| **Data Processing** | Pandas 2.1, OpenPyXL 3.1 |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Styling** | CSS Variables, Gradients, Animations |
| **Fonts** | Google Fonts (Inter) |

---

## 📁 Project Structure

```
cypher/
├── backend/
│   ├── app.py              # Flask API server
│   ├── scraper.py          # Selenium web scraper
│   ├── parser.py           # HTML parser
│   ├── analytics.py        # Analytics engine
│   ├── exporter.py         # CSV/Excel exporter
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Main UI page
│   ├── styles.css          # Premium styling
│   └── app.js              # Frontend logic
├── tests/
│   ├── test_scraper.py     # Test suite
│   ├── fixtures/           # Mock test data
│   └── README.md           # Testing guide
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

---

## 🧪 Testing

### Run Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run test suite
python tests/test_scraper.py
```

The test suite offers two modes:
1. **Mock Data Testing**: Tests parser with sanitized fixtures (no network required)
2. **Real Data Testing**: Tests full scraper with your hallticket (requires configuration)

See [tests/README.md](file:///Users/yashhwanth/Documents/cypher/tests/README.md) for detailed testing instructions.

---

## 🔧 Configuration

All sensitive configuration is managed through the `.env` file:

```env
# Your university's results portal URL
CAMPX_BASE_URL=https://your-university-portal.edu/results

# Flask server port
FLASK_PORT=5000

# Enable debug mode (disable in production)
FLASK_DEBUG=True

# Directory for exported files
EXPORT_DIR=./exports
```

> **Security Note**: Never commit your `.env` file to version control. It's already in `.gitignore`.

---

## 🔒 Security & Privacy

- **No Hardcoded URLs**: All portal URLs are configurable via environment variables
- **Personal Data Protection**: Test fixtures use sanitized mock data
- **Secure Credentials**: Your hallticket and results are never stored or transmitted
- **Local Processing**: All data processing happens locally on your machine

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

This project is for educational purposes. Use responsibly and only with proper authorization.

---

## 🙏 Acknowledgments

- Built as a learning project for web scraping and data analysis
- Demonstrates integration with university portal systems

---

**Made with ❤️ for easier academic result tracking**
