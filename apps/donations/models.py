"""
Models for handling donations and campaigns.
"""
from django.db import models
from django.conf import settings
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.core.validators import MinValueValidator
from django.utils import timezone

class DonationPage(Page):
    """Page for accepting donations."""
    description = RichTextField(
        help_text="Main content for the donation page"
    )
    thank_you_text = RichTextField(
        help_text="Text shown after successful donation"
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('thank_you_text'),
    ]

    class Meta(Page.Meta):
        verbose_name = "Donation Page"
        verbose_name_plural = "Donation Pages"

class DonationCampaign(models.Model):
    """A specific donation campaign."""
    title = models.CharField(max_length=200)
    description = RichTextField()
    goal_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    current_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)]
    )
    start_date = models.DateField()
    end_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def __str__(self) -> str:
        return str(self.title)

    def get_progress_percentage(self):
        """Calculate campaign progress as percentage."""
        if self.goal_amount <= 0:
            return 0
        return float(self.current_amount) / float(self.goal_amount) * 100

class Donation(models.Model):
    """Individual donation record."""
    PAYMENT_METHODS = [
        ('card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
    ]

    DONATION_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    campaign = models.ForeignKey(
        DonationCampaign,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donations'
    )
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donations'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='card')
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    donation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=DONATION_STATUS,
        default='pending'
    )

    class Meta:
        ordering = ['-donation_date']
        verbose_name = "Donation"
        verbose_name_plural = "Donations"

    def __str__(self) -> str:
        return str(f"Donation of {self.amount} by {self.donor or 'Anonymous'}")

    def save(self, *args, **kwargs):
        """Update campaign amount on successful donation."""
        if self.status == 'completed' and self.campaign:
            self.campaign.current_amount += self.amount
            self.campaign.save()
        super().save(*args, **kwargs)