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
        
        MultiFieldPanel([
            FieldPanel('about_title'),
            FieldPanel('about_subtitle'),
            FieldPanel('about_description'),
            FieldPanel('about_content_secondary'),
            FieldPanel('about_cta_text'),
            FieldPanel('about_cta_link'),
        ], heading="About Section"),
        
        MultiFieldPanel([
            FieldPanel('services_title'),
            FieldPanel('services_subtitle'),
            FieldPanel('services_description'),
        ], heading="Services Section"),
        
        MultiFieldPanel([
            FieldPanel('team_title'),
            FieldPanel('team_subtitle'),
            FieldPanel('team_description'),
        ], heading="Team Section"),
        
        MultiFieldPanel([
            FieldPanel('contact_title'),
            FieldPanel('contact_subtitle'),
            FieldPanel('contact_description'),
            FieldPanel('address'),
            FieldPanel('email'),
            FieldPanel('phone'),
        ], heading="Contact Section"),
        
        InlinePanel('services', label="Services"),
        InlinePanel('team_members', label="Team Members"),
        InlinePanel('featured_programs', label="Featured Programs"),
    ]

    class Meta(Page.Meta):
        verbose_name = "Homepage"


class ServiceOrderable(Orderable):
    """Service item for the home page."""
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=100)
    description = RichTextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class name")

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('icon'),
    ]

    def __str__(self) -> str:
        return str(self.title)


class TeamMemberOrderable(Orderable):
    """Team member item for the home page."""
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = RichTextField()
    photo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('position'),
        FieldPanel('bio'),
        FieldPanel('photo'),
    ]

    def __str__(self) -> str:
        return str(self.name)


class FeaturedProgramOrderable(Orderable):
    """Featured program item for the home page."""
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='featured_programs')
    title = models.CharField(max_length=100)
    description = RichTextField()
    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    link = models.URLField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('image'),
        FieldPanel('link'),
    ]

    def __str__(self) -> str:
        return str(self.title)