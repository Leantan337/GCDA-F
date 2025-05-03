"""
Models for user engagement tracking and management.
"""
from django.db import models
from django.conf import settings
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

class EngagementEvent(models.Model):
    class Meta:
        app_label = 'engagement'
    """Model to track user engagement events."""
    EVENT_TYPES = [
        ('view', 'Page View'),
        ('like', 'Like'),
        ('share', 'Share'),
        ('download', 'Download'),
        ('subscribe', 'Newsletter Subscribe'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='engagement_events',
        help_text='User who performed the action'
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        help_text='Type of engagement action'
    )
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='engagement_events',
        help_text='Page where the engagement occurred'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text='When the engagement occurred'
    )
    metadata = models.JSONField(
        null=True,
        blank=True,
        help_text='Additional event data in JSON format'
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Engagement Event"
        verbose_name_plural = "Engagement Events"
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['event_type']),
        ]

    def __str__(self):
        return f"{self.event_type} by {self.user} on {self.page}"

class NewsletterSubscription(models.Model):
    class Meta:
        app_label = 'engagement'
    """Newsletter subscription management."""
    email = models.EmailField(
        unique=True,
        help_text='Subscriber email address'
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='Subscriber name'
    )
    subscribed_at = models.DateTimeField(
        auto_now_add=True
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Whether the subscription is currently active'
    )
    preferences = models.JSONField(
        null=True,
        blank=True,
        help_text='Subscriber preferences in JSON format'
    )

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"

    def __str__(self):
        return f"Newsletter subscription for {self.email}"

    def unsubscribe(self):
        """Deactivate the subscription."""
        self.is_active = False
        self.save()