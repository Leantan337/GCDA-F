import pytest
from django.test import TestCase
from wagtail.models import Page
from apps.core.models import HomePage, ServiceOrderable, TeamMemberOrderable

@pytest.mark.django_db
class TestHomePage(TestCase):
    def setUp(self):
        # Ensure a root page exists
        if not Page.objects.filter(depth=1).exists():
            self.root = Page.objects.create(title='Root', slug='root', path='0001', depth=1, numchild=1, url_path='/')
        else:
            self.root = Page.objects.get(depth=1)
        # Create a HomePage instance as child of root using add_child
        self.home = self.root.add_child(instance=HomePage(
            title='GCDA Home',
            slug='gcda-home',
            path='00010001',
            depth=2,
            url_path='/gcda-home/',
            mission_statement='Mission',
            hero_subtitle='Subtitle',
            hero_cta_text='CTA',
            hero_video_url='',
            about_title='About',
            about_subtitle='Subtitle',
            about_description='Description',
            about_content_secondary='',
            about_cta_text='',
            about_cta_link='',
            services_title='Services',
            services_subtitle='',
            services_description='',
            team_title='Team',
            team_subtitle='',
            team_description='',
            contact_title='Contact',
            contact_subtitle='',
            contact_description='',
            address='',
            email='',
            phone='',
            people_helped=0,
            countries_served=0,
            projects_completed=0,
            volunteers=0
        ))

    def test_home_page_creation(self):
        """Test that we can create a HomePage."""
        self.assertEqual(self.home.title, 'GCDA Home')
        self.assertEqual(self.home.slug, 'gcda-home')

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
            position='Director',
            bio='Experienced community leader',
            photo=None
        )
        self.assertEqual(team_member.name, 'John Doe')
        self.assertTrue(TeamMemberOrderable.objects.filter(page=self.home).exists())