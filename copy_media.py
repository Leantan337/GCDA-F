#!/usr/bin/env python
"""
Utility script to copy media files to the staticfiles directory.
This ensures media files are accessible in production.
"""

import os
import shutil
from pathlib import Path

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent

# Source and destination paths
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_MEDIA_DIR = os.path.join(STATIC_ROOT, 'media')

def ensure_directory_exists(directory):
    """Make sure a directory exists, create it if it doesn't."""
    if not os.path.exists(directory):
        print(f"Creating directory: {directory}")
        os.makedirs(directory, exist_ok=True)

def copy_media_files():
    """Copy all media files to the staticfiles/media directory."""
    ensure_directory_exists(MEDIA_ROOT)
    ensure_directory_exists(STATIC_ROOT)
    ensure_directory_exists(STATIC_MEDIA_DIR)
    
    print(f"Copying media files from {MEDIA_ROOT} to {STATIC_MEDIA_DIR}")
    
    # Copy all files from media to staticfiles/media
    for root, dirs, files in os.walk(MEDIA_ROOT):
        relative_path = os.path.relpath(root, MEDIA_ROOT)
        static_path = os.path.join(STATIC_MEDIA_DIR, relative_path) if relative_path != '.' else STATIC_MEDIA_DIR
        
        # Create directories in the destination
        ensure_directory_exists(static_path)
        
        # Copy files
        for file in files:
            source_file = os.path.join(root, file)
            dest_file = os.path.join(static_path, file)
            print(f"Copying: {source_file} -> {dest_file}")
            shutil.copy2(source_file, dest_file)
    
    print("Media files copied successfully!")
    print("Setting permissions...")
    # Set permissions for the media directory
    for root, dirs, files in os.walk(STATIC_MEDIA_DIR):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o755)
        for f in files:
            os.chmod(os.path.join(root, f), 0o644)
    
    print("Permissions set successfully!")

if __name__ == "__main__":
    copy_media_files() 