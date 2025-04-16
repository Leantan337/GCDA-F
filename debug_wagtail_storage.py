"""
Deep debugging of Wagtail image storage configuration.
Tests the actual storage paths used by Wagtail images to ensure they're using S3.
"""

import os
import sys
import django
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import io
from PIL import Image

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def debug_wagtail_storage_system():
    """Deeply inspect Wagtail's storage configuration and test actual file storage."""
    
    print("\n=== WAGTAIL STORAGE DEBUGGING ===")
    
    # First check if Wagtail is installed and configured properly
    try:
        from wagtail.images.models import Image as WagtailImage
        print("✅ Wagtail Image model is available.")
    except ImportError:
        print("❌ Wagtail Image model could not be imported!")
        return
    
    # Check actual storage backend for Wagtail images
    try:
        # Get an instance of the storage class
        image_storage = WagtailImage.objects.first()
        if image_storage:
            print(f"\n-- Found Existing Image --")
            print(f"Title: {image_storage.title}")
            print(f"Storage class: {image_storage.file.storage.__class__.__name__}")
            print(f"Storage location: {image_storage.file.name}")
            if hasattr(image_storage.file.storage, 'bucket_name'):
                print(f"S3 Bucket: {image_storage.file.storage.bucket_name}")
            try:
                print(f"Image URL: {image_storage.file.url}")
            except Exception as e:
                print(f"Error getting image URL: {str(e)}")
        else:
            print("No existing images found in database.")
    except Exception as e:
        print(f"Error examining existing images: {str(e)}")
    
    # Analyze Wagtail settings
    print("\n-- Wagtail Storage Settings --")
    print(f"WAGTAIL_SITE_NAME: {getattr(settings, 'WAGTAIL_SITE_NAME', 'Not set')}")
    print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}")
    print(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'Not set')}")
    print(f"MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'Not set')}")
    print(f"WAGTAILIMAGES_STORAGE: {getattr(settings, 'WAGTAILIMAGES_STORAGE', 'DEFAULT_FILE_STORAGE will be used')}")
    print(f"WAGTAILIMAGES_IMAGE_MODEL: {getattr(settings, 'WAGTAILIMAGES_IMAGE_MODEL', 'Default model will be used')}")
    
    # Check if USE_S3 is actually True in Django settings (not just env var)
    print(f"\nUSE_S3 in Django settings: {getattr(settings, 'USE_S3', False)}")
    
    # Get storage class
    print(f"\n-- Default Storage Analysis --")
    print(f"Default Storage Class: {default_storage.__class__.__name__}")
    print(f"Default Storage Module: {default_storage.__class__.__module__}")
    
    if hasattr(default_storage, 'location'):
        print(f"Storage location: {default_storage.location}")
    if hasattr(default_storage, 'bucket_name'):
        print(f"Storage S3 bucket name: {default_storage.bucket_name}")
    
    # Attempt to create a file with the default storage
    print("\n-- Test Upload with Default Storage --")
    try:
        # Create a small test image
        print("Creating test image...")
        image = Image.new('RGB', (100, 100), color='red')
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Upload to default storage
        test_path = 'media/test_debug_image.jpg'
        print(f"Uploading test image to: {test_path}")
        path = default_storage.save(test_path, ContentFile(img_io.read()))
        print(f"File saved to: {path}")
        
        # Try to get the URL
        try:
            url = default_storage.url(path)
            print(f"File URL: {url}")
        except Exception as e:
            print(f"Error getting URL: {str(e)}")
        
        print("✅ Test upload succeeded")
    except Exception as e:
        print(f"❌ Test upload failed: {str(e)}")
    
    # Special check for Django Storage Backends
    try:
        storage_class = getattr(settings, 'DEFAULT_FILE_STORAGE', '')
        print(f"\n-- Import Analysis of {storage_class} --")
        
        parts = storage_class.split('.')
        module_name = '.'.join(parts[:-1])
        class_name = parts[-1]
        
        try:
            print(f"Attempting to import {module_name}...")
            module = __import__(module_name, fromlist=[class_name])
            print(f"Module imported successfully.")
            
            cls = getattr(module, class_name)
            print(f"Class {class_name} found in module.")
            
            # Check any special attributes of the MediaStorage class
            print(f"Class attributes:")
            for attr in dir(cls):
                if not attr.startswith('__') and not callable(getattr(cls, attr)):
                    try:
                        value = getattr(cls, attr)
                        print(f"  {attr}: {value}")
                    except Exception:
                        print(f"  {attr}: <error retrieving value>")
        except ImportError:
            print(f"Failed to import {module_name}")
        except AttributeError:
            print(f"Failed to find class {class_name} in {module_name}")
    except Exception as e:
        print(f"Error in import analysis: {str(e)}")
    
    # Print any known Wagtail image storage issues
    print("\n-- Known Wagtail Storage Issues --")
    if not getattr(settings, 'USE_S3', False):
        print("❌ USE_S3 setting is False or not defined!")
    
    if hasattr(default_storage, 'base_location'):
        if default_storage.base_location != 'media':
            print(f"⚠️ Warning: Storage base_location is {default_storage.base_location}, not 'media'")
    
    print("\nDebugging complete. Review the output above for clues about storage issues.")

if __name__ == "__main__":
    debug_wagtail_storage_system()
