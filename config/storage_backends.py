from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    Storage for user-uploaded media files.
    These will be properly stored in the S3 bucket.
    """
    location = 'media'  # Store files in the media/ directory in S3
    # Remove default_acl as it's not supported with the current bucket settings
    file_overwrite = False
