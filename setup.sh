#!/bin/bash
# Setup script for Linux/Mac

echo "========================================"
echo "Mass Spectrometry Data Processor Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Display Python version
PYTHON_VERSION=$(python3 --version)
echo "[OK] Found $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "[1/3] Creating virtual environment..."
python3 -m venv venv
echo "[OK] Virtual environment created"
echo ""

# Activate virtual environment and install dependencies
echo "[2/3] Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "[OK] Dependencies installed"
echo ""

# Create directory structure if needed
echo "[3/3] Setting up directory structure..."
mkdir -p input output scripts utils
echo "[OK] Directory structure ready"
echo ""

echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo ""
echo "To get started:"
echo "  1. Place your CSV file in the 'input/' directory and rename it to 'data.csv'"
echo "  2. Activate the virtual environment: source venv/bin/activate"
echo "  3. Run a script: python scripts/01_remove_header_lines.py"
echo ""
