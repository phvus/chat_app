#!/bin/bash
echo "Creating Virtual Environment..."
python3 -m venv venv

echo ""
echo "Activating Virtual Environment..."
source venv/bin/activate

echo ""
echo "Installing Dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup Complete! Virtual environment is ready."
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the application:"
echo "  python run.py"
