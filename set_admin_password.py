
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngo_website.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='admin')
user.set_password('admin123')
user.save()

print("Password set successfully for admin user")
