import pytest
from django.contrib.auth import get_user_model
from wagtail.models import Page
from apps.comments.models import Comment
from django.utils import timezone
import uuid

@pytest.mark.django_db
class TestCommentModel:
    def setup_method(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='bob', email='bob@example.com', password='pw')
        self.approver = User.objects.create_user(username='approver', email='approver@example.com', password='pw')
        root = Page.get_first_root_node()
        self.page = root.add_child(instance=Page(title='Content', slug=f'content-{uuid.uuid4().hex[:8]}'))
        self.comment = Comment.objects.create(
            page=self.page,
            author=self.user,
            text='A test comment',
            is_approved=False
        )

    def test_str(self):
        assert str(self.comment) == f"Comment by {self.user} on {self.page}"

    def test_approve(self):
        self.comment.approve(user=self.approver)
        self.comment.refresh_from_db()
        assert self.comment.is_approved is True
        assert self.comment.approved_by == self.approver
        assert self.comment.approved_at is not None
        assert abs((timezone.now() - self.comment.approved_at).total_seconds()) < 5

    def test_track_submission(self, rf):
        request = rf.post('/')
        request.META['REMOTE_ADDR'] = '1.2.3.4'
        request.META['HTTP_USER_AGENT'] = 'pytest-agent'
        self.comment.track_submission(request)
        self.comment.refresh_from_db()
        assert self.comment.ip_address == '1.2.3.4'
        assert self.comment.user_agent == 'pytest-agent'
