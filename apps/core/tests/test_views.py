import pytest
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.messages import get_messages
from apps.core.models import HomePage
from wagtail.models import Page
from apps.news.models import NewsPage
import uuid

@pytest.mark.django_db
class TestCoreViews(TestCase):
    def setUp(self):
        self.client = Client()
        # Ensure a root page exists
        if not Page.objects.filter(depth=1).exists():
            self.root = Page.objects.create(title='Root', slug='root', path='0001', depth=1, numchild=1, url_path='/')
        else:
            self.root = Page.objects.get(depth=1)
        # Use a unique slug for HomePage to avoid collision
        unique_slug = f'home-{uuid.uuid4().hex[:8]}'
        self.home = self.root.add_child(instance=HomePage(
            title='Home',
            slug=unique_slug,
            path='00010001',
            depth=2,
            url_path=f'/{unique_slug}/',
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
        # Create a NewsPage for testing index view
        self.news_page = self.home.add_child(instance=NewsPage(
            title="Test News",
            slug=f"test-news-{uuid.uuid4().hex[:8]}",
            intro="Intro text",
            body="Body text"
        ))

    def test_index_view_renders(self):
        url = reverse('core:home')
        response = self.client.get(url)
        assert response.status_code == 200
        assert 'latest_news' in response.context
        assert any(news.title == "Test News" for news in response.context["latest_news"])

    def test_contact_view_get_redirects(self):
        url = reverse('core:contact')
        response = self.client.get(url)
        assert response.status_code == 302
        assert response.url.endswith('#contact')

    def test_contact_view_post_success(self):
        url = reverse('core:contact')
        data = {
            'name': 'Alice',
            'email': 'alice@example.com',
            'subject': 'Help',
            'message': 'I want to volunteer.'
        }
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200
        messages = list(get_messages(response.wsgi_request))
        assert any('successfully' in m.message for m in messages)
        assert response.redirect_chain[-1][0].endswith(reverse('core:home'))
