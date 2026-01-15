#!/bin/bash

# Cypher Setup Script
# This script sets up the development environment

echo "🚀 Setting up Cypher..."

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "📚 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Create exports directory
echo "📁 Creating exports directory..."
cd ..
mkdir -p exports

# Copy environment file
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. You can edit it if needed."
fi

echo ""
echo "🎉 Setup complete! To start the application:"
echo ""
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start the backend server:"
echo "   cd backend && python app.py"
echo ""
echo "3. Open frontend/index.html in your browser"
echo ""
echo "Happy coding! 🚀"
