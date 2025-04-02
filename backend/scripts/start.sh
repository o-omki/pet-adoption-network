#!/bin/bash
set -e

# Run migrations if needed (only in production)
if [ "$APP_ENV" = "prod" ]; then
    echo "Running database migrations..."
    alembic upgrade head
fi

# Start the FastAPI application with Uvicorn
echo "Starting Pet Adoption Network API server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level "${LOG_LEVEL:-info}" --proxy-headers