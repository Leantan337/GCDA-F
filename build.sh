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

# Create superuser idempotently
echo "Attempting to create superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'secret123')
    print("Superuser created successfully!")
else:
    print("Superuser already exists, skipping creation.")
EOF

# Build phase complete - database operations will be handled during deployment
echo "Build phase complete. Database migrations will run on startup."
