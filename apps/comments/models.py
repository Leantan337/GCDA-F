"""
Models for handling comments and user interactions.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from wagtail.models import Page

class Comment(models.Model):
    """Model for user comments on pages."""
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The page this comment belongs to"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="User who wrote the comment"
    )
    text = models.TextField(
        help_text="Comment content"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    is_approved = models.BooleanField(
        default=models.NOT_PROVIDED,
        help_text="Whether the comment is approved and visible"
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_comments'
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )
    user_agent = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_approved']),
        ]

    def __str__(self) -> str:
        return str(f"Comment by {self.author} on {self.page}")

    def approve(self, user=None):
        """Approve the comment with tracking information."""
        self.is_approved = True
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save()

    def track_submission(self, request):
        """Track comment submission details."""
        self.ip_address = request.META.get('REMOTE_ADDR')
        self.user_agent = request.META.get('HTTP_USER_AGENT', '')
        self.save()