#!/bin/bash
# Attack Path Mapper - Automated Setup Script
# This script automates the installation and setup process

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║      🎯 Attack Path Mapper - Automated Setup                 ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "[*] Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "[!] Error: Python 3 is not installed"
    echo "    Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "[+] Found Python $PYTHON_VERSION"

# Check if version is at least 3.8
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "[!] Error: Python 3.8 or higher is required"
    echo "    Current version: $PYTHON_VERSION"
    exit 1
fi

# Check pip
echo "[*] Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "[!] Error: pip is not installed"
    echo "    Please install pip for Python 3"
    exit 1
fi
echo "[+] pip found"

# Install dependencies
echo ""
echo "[*] Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "[+] Dependencies installed successfully"
else
    echo "[!] Error installing dependencies"
    exit 1
fi

# Create demo data
echo ""
echo "[*] Creating sample scan data..."
python3 attack_path_mapper.py --demo

if [ $? -eq 0 ]; then
    echo "[+] Sample data created"
else
    echo "[!] Error creating sample data"
    exit 1
fi

# Run a test analysis
echo ""
echo "[*] Running test analysis..."
python3 attack_path_mapper.py sample_scan.json > test_output.txt 2>&1

if [ $? -eq 0 ]; then
    echo "[+] Test analysis completed successfully"
    rm test_output.txt
else
    echo "[!] Error running test analysis"
    cat test_output.txt
    rm test_output.txt
    exit 1
fi

# Success message
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                   ✅ Setup Complete!                          ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "You're all set! Here's what you can do now:"
echo ""
echo "1. Run analysis on sample data:"
echo "   python3 attack_path_mapper.py sample_scan.json"
echo ""
echo "2. Start the web interface:"
echo "   python3 web_visualizer.py"
echo "   Then open: http://localhost:8000"
echo ""
echo "3. Try the complex example:"
echo "   python3 attack_path_mapper.py example_scan_complex.json"
echo ""
echo "4. Read the documentation:"
echo "   - README.md - Full documentation"
echo "   - QUICKSTART.md - Quick start guide"
echo "   - MITRE_MAPPING.md - ATT&CK technique reference"
echo ""
echo "Happy hacking! 🎯"
