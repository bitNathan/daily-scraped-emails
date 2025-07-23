#!/bin/bash

LOGFILE=""
PROJECT_DIR=""

if [[ -z "$1" ]]; then
  echo "[$(date '+%F %T')] ERROR: No project path specified."
  echo "Usage: $0 /path/to/project" >&2
  exit 1
fi

PROJECT_DIR="$1"
LOGFILE="$PROJECT_DIR/cron.log"

# validate directory
if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "[$(date '+%F %T')] ERROR: Directory not found: $PROJECT_DIR" | tee -a "$LOGFILE" >&2
  exit 1
fi

cd "$PROJECT_DIR" || {
  echo "[$(date '+%F %T')] ERROR: Could not cd into $PROJECT_DIR" | tee -a "$LOGFILE" >&2
  exit 1
}

# make sure directory is a git repo
if [[ ! -d ".git" ]]; then
  echo "[$(date '+%F %T')] ERROR: Not a Git repo: $PROJECT_DIR" | tee -a "$LOGFILE" >&2
  exit 1
fi

# save everythiong to cron log
{
  echo "[$(date '+%F %T')] --- Starting git update in $PROJECT_DIR ---"
  git fetch origin
   
  # Check for new commits in the remote that aren't in local
  UPSTREAM="@{u}"
  LOCAL=$(git rev-parse @)
  REMOTE=$(git rev-parse "$UPSTREAM")
  BASE=$(git merge-base @ "$UPSTREAM")

  if [[ "$LOCAL" = "$REMOTE" ]]; then
    echo "[$(date '+%F %T')] Up-to-date, nothing to pull."
  elif [[ "$LOCAL" = "$BASE" ]]; then
    echo "[$(date '+%F %T')] New changes detected. Running git pull..."
    git pull --ff-only || {
      echo "[$(date '+%F %T')] ERROR: git pull failed!"
      exit 1
    }
    echo "[$(date '+%F %T')] git pull successful."
  else
    echo "[$(date '+%F %T')] WARNING: Local repo diverged from remote. Manual intervention needed."
    exit 1
  fi

  echo "[$(date '+%F %T')] --- Update complete ---"
} >> "$LOGFILE" 2>&1
