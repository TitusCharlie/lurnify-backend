#!/usr/bin/env bash
set -e

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting app..."

# Upgrade pip & reinstall bcrypt cleanly
pip install --upgrade pip
pip install --force-reinstall --no-cache-dir bcrypt==4.1.2

# Install dependencies
pip install -r requirements.txt

# start.sh
set -o errexit
set -o pipefail
set -o nounset

# Run Uvicorn with proper settings for Render
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
