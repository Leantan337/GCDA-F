from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from wagtail.models import Page
from ..models import DonationPage, DonationCampaign

class DonationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a root page for the donation page
        self.root_page = Page.objects.get(id=1)
        
        # Create a donation page
        self.donation_page = DonationPage(
            title="Donate",
            description="Help us make a difference",
            thank_you_text="Thank you for your support"
        )
        self.root_page.add_child(instance=self.donation_page)
        
        # Create a test campaign
        self.campaign = DonationCampaign.objects.create(
            title="Test Campaign",
            description="Test Description",
            target_amount=1000.00,
            amount_raised=500.00
        )

    def test_donation_page_view(self):
        url = reverse('donations:donation_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/donation_page.html')
        self.assertContains(response, "Test Campaign")

    def test_campaign_list_view(self):
        url = reverse('donations:campaign_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/campaign_list.html')
        self.assertQuerysetEqual(
            response.context['campaigns'],
            [self.campaign],
            transform=lambda x: x
        )

    def test_campaign_detail_view(self):
        url = reverse('donations:campaign_detail', kwargs={'pk': self.campaign.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/campaign_detail.html')
        self.assertEqual(response.context['campaign'], self.campaign)

    def test_donation_process(self):
        url = reverse('donations:process_donation', kwargs={'campaign_id': self.campaign.pk})
        data = {
            'amount': '50.00',
            'payment_method': 'card',
            'email': 'donor@example.com',
            'name': 'Test Donor'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect to thank you page
        
        # Check if campaign amount is updated
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.amount_raised, 550.00)

    def test_thank_you_page(self):
        url = reverse('donations:thank_you')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/thank_you.html')
