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

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create cache table
echo "Creating cache table..."
python manage.py createcachetable

# Create Wagtail site entry if needed
echo "Configuring Wagtail site..."
python manage.py shell -c "from wagtail.models import Site; from os import environ; hostname = environ.get('RAILWAY_PUBLIC_DOMAIN', 'gcda.up.railway.app'); Site.objects.get_or_create(hostname=hostname, port=80, is_default_site=True, root_page_id=1, site_name='GCDA Website')"

# Create a superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput
fi
