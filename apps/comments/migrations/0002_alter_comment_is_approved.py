# Generated by Django 4.2.20 on 2025-04-19 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='is_approved',
            field=models.BooleanField(default=False, help_text='Whether the comment is approved and visible'),
        ),
    ]
