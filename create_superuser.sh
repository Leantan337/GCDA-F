#!/usr/bin/env bash

# Create Django superuser idempotently
echo "Attempting to create superuser..."

# Python script to create superuser if it doesn't exist
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'secret123')
    print("Superuser created successfully!")
else:
    print("Superuser already exists, skipping creation.")
EOF
