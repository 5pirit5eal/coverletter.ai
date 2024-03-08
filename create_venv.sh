#!/bin/bash

# Check if .venv folder exists
if [ -d ".venv" ]; then
    # Prompt user for confirmation
    read -p "The .venv folder already exists. Do you want to delete it? (y/n): " confirm

    # Check user's response
    if [ "$confirm" = "y" ]; then
        # Delete .venv folder
        rm -rf .venv
        echo "Deleted .venv folder."
    else
        echo "Skipping deletion of .venv folder."
        return
    fi
fi

python -m venv .venv --prompt coverletter
source .venv/bin/activate
pip install -r requirements.txt
pip install -r dev-requirements.txt