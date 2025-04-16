#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting deployment initialization..."

# Wait for the database to be fully available
echo "Waiting for database to be ready..."
sleep 5

# Run S3 diagnostics
echo "Running S3 diagnostics..."
python debug_s3.py
python test_s3_upload.py

# Run the custom migration fixer to mark problematic migration as applied
echo "Running migration fixer..."
python fix_migrations.py

# Then run migrations normally
echo "Running migrations..."
python manage.py migrate

# Create cache table
echo "Creating cache table..."
python manage.py createcachetable

# Create Wagtail site entry if needed
echo "Configuring Wagtail site..."
python manage.py shell -c "from wagtail.models import Site; from os import environ; hostname = environ.get('RAILWAY_PUBLIC_DOMAIN', 'gcda.up.railway.app'); Site.objects.get_or_create(hostname=hostname, port=80, is_default_site=True, root_page_id=1, site_name='GCDA Website')"

# Run additional Wagtail storage diagnostics after migrations
echo "Running Wagtail storage diagnostics..."
python debug_wagtail_storage.py

# Create a superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput
fi

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn config.wsgi:application
