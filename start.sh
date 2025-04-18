#!/bin/bash
set -e

echo "🚀 Starting application initialization..."

# Only check PostgreSQL if DATABASE_URL is set
if [ -n "$DATABASE_URL" ]; then
  check_postgres() {
      python << END
import sys
import psycopg2
from urllib.parse import urlparse
import os

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    print("No DATABASE_URL found")
    sys.exit(1)

try:
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port or 5432
    
    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    conn.close()
    sys.exit(0)
except Exception as e:
    print(f"PostgreSQL is unavailable - {str(e)}")
    sys.exit(1)
END
  }

  echo "⏳ Waiting for PostgreSQL to be ready..."
  count=0
  until check_postgres || [ $count -eq 30 ]; do
      echo "PostgreSQL is unavailable - sleeping 2s"
      sleep 2
      count=$((count + 1))
  done

  if [ $count -eq 30 ]; then
      echo "❌ Failed to connect to PostgreSQL after 60 seconds"
      exit 1
  fi
  echo "✅ PostgreSQL is ready"
fi

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
