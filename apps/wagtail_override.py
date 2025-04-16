"""
This module directly overrides Wagtail's storage configuration.
"""

from django.conf import settings
from importlib import import_module

def override_wagtail_storages():
    """
    Forcefully overrides Wagtail's storage mechanism by directly patching
    the Image and Document models.
    """
    if not settings.USE_S3:
        print("S3 not enabled, not overriding storage.")
        return
    
    print("Overriding Wagtail storage backend...")
    
    try:
        # Import our MediaStorage
        storage_path = settings.DEFAULT_FILE_STORAGE
        module_name, class_name = storage_path.rsplit('.', 1)
        module = import_module(module_name)
        storage_class = getattr(module, class_name)()
        
        # Override Wagtail Image's storage
        from wagtail.images.models import AbstractImage
        AbstractImage.file.field.storage = storage_class
        print("✅ Successfully overrode AbstractImage.file.field.storage")
        
        # Override Wagtail Document's storage
        try:
            from wagtail.documents.models import AbstractDocument
            AbstractDocument.file.field.storage = storage_class
            print("✅ Successfully overrode AbstractDocument.file.field.storage")
        except (ImportError, AttributeError) as e:
            print(f"⚠️ Could not override document storage: {e}")
            
        print("Storage backend override complete.")
        
    except Exception as e:
        print(f"❌ Error overriding storage: {e}")
