#!/usr/bin/env bash
# start.sh
set -o errexit
set -o pipefail
set -o nounset

# Run Uvicorn with proper settings for Render
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
