#!/bin/bash
set -e  # Exit on error

echo "🚀 Starting build process..."

# Create necessary directories in the persistent volume
echo "📁 Setting up persistent storage directories..."
mkdir -p /media/staticfiles
mkdir -p /media/uploads
chmod -R 755 /media

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Django setup commands
echo "🔧 Running Django migrations..."
python manage.py migrate --noinput

echo "📚 Collecting static files..."
python manage.py collectstatic --noinput

# Create cache table for sessions if not exists
echo "🗄️ Setting up cache tables..."
python manage.py createcachetable

# Optional: Compress static files
echo "🗜️ Compressing static files..."
python manage.py compress --force

# Create superuser if environment variables are set
if [[ -n "${DJANGO_SUPERUSER_EMAIL}" ]] && [[ -n "${DJANGO_SUPERUSER_PASSWORD}" ]]; then
    echo "👤 Creating superuser..."
    python manage.py createsuperuser --noinput --email "${DJANGO_SUPERUSER_EMAIL}" --username "${DJANGO_SUPERUSER_USERNAME:-admin}"
fi

echo "✅ Build process completed successfully!"
