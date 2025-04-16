"""Script to fix database issues with NewsIndexPage model."""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import sqlite3
from django.db import connection

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Fix NewsIndexPage table
print("Examining news_newsindexpage table structure:")
cursor.execute("PRAGMA table_info(news_newsindexpage)")
columns = cursor.fetchall()
print("Existing columns:")
for column in columns:
    print(f"  - {column}")

# Check for header_image_id column and add it if it doesn't exist
header_image_id_exists = False
for column in columns:
    if column[1] == 'header_image_id':
        header_image_id_exists = True
        break

if not header_image_id_exists:
    print("Adding missing 'header_image_id' column to news_newsindexpage")
    cursor.execute("ALTER TABLE news_newsindexpage ADD COLUMN header_image_id INTEGER DEFAULT NULL REFERENCES wagtailimages_image(id)")

# Check if intro column exists and add it if it doesn't
intro_exists = False
for column in columns:
    if column[1] == 'intro':
        intro_exists = True
        break

if not intro_exists:
    print("Adding missing 'intro' column to news_newsindexpage")
    cursor.execute("ALTER TABLE news_newsindexpage ADD COLUMN intro VARCHAR(250) DEFAULT ''")

# Fix NewsCategory table
print("\nExamining news_newscategory table structure:")
cursor.execute("PRAGMA table_info(news_newscategory)")
category_columns = cursor.fetchall()
print("Existing columns:")
for column in category_columns:
    print(f"  - {column}")

# Check if description column exists in news_newscategory and add it if it doesn't
description_exists = False
for column in category_columns:
    if column[1] == 'description':
        description_exists = True
        break

if not description_exists:
    print("Adding missing 'description' column to news_newscategory")
    cursor.execute("ALTER TABLE news_newscategory ADD COLUMN description TEXT DEFAULT ''")

# Commit changes and close
conn.commit()
conn.close()

print("Database fixes applied successfully!")
print("Now marking migrations as applied...")

# Mark the migrations as applied using Django's migrations framework
cursor = connection.cursor()
cursor.execute(
    "INSERT OR IGNORE INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)",
    ['news', '0003_add_missing_newsindexpage_intro_field', django.utils.timezone.now()]
)
connection.commit()

print("All done! The database should be fixed now.")
