import pytest
from django.contrib.auth import get_user_model
from wagtail.models import Page
from apps.engagement.models import EngagementEvent, NewsletterSubscription
import uuid
from django.utils import timezone

@pytest.mark.django_db
class TestEngagementModels:
    def setup_method(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='engager', email='engager@example.com', password='pw')
        root = Page.get_first_root_node()
        self.page = root.add_child(instance=Page(title='Engagement Page', slug=f'engage-{uuid.uuid4().hex[:8]}'))

    def test_engagement_event_creation(self):
        event = EngagementEvent.objects.create(
            user=self.user,
            event_type='view',
            page=self.page,
            metadata={'foo': 'bar'}
        )
        assert str(event) == f"view by {self.user} on {self.page}"
        assert event.metadata['foo'] == 'bar'

    def test_event_types(self):
        types = dict(EngagementEvent.EVENT_TYPES)
        assert 'view' in types and 'like' in types

    def test_newsletter_subscription(self):
        ns = NewsletterSubscription.objects.create(
            email=f"test-{uuid.uuid4().hex[:8]}@example.com",
            name="Test User",
            preferences={"weekly": True}
        )
        assert str(ns).startswith("Newsletter subscription for test-")
        assert ns.is_active
        ns.unsubscribe()
        ns.refresh_from_db()
        assert not ns.is_active
        assert ns.preferences["weekly"] is True
