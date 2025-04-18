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

# Create static directory structure
echo "📁 Creating static directory structure..."
mkdir -p static/assets/{css,js,img}

# Create empty placeholder files to prevent WhiteNoise errors
echo "📄 Creating placeholder files..."
touch static/assets/img/testimonials-bg.jpg

# Collect static files
echo "📚 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Make start script executable
chmod +x start.sh

echo "✅ Build process completed successfully!"
