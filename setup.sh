#!/bin/bash

# Cypher Setup Script
# Automated setup for the Cypher project

set -e

echo "🚀 Cypher Setup"
echo "================"
echo ""

# Check Python version
echo "Step 1: Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "Step 2: Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate and install dependencies
echo ""
echo "Step 3: Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r backend/requirements.txt
echo "✓ Dependencies installed"

# Setup .env file
echo ""
echo "Step 4: Configuring environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your configuration:"
    echo "   - CAMPX_BASE_URL: Your university portal URL"
    echo "   - CAMPX_API_URL: API endpoint URL"
    echo "   - CAMPX_INSTITUTION_CODE: Your institution code"
    echo "   - CAMPX_TENANT_ID: Your tenant ID"
    echo "   - EX_HTN: Test hall ticket number"
else
    echo "✓ .env file already exists"
fi

# Create necessary directories
echo ""
echo "Step 5: Creating directories..."
mkdir -p generated
mkdir -p exports
echo "✓ Directories created"

# Run verification
echo ""
echo "Step 6: Running verification..."
./scripts/verify.sh

echo ""
echo "================================="
echo "✅ Setup Complete!"
echo ""
echo "Next Steps:"
echo "  1. Edit .env with your configuration"
echo "  2. Run: source venv/bin/activate"
echo "  3. Start backend: python backend/app.py"
echo "  4. Run tests: python -m pytest tests/unit/ -v"
echo ""
echo "Documentation:"
echo "  - README.md - Project overview"
echo "  - docs/API.md - API documentation"
echo "  - docs/ARCHITECTURE.md - System architecture"
echo ""
