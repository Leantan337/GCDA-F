"""
News and blog functionality for the website.
"""
from django import forms
from django.db import models
from django.utils import timezone
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images import get_image_model_string
from wagtail.search import index
from django.conf import settings
from wagtail.images.models import Image

class NewsCategory(models.Model):
    """Categories for news articles."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=80, unique=True)
    
    class Meta:
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"
        
    def __str__(self):
        return self.name

class NewsIndexPage(Page):
    """Container page for news articles."""
    introduction = RichTextField(
        blank=True,
        help_text='Text to describe this section'
    )

    content_panels = Page.content_panels + [
        FieldPanel('introduction')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        news_items = NewsPage.objects.child_of(self).live().order_by('-first_published_at')
        context['news_items'] = news_items
        return context

    class Meta:
        verbose_name = "News Index Page"
        verbose_name_plural = "News Index Pages"

class NewsPage(Page):
    """Individual news article page."""
    date = models.DateField("Post date", default=timezone.now)
    intro = models.CharField(max_length=250, help_text='Brief introduction')
    body = RichTextField()
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='news_articles'
    )
    categories = models.ManyToManyField(
        NewsCategory,
        blank=True,
        related_name='news_pages'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('author'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('featured_image'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
    ]

    class Meta:
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} ({self.date})"
