from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_newsindexpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsindexpage',
            name='intro',
            field=models.CharField(blank=True, max_length=250, default=''),
            preserve_default=False,
        ),
    ]
