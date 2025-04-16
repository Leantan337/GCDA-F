#!/usr/bin/env bash
# exit on error
set -o errexit

# Print debug information
echo "Starting build process..."
ls -la

# Install dependencies
pip install -r requirements.txt

# Ensure media directory exists with proper permissions
mkdir -p /opt/data/media
chmod -R 755 /opt/data/media

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Set permissions on static files
chmod -R 755 staticfiles

# Ensure proper S3 configuration if enabled
if [ "$USE_S3" = 'True' ]; then
    echo "S3 storage enabled for media files"
fi

# Build phase complete - database operations will be handled during deployment
echo "Build phase complete. Database migrations will run on startup."
