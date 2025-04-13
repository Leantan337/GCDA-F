from django.apps import AppConfig
from django.utils.functional import cached_property
class DonationsConfig(AppConfig):
    @cached_property
    def default_auto_field(self) -> str:
        return 'django.db.models.BigAutoField'
    
    name = 'apps.donations'  # Update the name to include the apps prefix
