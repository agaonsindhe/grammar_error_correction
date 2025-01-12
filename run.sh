#!/bin/bash

echo "Setting up the environment..."

# Step 1: Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it and try again."
    exit 1
else
    echo "Python 3 is installed: $(python3 --version)"
fi

# Step 2: Create and activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

# Step 3: Install dependencies
echo "Installing dependencies..."
pip install -r backend/requirements.txt

# Step 4: Run the Flask app and display output
echo "Starting the Flask app..."
PYTHONUNBUFFERED=1  python backend/app.py 2>&1
