import pytest
from django.test import TestCase
from wagtail.models import Page
from wagtail.test.utils.form_data import nested_form_data, rich_text

from apps.core.models import HomePage, ServiceOrderable, TeamMemberOrderable

pytest.mark.django_db

class TestHomePage(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=1)
        self.home = HomePage(title='GCDA Home', intro='Welcome to GCDA')
        self.root_page.add_child(instance=self.home)

    def test_home_page_creation(self):
        """Test that we can create a HomePage."""
        self.assertEqual(self.home.title, 'GCDA Home')
        self.assertEqual(self.home.intro, 'Welcome to GCDA')

    def test_can_create_service(self):
        """Test that we can create a service."""
        service = ServiceOrderable.objects.create(
            page=self.home,
            title='Community Development',
            description='Supporting local communities',
            icon='users'
        )
        self.assertEqual(service.title, 'Community Development')
        self.assertTrue(ServiceOrderable.objects.filter(page=self.home).exists())

    def test_can_create_team_member(self):
        """Test that we can create a team member."""
        team_member = TeamMemberOrderable.objects.create(
            page=self.home,
            name='John Doe',
            role='Director',
            bio='Experienced community leader'
        )
        self.assertEqual(team_member.name, 'John Doe')
        self.assertTrue(TeamMemberOrderable.objects.filter(page=self.home).exists())

    def test_home_page_parent_page_types(self):
        """Test that HomePage can only be created under Root page."""
        self.assertEqual(HomePage.parent_page_types, [])

    def test_home_page_subpage_types(self):
        """Test that HomePage allows appropriate subpage types."""
        self.assertEqual(HomePage.subpage_types, ['news.NewsIndexPage', 'donations.DonationPage'])

    def test_home_page_get_context(self):
        """Test that get_context adds appropriate data."""
        context = self.home.get_context({})
        self.assertIn('services', context)
        self.assertIn('team_members', context)
        self.assertIn('featured_programs', context)