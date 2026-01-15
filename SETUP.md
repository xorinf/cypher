# Setup Guide - Cypher

This guide will help you set up and configure Cypher for your university's results portal.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Configuration](#configuration)
- [ChromeDriver Setup](#chromedriver-setup)
- [Testing Your Setup](#testing-your-setup)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed
- **Google Chrome** browser installed
- **Git** for cloning the repository
- **Access to your university's results portal** with a valid hallticket number

### Check Python Version

```bash
python3 --version
# Should output: Python 3.8.x or higher
```

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/xorinf/cypher.git
cd cypher
```

### 2. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\\Scripts\\activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

This installs:
- Flask (web server)
- Selenium (web automation)
- BeautifulSoup (HTML parsing)
- Pandas & OpenPyXL (data export)
- webdriver-manager (automatic ChromeDriver management)

---

## Configuration

### 1. Create Environment File

```bash
cp .env.example .env
```

### 2. Edit .env File

Open `.env` in your text editor and configure:

```env
# CRITICAL: Replace with your university's actual results portal URL
# Example: https://university.edu/student/results
CAMPX_BASE_URL=https://your-university-portal.edu/results

# Flask server configuration (change if port 5000 is in use)
FLASK_PORT=5000

# Enable debug mode for development
FLASK_DEBUG=True

# Directory where CSV/Excel exports will be saved
EXPORT_DIR=./exports
```

### 3. Finding Your University's Portal URL

1. Open your university's results portal in a browser
2. Navigate to the results checking page
3. Copy the full URL from the address bar
4. Paste it in your `.env` file as `CAMPX_BASE_URL`

**Example URLs:**
- `https://university.edu/student/results`
- `https://portal.university.edu/exam-results`
- `https://results.university.ac.in/student/view`

---

## ChromeDriver Setup

Cypher uses `webdriver-manager` which **automatically downloads** the correct ChromeDriver version for your Chrome browser. No manual installation needed!

### Verify Chrome Installation

```bash
# macOS
/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --version

# Linux
google-chrome --version

# Windows
"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --version
```

If Chrome is not installed:
- **macOS**: Download from [google.com/chrome](https://www.google.com/chrome/)
- **Linux**: `sudo apt-get install google-chrome-stable`
- **Windows**: Download from [google.com/chrome](https://www.google.com/chrome/)

---

## Testing Your Setup

### Test 1: Environment Configuration

```bash
source venv/bin/activate  # Skip on Windows: already activated
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('URL:', os.getenv('CAMPX_BASE_URL'))"
```

Should output your configured URL (not the placeholder).

### Test 2: Dependencies

```bash
python -c "import flask, selenium, bs4, pandas; print('✅ All dependencies installed')"
```

Should output: `✅ All dependencies installed`

### Test 3: Mock Data Test

```bash
python tests/test_scraper.py
# Choose option 1 (Mock data test)
```

Should successfully parse mock fixture data.

### Test 4: Real Data Test (Optional)

1. Edit `tests/test_scraper.py`
2. Replace `YOUR_HALLTICKET_HERE` with your actual hallticket
3. Run:
   ```bash
   python tests/test_scraper.py
   # Choose option 2 (Real data test)
   ```

---

## Running the Application

### Start Backend Server

```bash
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
cd backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000/
```

### Open Frontend

**Option 1: Direct File**
- Open `frontend/index.html` in your browser

**Option 2: Local Server (Recommended)**
```bash
# In a new terminal
cd frontend
python -m http.server 8080
```
Then navigate to `http://localhost:8080`

---

## Troubleshooting

### Issue: "CAMPX_BASE_URL environment variable is not set"

**Solution:**
- Ensure `.env` file exists in project root
- Verify `CAMPX_BASE_URL` is set (not the placeholder)
- Restart the backend server

### Issue: ChromeDriver compatibility error

**Solution:**
```bash
pip install --upgrade webdriver-manager selenium
```

The webdriver-manager will download the correct version automatically.

### Issue: "Module not found" errors

**Solution:**
```bash
source venv/bin/activate
pip install -r backend/requirements.txt
```

### Issue: Results not loading / Invalid hallticket

**Checklist:**
1. Is your university portal URL correct in `.env`?
2. Is your hallticket number valid and active?
3. Is the portal accessible from your network?
4. Check if portal requires VPN or campus network

### Issue: Port 5000 already in use

**Solution:**
Edit `.env` and change:
```env
FLASK_PORT=5001  # or any available port
```

### Issue: Permission denied for exports directory

**Solution:**
```bash
mkdir -p exports
chmod 755 exports
```

---

## Next Steps

Once setup is complete:

1. ✅ Read the [README.md](file:///Users/yashhwanth/Documents/cypher/README.md) for usage instructions
2. ✅ Check [tests/README.md](file:///Users/yashhwanth/Documents/cypher/tests/README.md) for testing guide
3. ✅ Start the application and fetch your results!

---

## Security Reminders

- ⚠️ Never share your `.env` file
- ⚠️ Never commit sensitive data to version control
- ⚠️ Use this tool only for your own academic data
- ⚠️ Respect your university's terms of service

---

## Need Help?

If you encounter issues not covered here:
1. Check existing GitHub issues
2. Create a new issue with:
   - Your Python version
   - Error message (remove sensitive data)
   - Steps to reproduce

---

**Happy result tracking! 🎓**
