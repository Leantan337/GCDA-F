#!/bin/bash
set -e  # Exit on error

echo "🚀 Starting application initialization..."

# Run migrations
echo "🔧 Running database migrations..."
python manage.py migrate --noinput

# Create superuser if environment variables are set
if [[ -n "${DJANGO_SUPERUSER_EMAIL}" ]] && [[ -n "${DJANGO_SUPERUSER_PASSWORD}" ]]; then
    echo "👤 Creating superuser..."
    python manage.py createsuperuser --noinput --email "${DJANGO_SUPERUSER_EMAIL}" --username "${DJANGO_SUPERUSER_USERNAME:-admin}" || true
fi

# Start gunicorn
echo "🌟 Starting Gunicorn..."
gunicorn config.wsgi:application
