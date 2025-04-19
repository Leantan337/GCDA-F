import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from wagtail.models import Page
from apps.comments.models import Comment
import uuid

@pytest.mark.django_db
def test_add_comment_view(client, rf):
    User = get_user_model()
    user = User.objects.create_user(username='alice', email='alice@example.com', password='pw')
    root = Page.get_first_root_node()
    page = root.add_child(instance=Page(title='Content', slug=f'content-{uuid.uuid4().hex[:8]}'))
    client.force_login(user)
    url = reverse('comments:add_comment', args=[page.id])
    response = client.post(url, {"text": "A view test comment"}, HTTP_REFERER='/somewhere/')
    assert response.status_code == 302
    assert response.url == '/somewhere/'
    assert Comment.objects.filter(page=page, author=user, text="A view test comment").exists()
