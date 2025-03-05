"""
Common imports and base classes for models
"""
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultipleChooserPanel

class BasePage(Page):
    """Base page class with common functionality"""
    description = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]

    class Meta:
        abstract = True 