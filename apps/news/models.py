"""News models for the NGO website."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.images import get_image_model_string
from wagtail.search import index


class NewsCategory(models.Model):
    """Category for news articles."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
    ]
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"


class NewsPage(Page):
    """News article page model."""
    template = 'news/news_page.html'
    
    # News fields
    date = models.DateField(_('Post date'))
    intro = models.CharField(max_length=250)
    body = RichTextField()
    categories = ParentalManyToManyField('news.NewsCategory', blank=True)
    
    # Featured image
    featured_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.FilterField('date'),
    ]
    
    # Content panels for the admin
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="News article metadata"),
        FieldPanel('intro'),
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['recent_posts'] = NewsPage.objects.live().exclude(id=self.id).order_by('-date')[:5]
        context['categories'] = NewsCategory.objects.all()
        return context