"""
Django settings for GCDA project.
"""

import os
import sys
from pathlib import Path
from urllib.parse import urlparse

# Load env variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# Add Railway domains to allowed hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# Check for Railway external hostname
RAILWAY_HOSTNAME = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
if RAILWAY_HOSTNAME:
    ALLOWED_HOSTS.append(RAILWAY_HOSTNAME)

# Add any Railway domains
ALLOWED_HOSTS.extend(['.up.railway.app'])

# CSRF settings - allow requests from the browser preview
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://127.0.0.1:7552', 'http://localhost:8000']

# Add Railway domains to CSRF trusted origins
if RAILWAY_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.extend([
        f'https://{RAILWAY_HOSTNAME}',
        'https://gcda-f-production.up.railway.app'
    ])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Wagtail apps
    'wagtail',
    'wagtail.admin',
    'wagtail.documents',
    'wagtail.snippets',
    'wagtail.users',
    'wagtail.images',
    'wagtail.embeds',
    'wagtail.search',
    'wagtail.sites',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail_modeladmin',  
    'taggit',  

    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap4',  

    # Local apps
    'apps.core.apps.CoreConfig',
    'apps.news.apps.NewsConfig',  
    'apps.donations.apps.DonationsConfig',
    'apps.engagement.apps.EngagementConfig',
    'apps.comments.apps.CommentsConfig',
]

# Add this setting (usually ID 1 is the default site)
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# Use PostgreSQL on Railway, SQLite locally
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Use dj_database_url for Railway PostgreSQL
    import dj_database_url
    # Print the DATABASE_URL for debugging (will be hidden in logs)
    print(f"Connecting to database with URL: {DATABASE_URL}")
    
    # Parse DATABASE_URL to get configuration
    db_config = dj_database_url.parse(DATABASE_URL)
    
    # Explicitly set database configuration
    DATABASES = {
        'default': db_config
    }
    
    # Print database config for debugging (password will be hidden in logs)
    print(f"Database config: Engine={db_config.get('ENGINE')}, Name={db_config.get('NAME')}, Host={db_config.get('HOST')}, Port={db_config.get('PORT')}")
else:
    # Use SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = '/opt/data/media' if not DEBUG else os.path.join(BASE_DIR, 'media')

# Ensure media directory exists
os.makedirs(MEDIA_ROOT, exist_ok=True)

# AWS S3 Configuration
USE_S3 = os.environ.get('USE_S3', '') == 'True'

# Always use WhiteNoise for static files (regardless of S3 setting)
if not DEBUG:
    # Use WhiteNoise for static files
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configure media storage based on environment
if not DEBUG and not USE_S3:
    # Store media in staticfiles directory when not using S3
    MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
    MEDIA_URL = '/staticfiles/media/'
    
    # Ensure media directory exists
    os.makedirs(MEDIA_ROOT, exist_ok=True)

# S3 Configuration for media files only (when enabled)
if USE_S3:
    # S3 Storage Credentials
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'eu-north-1')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    
    # Add storages to installed apps
    INSTALLED_APPS += ['storages']
    
    # Only use S3 for media files, not static files
    DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaStorage'
    
    # Specific Wagtail image and document storage settings
    WAGTAILDOCS_DOCUMENT_MODEL = 'wagtaildocs.Document'
    WAGTAILIMAGES_IMAGE_MODEL = 'wagtailimages.Image'
    
    # Ensure Wagtail images use the same storage
    WAGTAILIMAGES_STORAGE = 'config.storage_backends.MediaStorage'
    WAGTAILDOCS_STORAGE = 'config.storage_backends.MediaStorage'
    
    # Media URL for S3
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Configure Wagtail to use the database for image renditions
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Wagtail settings
WAGTAIL_SITE_NAME = "GCDA"
# Using default Wagtail image model

# Search
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend
if DEBUG:
    WAGTAILADMIN_BASE_URL = 'http://localhost:8000'
elif RAILWAY_HOSTNAME:
    WAGTAILADMIN_BASE_URL = f'https://{RAILWAY_HOSTNAME}'
else:
    WAGTAILADMIN_BASE_URL = 'https://gcda.up.railway.app'

# Email settings (use console in development, configure for production)
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Add these settings for crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"