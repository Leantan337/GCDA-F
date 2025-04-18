#!/bin/bash
set -e  # Exit on error

echo "🚀 Starting build process..."

# Create necessary directories in the persistent volume
echo "📁 Setting up persistent storage directories..."
mkdir -p /media/staticfiles
mkdir -p /media/uploads
chmod -R 755 /media

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📚 Collecting static files..."
python manage.py collectstatic --noinput

# Optional: Try to compress static files, but don't fail if it errors
echo "🗜️ Attempting to compress static files..."
python manage.py compress --force || echo "⚠️ Compression skipped - no compress tags found (this is okay)"

# Make start script executable
chmod +x start.sh

echo "✅ Build process completed successfully!"
