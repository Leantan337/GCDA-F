from django.apps import AppConfig
from django.utils.functional import cached_property
class CommentsConfig(AppConfig):
    @cached_property
    def default_auto_field(self):
        return 'django.db.models.BigAutoField'
    
    name = 'apps.comments'