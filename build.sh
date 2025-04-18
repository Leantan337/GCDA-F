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

# Create static directory if it doesn't exist
echo "📁 Creating static directory..."
mkdir -p static/assets/img

# Create a simple placeholder image if needed
echo "🖼️ Setting up default images..."
if [ ! -f static/assets/img/testimonials-bg.jpg ]; then
    echo "⚠️ Creating empty placeholder image..."
    convert -size 1920x1080 xc:gray static/assets/img/testimonials-bg.jpg || true
fi

# Collect static files
echo "📚 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Make start script executable
chmod +x start.sh

echo "✅ Build process completed successfully!"
