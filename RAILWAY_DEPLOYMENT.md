# Railway Deployment Guide for GCDA

This guide will help you deploy your GCDA Django project to Railway.

## Prerequisites

- A Railway account (sign up at [railway.app](https://railway.app))
- Git repository with your GCDA project
- Railway CLI (optional, but helpful)

## Deployment Steps

### 1. Connect your repository to Railway

1. Log in to your Railway account
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your GCDA repository
4. Railway will automatically detect the Django project

### 2. Configure Environment Variables

Set the following environment variables in Railway dashboard:

- `SECRET_KEY` - A secure secret key for Django
- `DEBUG` - Set to 'False' for production
- `DJANGO_SETTINGS_MODULE` - Set to 'config.settings'
- `USE_S3` - Set to 'True' if using S3 for media storage (recommended)

If using S3 for media storage, add these as well:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_STORAGE_BUCKET_NAME`
- `AWS_S3_REGION_NAME`

### 3. Add a PostgreSQL Database

1. In your project dashboard, click "New" → "Database" → "PostgreSQL"
2. Railway will automatically create the database and provide the `DATABASE_URL` to your application

### 4. Deploy and Run Migrations

The first deployment will automatically run based on the `railway.json` configuration in your project, which:
- Installs dependencies
- Collects static files
- Starts the application with Gunicorn

After the first deployment, you'll need to run migrations:

1. Click on your web service
2. Go to "Settings" → "Shell"
3. Run: `python manage.py migrate`

### 5. Create a Superuser

Create a Django admin superuser:

1. In the Railway shell, run:
   ```
   python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'your-password')"
   ```
2. Replace 'your-password' with a secure password

### 6. Access Your Application

Your application will be available at the domain provided by Railway (shown in your project dashboard).

## Troubleshooting

If you encounter any issues:

1. Check the logs in the Railway dashboard
2. Verify your environment variables are set correctly
3. Ensure that database migrations have been applied
4. Check that static files are being served correctly

## Local Development

Continue using SQLite for local development. Railway will automatically use PostgreSQL in production via the DATABASE_URL environment variable.
