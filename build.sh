#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset

# Install dependencies (Render does this automatically, but just in case)
pip install -r requirements.txt

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create Django superuser if it doesn't exist (fail-safe)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
username = "$DJANGO_SUPERUSER_USERNAME"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, "$DJANGO_SUPERUSER_EMAIL", "$DJANGO_SUPERUSER_PASSWORD")
else:
    print(f"Superuser '{username}' already exists. Skipping creation.")
END
fi
