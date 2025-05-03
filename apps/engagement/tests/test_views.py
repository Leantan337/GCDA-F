from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from ..models import NewsletterSubscription, EngagementEvent

class EngagementViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a test subscription
        self.subscription = NewsletterSubscription.objects.create(
            email='subscriber@example.com',
            name='Test Subscriber',
            subscribed=True
        )

    def test_newsletter_subscribe(self):
        url = reverse('engagement:newsletter_subscribe')
        data = {
            'email': 'new@example.com',
            'name': 'New Subscriber'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful subscription
        
        # Check if subscription was created
        self.assertTrue(
            NewsletterSubscription.objects.filter(
                email='new@example.com',
                subscribed=True
            ).exists()
        )
        
        # Check if confirmation email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], 'new@example.com')

    def test_newsletter_unsubscribe(self):
        url = reverse('engagement:newsletter_unsubscribe', kwargs={'email': self.subscription.email})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after unsubscribe
        
        # Check if subscription was updated
        self.subscription.refresh_from_db()
        self.assertFalse(self.subscription.subscribed)

    def test_track_engagement(self):
        self.client.force_login(self.user)
        url = reverse('engagement:track_event')
        data = {
            'event_type': 'view',
            'page_id': '1',
            'content_type': 'page',
            'object_id': '1',
            'metadata': '{"path": "/", "title": "Home"}'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        # Check if event was created
        self.assertTrue(
            EngagementEvent.objects.filter(
                user=self.user,
                event_type='view'
            ).exists()
        )

    def test_unsubscribe_page_view(self):
        url = reverse('engagement:unsubscribe', kwargs={'email': self.subscription.email})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'engagement/unsubscribe.html')
        self.assertEqual(response.context['email'], self.subscription.email)

    def test_invalid_unsubscribe_email(self):
        url = reverse('engagement:unsubscribe', kwargs={'email': 'nonexistent@example.com'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
