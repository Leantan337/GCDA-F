from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import wagtail.images.models
from wagtail.search.index import Indexed
from wagtail.models import Collection


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('wagtailcore', '0083_workflowcontenttype'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.images.models.get_upload_to, verbose_name='file', width_field='width')),
                ('width', models.IntegerField(editable=False, verbose_name='width')),
                ('height', models.IntegerField(editable=False, verbose_name='height')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('focal_point_x', models.IntegerField(blank=True, null=True)),
                ('focal_point_y', models.IntegerField(blank=True, null=True)),
                ('focal_point_width', models.IntegerField(blank=True, null=True)),
                ('focal_point_height', models.IntegerField(blank=True, null=True)),
                ('file_size', models.PositiveIntegerField(editable=False, null=True)),
                ('collection', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.collection', verbose_name='collection')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text=None, through='taggit.TaggedItem', to='taggit.Tag', verbose_name='tags')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'abstract': False,
            },
            bases=(Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='CustomRendition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_spec', models.CharField(db_index=True, max_length=255)),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.images.models.get_rendition_upload_to, width_field='width')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(blank=True, default='', editable=False, max_length=16)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renditions', to='core.customimage')),
            ],
            options={
                'unique_together': {('image', 'filter_spec', 'focal_point_key')},
                'abstract': False,
            },
        ),
    ]
