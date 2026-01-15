# Cypher

Cypher is a web/app application designed to automate the retrieval and analysis of college examination results. By integrating with the **CampX** system used by the university, Cypher fetches result spreadsheets and provides advanced tools for score analysis and academic performance tracking.

Cypher is a full-stack web application designed to automate the retrieval and analysis of college examination results from Anurag University's **CampX** system. It fetches result data, generates downloadable spreadsheets, and provides advanced analytics on academic performance.

![Cypher Application](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)

---

## 🎯 Features

### Core Functionality
- **🔗 CampX Integration**: Direct integration with Anurag University's CampX system
- **📊 Automated Data Retrieval**: Web scraping with Selenium for seamless result fetching
- **📈 Advanced Analytics**: GPA calculation, grade distribution, and performance insights
- **📑 Export Options**: Download results as CSV or Excel with detailed formatting
- **🎨 Modern UI**: Premium dark theme with smooth animations and responsive design

### Analytics Dashboard
- Real-time GPA calculation
- Subject-wise performance analysis
- Pass/fail status tracking
- Grade distribution visualization
- Performance level classification

---

## 🏗️ Architecture

### Backend (Python + Flask)
- **Flask API Server** (`backend/app.py`)
- **Web Scraper** (`backend/scraper.py`) - Selenium-based automation
- **HTML Parser** (`backend/parser.py`) - BeautifulSoup data extraction
- **Analytics Engine** (`backend/analytics.py`) - Performance calculations
- **Data Exporter** (`backend/exporter.py`) - CSV/Excel generation

### Frontend (HTML + CSS + JavaScript)
- **Responsive UI** (`frontend/index.html`)
- **Premium Styling** (`frontend/styles.css`) - Dark theme with gradients
- **Dynamic Rendering** (`frontend/app.js`) - API integration and state management

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Chrome browser (for Selenium)
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:xorinf/cypher.git
   cd cypher
   ```

2. **Set up Python virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Install ChromeDriver**
   ```bash
   # macOS
   brew install chromedriver
   
   # Linux
   sudo apt-get install chromium-chromedriver
   
   # Or download from: https://chromedriver.chromium.org/
   ```

5. **Configure environment variables**
   ```bash
   cd ..
   cp .env.example .env
   # Edit .env if needed
   ```

### Running the Application

1. **Start the backend server**
   ```bash
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

1. **Enter Hall Ticket Number**: Input your student hall ticket number
2. **Select Exam Type**: Choose the examination type (optional)
3. **Select View Type**: Choose "All Semesters" or "Current Semester"
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
| **Frontend** | HTML5, CSS3 (Custom), Vanilla JavaScript |
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
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

---

## 🔧 Configuration

Edit `.env` file to customize:

```env
CAMPX_BASE_URL=https://aupulse.campx.in/aupulse/ums/results
FLASK_PORT=5000
FLASK_DEBUG=True
EXPORT_DIR=./exports
```

---

## 🧪 Testing

To test with a hall ticket number:
1. Start the backend server
2. Open the frontend in browser
3. Enter a valid hall ticket number
4. Verify results are fetched and displayed correctly

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

## 📝 License

This project is built for educational purposes for Anurag University students.

---

## 🙏 Acknowledgments

- Built for Anurag University students
- Integrates with CampX Digital Campus Ecosystem

---

**Made with ❤️ for easier result checking**
=======
The primary goal of Cypher is to simplify the process of checking and analyzing college results, making it easier me to track my academic progress without navigating complex legacy systems.
- **TBH**: im bored.

## ⚠️ Disclaimer

**Cypher** is a personal, experimental project created for learning and exploration purposes only.

- This project is **not officially affiliated with, endorsed by, or supported by** the university or the **CampX** system.
- All data access and analysis are intended **strictly for personal academic use**.
- No attempt is made to bypass security mechanisms, misuse credentials, or access data without proper authorization.

### Compliance Notice

If this project or its methodology is found to violate any terms of service, policies, or regulations of **CampX** or the university:

- I will **immediately remove this repository**
- I will **stop using this method of result retrieval**
- Any related tools or automation will be **discontinued**

This repository exists purely as a **technical demonstration** and will be taken down upon request or in case of any compliance concerns.

