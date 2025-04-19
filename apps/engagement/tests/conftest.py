import pytest

@pytest.fixture(autouse=True)
def set_test_staticfiles_storage(settings):
    settings.STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
