#!/bin/bash

# Vercel build script for Django
echo "Starting build process..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate --noinput

echo "Build completed successfully!" 