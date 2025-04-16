from django.db import models
from wagtail.images.models import AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    """Custom image model that stores renditions in the database."""
    admin_form_fields = (
        'title',
        'file',
        'collection',
        'tags',
        'focal_point_x',
        'focal_point_y',
        'focal_point_width',
        'focal_point_height',
    )

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class CustomRendition(AbstractRendition):
    """Custom rendition model that stores image renditions in the database."""
    image = models.ForeignKey(
        'CustomImage',
        on_delete=models.CASCADE,
        related_name='renditions'
    )

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
