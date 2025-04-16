#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create media directory with proper permissions
mkdir -p media/images
chmod -R 777 media

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create cache table
python manage.py createcachetable

# Create Wagtail site entry if needed
python manage.py shell -c "from wagtail.models import Site; Site.objects.get_or_create(hostname='gcda.onrender.com', port=80, is_default_site=True, root_page_id=1, site_name='GCDA Website')"

# Create superuser if environment variables are set
#if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
#    echo "Creating superuser..."
#    python manage.py createsuperuser --noinput
#fi
