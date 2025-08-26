#!/usr/bin/env -S /usr/bin/bash

# Check for mandatory parameter
if [ -z "$1" ]; then
    echo "Usage: $0 <audio-file.m4a | audio-file.wav>"
    exit 1
fi

# Virtual environment detection
VENV_DIR="venv"
PYTHON_SCRIPT="main.py"

if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found."
    echo "Please create it using 'python3 -m venv $VENV_DIR'"
    echo "Install dependencies using '$VENV_DIR/bin/pip install -r requirements.txt'"
    exit 1
fi

# Environment variables for python script
export OLLAMA_BASE_URL="http://MyPc1:11434"
export OLLAMA_MODEL_NAME="llama3.2:latest"
export OLLAMA_TIMEOUT_SECONDS="1800"

# Activate virtual environment and run the Python script
source "$VENV_DIR/bin/activate"

python3 "$PYTHON_SCRIPT" "$1"

deactivate