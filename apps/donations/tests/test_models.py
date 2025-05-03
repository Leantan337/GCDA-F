from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from ..models import DonationCampaign, DonationPage

class DonationCampaignTest(TestCase):
    def setUp(self):
        self.campaign = DonationCampaign.objects.create(
            title="Test Campaign",
            description="Test Description",
            target_amount=1000.00,
            amount_raised=500.00
        )

    def test_campaign_progress_percentage(self):
        # Test progress calculation
        self.assertEqual(self.campaign.progress_percentage, 50)
        
        # Test with zero target amount
        with self.assertRaises(ValidationError):
            DonationCampaign.objects.create(
                title="Invalid Campaign",
                description="Test",
                target_amount=0,
                amount_raised=0
            )

    def test_campaign_remaining_amount(self):
        self.assertEqual(
            self.campaign.remaining_amount,
            Decimal('500.00')
        )

    def test_campaign_update_amount(self):
        self.campaign.add_donation(Decimal('250.00'))
        self.assertEqual(
            self.campaign.amount_raised,
            Decimal('750.00')
        )
        
        # Test exceeding target amount
        self.campaign.add_donation(Decimal('500.00'))
        self.assertEqual(
            self.campaign.amount_raised,
            Decimal('1250.00')
        )
        self.assertEqual(self.campaign.progress_percentage, 125)

class DonationPageTest(TestCase):
    def setUp(self):
        self.donation_page = DonationPage(
            title="Donate",
            description="Help us make a difference",
            thank_you_text="Thank you for your support"
        )

    def test_page_validation(self):
        # Test required fields
        with self.assertRaises(ValidationError):
            DonationPage(title="Donate").full_clean()

    def test_page_str_representation(self):
        self.assertEqual(
            str(self.donation_page),
            "Donate"
        )
