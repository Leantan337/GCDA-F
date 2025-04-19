import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from wagtail.models import Page
from apps.news.models import NewsPage, NewsIndexPage, NewsCategory
from django.utils import timezone
import uuid

@pytest.mark.django_db
def test_news_list_view(client):
    User = get_user_model()
    user = User.objects.create_user(username='newsuser', email='newsuser@example.com', password='pw')
    root = Page.get_first_root_node()
    index = root.add_child(instance=NewsIndexPage(title='News Index', slug=f'news-index-{uuid.uuid4().hex[:8]}'))
    news = index.add_child(instance=NewsPage(
        title='Sample News',
        slug=f'sample-news-{uuid.uuid4().hex[:8]}',
        intro='Test intro',
        body='Test body',
        author=user,
        date=timezone.now()
    ))
    url = reverse('news:news_list')
    response = client.get(url)
    assert response.status_code == 200
    assert b'Sample News' in response.content

@pytest.mark.django_db
def test_news_detail_view(client):
    User = get_user_model()
    user = User.objects.create_user(username='newsuser', email='newsuser@example.com', password='pw')
    root = Page.get_first_root_node()
    index = root.add_child(instance=NewsIndexPage(title='News Index', slug=f'news-index-{uuid.uuid4().hex[:8]}'))
    news = index.add_child(instance=NewsPage(
        title='Sample News',
        slug=f'sample-news-{uuid.uuid4().hex[:8]}',
        intro='Test intro',
        body='Test body',
        author=user,
        date=timezone.now()
    ))
    url = reverse('news:news_detail', args=[news.slug])
    response = client.get(url)
    assert response.status_code == 200
    assert b'Sample News' in response.content
