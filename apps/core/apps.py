from django.apps import AppConfig
from django.utils.functional import cached_property

class CoreConfig(AppConfig):
    @cached_property
    def default_auto_field(self):
        return 'django.db.models.BigAutoField'
    
    name = 'apps.core'
    
    def ready(self):
        """
        Called when Django apps are fully loaded.
        Apply Wagtail storage overrides here to ensure everything is properly initialized.
        """
        from django.conf import settings
        if settings.USE_S3:
            # Import and apply storage overrides from wagtail_override
            try:
                from apps.wagtail_override import override_wagtail_storages
                print("Overriding Wagtail storage backend...")
                override_wagtail_storages()
                print("Storage backend overrides applied successfully!")
            except Exception as e:
                print(f" Error overriding storage: {e}")
