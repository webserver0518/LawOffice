#!/bin/bash

# Navigate to project folder
cd "$(dirname "$0")" || exit 1

# Remove old virtual environment if it exists
rm -rf .venv

# Create new virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Deactivate virtual environment
deactivate

# Reload systemd and restart the Flask service
sudo systemctl daemon-reload
sudo systemctl restart flask-lawofficesystem
sudo systemctl status flask-lawofficesystem
