from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    This migration is used to fix a state issue where the database tables already exist
    but Django's migration record doesn't know about them. It essentially does nothing
    except mark the migration as applied.
    """

    dependencies = [
        ('news', '0003_add_missing_newsindexpage_intro_field'),
    ]

    # This migration is intentionally empty, as it's just meant to reconcile
    # the migration state with the actual database state.
    operations = []
