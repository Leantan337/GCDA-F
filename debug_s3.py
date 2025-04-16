"""
Script to debug S3 configuration issues.
Run this in production to verify settings.
"""

import os
import django
import boto3
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def debug_s3_configuration():
    """Print out all S3-related configuration to debug issues."""
    print("=== S3 Configuration Debugging ===")
    
    # Check environment settings
    print("\n-- Environment Variables --")
    print(f"USE_S3 = {os.environ.get('USE_S3', 'Not set')}")
    print(f"AWS_ACCESS_KEY_ID exists: {bool(os.environ.get('AWS_ACCESS_KEY_ID', ''))}")
    print(f"AWS_SECRET_ACCESS_KEY exists: {bool(os.environ.get('AWS_SECRET_ACCESS_KEY', ''))}")
    print(f"AWS_STORAGE_BUCKET_NAME: {os.environ.get('AWS_STORAGE_BUCKET_NAME', 'Not set')}")
    print(f"AWS_S3_REGION_NAME: {os.environ.get('AWS_S3_REGION_NAME', 'Not set')}")
    
    # Check Django settings
    print("\n-- Django Settings --")
    print(f"settings.USE_S3 = {getattr(settings, 'USE_S3', False)}")
    print(f"DEFAULT_FILE_STORAGE = {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}")
    print(f"MEDIA_URL = {getattr(settings, 'MEDIA_URL', 'Not set')}")
    
    # Check Wagtail-specific settings
    print("\n-- Wagtail Settings --")
    print(f"WAGTAILIMAGES_STORAGE = {getattr(settings, 'WAGTAILIMAGES_STORAGE', 'Not set')}")
    print(f"WAGTAILDOCS_STORAGE = {getattr(settings, 'WAGTAILDOCS_STORAGE', 'Not set')}")
    
    # Try to actually connect to S3
    print("\n-- S3 Connection Test --")
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''),
            region_name=os.environ.get('AWS_S3_REGION_NAME', 'eu-north-1')
        )
        
        # List buckets to verify credentials
        response = s3.list_buckets()
        print(f"Successfully connected to S3")
        print(f"Available buckets: {[bucket['Name'] for bucket in response['Buckets']]}")
        
        # Check if our target bucket exists
        bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
        if bucket_name in [bucket['Name'] for bucket in response['Buckets']]:
            print(f"Target bucket '{bucket_name}' found")
            
            # List some recent objects in the bucket
            response = s3.list_objects_v2(
                Bucket=bucket_name,
                MaxKeys=5
            )
            
            if 'Contents' in response:
                print(f"Recent objects in bucket:")
                for obj in response['Contents']:
                    print(f"  {obj['Key']} (modified: {obj['LastModified']})")
            else:
                print(f"Bucket is empty or you don't have permission to list objects")
        else:
            print(f"Target bucket '{bucket_name}' NOT FOUND among available buckets")
    
    except Exception as e:
        print(f"Error connecting to S3: {str(e)}")
    
    # Print import paths to debug possible module issues
    print("\n-- Import Paths --")
    import sys
    print(f"Python path: {sys.path}")

if __name__ == "__main__":
    debug_s3_configuration()
