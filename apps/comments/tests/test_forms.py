import pytest
from apps.comments.forms import CommentForm

@pytest.mark.django_db
def test_comment_form_valid():
    form = CommentForm(data={"text": "Nice post!"})
    assert form.is_valid()

@pytest.mark.django_db
def test_comment_form_invalid():
    form = CommentForm(data={"text": ""})
    assert not form.is_valid()
    assert "text" in form.errors
