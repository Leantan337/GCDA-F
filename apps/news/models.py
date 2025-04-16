"""News models for the NGO website."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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


class NewsIndexPage(Page):
    """Index page for news articles."""
    template = 'news/news_index.html'
    
    intro = models.CharField(max_length=250, blank=True)
    header_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('header_image'),
    ]
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get all live news pages that are children of this index page
        news_items = NewsPage.objects.live().descendant_of(self).order_by('-date')
        
        # Filter by category if the category parameter is in the request
        category_slug = request.GET.get('category')
        if category_slug:
            category = NewsCategory.objects.filter(slug=category_slug).first()
            if category:
                news_items = news_items.filter(categories__in=[category])
                context['current_category'] = category
        
        # Pagination
        paginator = Paginator(news_items, 6)  # Show 6 news items per page
        page = request.GET.get('page')
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        
        context['news_items'] = news
        context['categories'] = NewsCategory.objects.all()
        return context


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
    
    # Parent page / subpage type rules
    parent_page_types = ['news.NewsIndexPage']
    
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