from .base import *  # noqa

# Test settings
DEBUG = False
TEMPLATE_DEBUG = False

# Use SQLite for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable password hashing to speed up tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable migrations for tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Email settings for tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Media settings for tests
MEDIA_ROOT = BASE_DIR / 'test_media'

# Cache settings for tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Disable Wagtail signals during testing
WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAIL_ENABLE_WHATS_NEW_BANNER = False