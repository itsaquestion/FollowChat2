#!/bin/bash
# Navigate to the script's directory
cd "$(dirname "$0")"

# Activate the virtual environment
source ./venv/bin/activate

# Run the Python script
python ./gen_scmp.py

