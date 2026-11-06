#!/bin/bash

echo "Setting up the environment..."

# Step 1: Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it and try again."
    exit 1
fi

# Step 2: Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run the application
echo "Starting the Flask app..."
python backend/app.py

