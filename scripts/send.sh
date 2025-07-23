#!/bin/bash
# script for automation with cron scheduler
# Example: ./start.sh /absolute/path/to/project

# Exit if no path is provided
if [ -z "$1" ]; then
  echo "Error: No project path provided."
  echo "Usage: $0 /absolute/path/to/project"
  exit 1
fi

PROJECT_PATH="$1"
ENV="$PROJECT_PATH/env"
PYTHON_BIN="$ENV/bin/python"
SCRIPT="$PROJECT_PATH/main.py"
LOG="$PROJECT_PATH/cron.log"

# Validate existence of essential files and directories
if [ ! -d "$ENV" ]; then
  echo "Error: Python virtual environment not found at $ENV"
  exit 1
fi

if [ ! -f "$SCRIPT" ]; then
  echo "Error: Python script not found at $SCRIPT"
  exit 1
fi

# Navigate to the project directory
cd "$PROJECT_PATH" || {
  echo "Error: Failed to change directory to $PROJECT_PATH"
  exit 1
}

# Activate the virtual environment and run the script
source "$ENV/bin/activate"
"$PYTHON_BIN" "$SCRIPT" >> "$LOG" 2>&1
