#!/bin/bash
set -e  # Exit on error

echo "🚀 Starting application initialization..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until PGPASSWORD=$PGPASSWORD psql -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" -c '\q' 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping 2s"
  sleep 2
done
echo "✅ PostgreSQL is ready!"

# Run migrations
echo "🔧 Running database migrations..."
python manage.py migrate --noinput || {
    echo "❌ Migration failed!"
    exit 1
}

# Create superuser if environment variables are set
if [[ -n "${DJANGO_SUPERUSER_EMAIL}" ]] && [[ -n "${DJANGO_SUPERUSER_PASSWORD}" ]]; then
    echo "👤 Creating superuser..."
    python manage.py createsuperuser --noinput --email "${DJANGO_SUPERUSER_EMAIL}" \
        --username "${DJANGO_SUPERUSER_USERNAME:-admin}" || echo "⚠️ Superuser already exists"
fi

# Start gunicorn with proper settings
echo "🌟 Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
