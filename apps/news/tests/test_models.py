import pytest
from django.contrib.auth import get_user_model
from wagtail.models import Page
from apps.news.models import NewsPage, NewsCategory, NewsIndexPage
from django.utils import timezone
import uuid

@pytest.mark.django_db
class TestNewsModels:
    def setup_method(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='newsuser', email='newsuser@example.com', password='pw')
        self.category = NewsCategory.objects.create(name='Events', slug=f'events-{uuid.uuid4().hex[:8]}')
        root = Page.get_first_root_node()
        self.index = root.add_child(instance=NewsIndexPage(title='News Index', slug=f'news-index-{uuid.uuid4().hex[:8]}'))
        self.news = self.index.add_child(instance=NewsPage(
            title='Sample News',
            slug=f'sample-news-{uuid.uuid4().hex[:8]}',
            intro='Test intro',
            body='Test body',
            author=self.user,
            date=timezone.now()
        ))
        self.news.categories.add(self.category)

    def test_str(self):
        assert str(self.news).startswith('Sample News')

    def test_category_str(self):
        assert str(self.category) == 'Events'

    def test_news_index_context(self, rf):
        request = rf.get('/')
        context = self.index.get_context(request)
        assert 'news_items' in context
        assert self.news in context['news_items']

    def test_news_ordering(self):
        news2 = self.index.add_child(instance=NewsPage(
            title='Older News',
            slug=f'older-news-{uuid.uuid4().hex[:8]}',
            intro='Old intro',
            body='Old body',
            author=self.user,
            date=timezone.now() - timezone.timedelta(days=1)
        ))
        items = list(NewsPage.objects.child_of(self.index).live().order_by('-date'))
        assert items[0].title == 'Sample News'
        assert items[1].title == 'Older News'
