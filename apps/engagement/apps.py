from django.apps import AppConfig
from django.utils.functional import cached_property
class EngagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.engagement'
    label = 'engagement'
    verbose_name = 'Engagement'
