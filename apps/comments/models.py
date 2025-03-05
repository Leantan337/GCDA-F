"""
Models for handling comments and user interactions.
"""
from django.db import models
from django.conf import settings
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
        default=False,
        help_text="Whether the comment is approved and visible"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_approved']),
        ]

    def __str__(self):
        return f"Comment by {self.author} on {self.page}"

    def approve(self):
        """Approve the comment."""
        self.is_approved = True
        self.save()