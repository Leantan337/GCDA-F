"""
Script to fix migration conflicts by marking problematic migrations as applied.
Used before running regular migrations to handle cases where the database schema
differs from the migration history.
"""

import os
import django
from django.db import connection

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def mark_migration_as_applied(app_name, migration_name):
    """Mark a specific migration as applied in the migration history table."""
    print(f"Marking migration {app_name}.{migration_name} as applied...")
    
    with connection.cursor() as cursor:
        # First check if the django_migrations table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'django_migrations'
            );
        """)
        if not cursor.fetchone()[0]:
            print("django_migrations table does not exist. Creating it first...")
            from django.core.management import call_command
            call_command('migrate', 'contenttypes', '0001', verbosity=1)
            return
        
        # Check if migration is already recorded
        cursor.execute(
            "SELECT COUNT(*) FROM django_migrations WHERE app = %s AND name = %s",
            [app_name, migration_name]
        )
        if cursor.fetchone()[0] > 0:
            print(f"Migration {app_name}.{migration_name} is already applied.")
            return
        
        # Insert the migration record
        cursor.execute(
            "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, NOW())",
            [app_name, migration_name]
        )
        print(f"Successfully marked {app_name}.{migration_name} as applied.")

if __name__ == "__main__":
    # Mark the problematic migration as applied
    mark_migration_as_applied('news', '0003_add_missing_newsindexpage_intro_field')
    
    print("Migration fix applied successfully. You can now run regular migrations.")
