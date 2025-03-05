from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from wagtail.models import Page

@login_required
def add_comment(request, page_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.page = Page.objects.get(id=page_id)
            comment.save()
    return redirect(request.META.get('HTTP_REFERER', '/')) 