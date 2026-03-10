#!/bin/bash
set -e  # Exit on error

# Check if Python3 is installed
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed!"
    echo "Please install Python3:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-venv"
    echo "  macOS: brew install python3"
    exit 1
fi

python3 --version

echo "Creating Virtual Environment..."
python3 -m venv venv

if [ ! -f "venv/bin/activate" ]; then
    echo "ERROR: Failed to create virtual environment!"
    exit 1
fi

echo ""
echo "Activating Virtual Environment..."
source venv/bin/activate

echo ""
echo "Installing Dependencies..."
pip install -r requirements.txt

echo ""
echo "============================================"
echo "Setup Complete! Virtual environment is ready."
echo "============================================"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the application:"
echo "  python run.py"
