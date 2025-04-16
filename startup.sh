#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting deployment initialization..."

# Wait for the database to be fully available
echo "Waiting for database to be ready..."
sleep 5

# Check if we should fake migrations
echo "Checking database state..."
python -c "
import sys
import django
from django.db import connection
django.setup()
cursor = connection.cursor()
try:
    cursor.execute(\"SELECT * FROM news_newsindexpage LIMIT 1\")
    print('Table exists, will use --fake-initial flag for migrations')
    sys.exit(0)
except Exception as e:
    print('Table check failed, will run normal migrations')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    # Tables exist, use fake-initial
    echo "Running migrations with --fake-initial flag..."
    python manage.py migrate --fake-initial
else
    # Normal migrations
    echo "Running migrations..."
    python manage.py migrate
fi

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

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn config.wsgi:application
