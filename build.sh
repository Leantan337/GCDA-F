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

# Copy default image if testimonials-bg.jpg is missing
echo "🖼️ Setting up default images..."
if [ ! -f static/assets/img/testimonials-bg.jpg ]; then
    echo "⚠️ testimonials-bg.jpg not found, using placeholder..."
    cp static/assets/img/default-bg.jpg static/assets/img/testimonials-bg.jpg || true
fi

# Collect static files with ignore errors
echo "📚 Collecting static files..."
python manage.py collectstatic --noinput --ignore-patterns="*.scss" --clear

# Make start script executable
chmod +x start.sh

echo "✅ Build process completed successfully!"
