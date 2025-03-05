"""
Core models for the NGO website.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.images import get_image_model_string

class HomePage(Page):
    """Home page model."""
    template = 'home/home_page.html'
    
    # Hero Section
    mission_statement = RichTextField(blank=True)
    hero_subtitle = RichTextField(blank=True)
    hero_cta_text = models.CharField(max_length=50, blank=True)
    hero_video_url = models.URLField(blank=True)
    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # About Section
    about_title = models.CharField(max_length=100, blank=True)
    about_subtitle = models.CharField(max_length=100, blank=True)
    about_description = RichTextField(blank=True)
    about_content_secondary = RichTextField(blank=True)
    about_cta_text = models.CharField(max_length=50, blank=True)
    about_cta_link = models.URLField(blank=True)

    # Services Section
    services_title = models.CharField(max_length=100, blank=True)
    services_subtitle = models.CharField(max_length=100, blank=True)
    services_description = RichTextField(blank=True)

    # Team Section
    team_title = models.CharField(max_length=100, blank=True)
    team_subtitle = models.CharField(max_length=100, blank=True)
    team_description = RichTextField(blank=True)

    # Contact Section
    contact_title = models.CharField(max_length=100, blank=True)
    contact_subtitle = models.CharField(max_length=100, blank=True)
    contact_description = RichTextField(blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Stats
    people_helped = models.IntegerField(default=0)
    countries_served = models.IntegerField(default=0)
    projects_completed = models.IntegerField(default=0)
    volunteers = models.IntegerField(default=0)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('mission_statement'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_cta_text'),
            FieldPanel('hero_video_url'),
            FieldPanel('hero_image'),
        ], heading="Hero Section"),

        InlinePanel('services', label="Services"),
        InlinePanel('team_members', label="Team Members"),
        InlinePanel('featured_programs', label="Featured Programs"),
    ]

    class Meta:
        verbose_name = "Homepage"

# Keep the related Orderable models in the same file