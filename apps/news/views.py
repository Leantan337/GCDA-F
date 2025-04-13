from django.shortcuts import render
from django.http import Http404
from wagtail.models import Page
from .models import NewsPage, NewsCategory  # Added NewsCategory import

def news_list(request):
    """View to list all news articles."""
    news_items = NewsPage.objects.live().order_by('-first_published_at')
    return render(request, 'news/news_list.html', {
        'news_items': news_items,
    })

def news_detail(request, slug):
    """View to show a single news article."""
    news_item = NewsPage.objects.live().filter(slug=slug).first()
    if not news_item:
        raise Http404("Article not found")
    return render(request, 'news/news_page.html', {
        'page': news_item,
        'recent_posts': NewsPage.objects.live().order_by('-date')[:5],
        'categories': NewsCategory.objects.all()
    })
