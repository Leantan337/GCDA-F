#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create cache table
python manage.py createcachetable

# Create Wagtail site entry if needed
python manage.py shell -c "from wagtail.models import Site; Site.objects.get_or_create(hostname='gcda.onrender.com', port=80, is_default_site=True, root_page_id=1, site_name='GCDA Website')"
