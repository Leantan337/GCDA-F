"""
Test script to directly upload a test file to S3 bucket.
This bypasses Django/Wagtail to verify if S3 credentials and bucket access work.
"""

import os
import sys
import django
import boto3
from io import BytesIO

# Setup Django to access settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_direct_s3_upload():
    """Attempt to directly upload a test file to S3 to verify credentials."""
    print("=== Testing Direct S3 Upload ===")

    # Get S3 configuration from environment
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID', '')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
    region_name = os.environ.get('AWS_S3_REGION_NAME', 'eu-north-1')
    
    # Validate we have the necessary credentials
    if not aws_access_key or not aws_secret_key or not bucket_name:
        print("ERROR: Missing required S3 credentials in environment variables")
        print(f"AWS_ACCESS_KEY_ID exists: {bool(aws_access_key)}")
        print(f"AWS_SECRET_ACCESS_KEY exists: {bool(aws_secret_key)}")
        print(f"AWS_STORAGE_BUCKET_NAME: {bucket_name}")
        return False
        
    print(f"Using bucket: {bucket_name} in region: {region_name}")
    
    try:
        # Create S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )
        
        # Create a test file in memory
        test_content = BytesIO(b"This is a test file to verify S3 uploads.")
        test_key = 'media/test_upload.txt'
        
        # Upload the file
        print(f"Attempting to upload test file to s3://{bucket_name}/{test_key}")
        s3.upload_fileobj(
            test_content, 
            bucket_name, 
            test_key,
            ExtraArgs={'ACL': 'public-read', 'ContentType': 'text/plain'}
        )
        
        # Verify the upload was successful by generating a URL and checking existence
        object_url = f"https://{bucket_name}.s3.amazonaws.com/{test_key}"
        print(f"Upload successful! Test file should be available at: {object_url}")
        
        # List the media directory to verify
        print("\nListing contents of media/ directory in bucket:")
        response = s3.list_objects_v2(
            Bucket=bucket_name,
            Prefix='media/',
            MaxKeys=10
        )
        
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"  {obj['Key']} (size: {obj['Size']} bytes)")
        else:
            print("No objects found in media/ directory")
            
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to upload to S3: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_direct_s3_upload()
    sys.exit(0 if success else 1)
