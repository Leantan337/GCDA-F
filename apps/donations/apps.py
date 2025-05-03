from django.apps import AppConfig
from django.utils.functional import cached_property
class DonationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.donations'
    label = 'donations'
    verbose_name = 'Donations'
