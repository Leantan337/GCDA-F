from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator
from wagtail.models import Page
from .models import NewsPage, NewsCategory  # Added NewsCategory import

def news_list(request):
    """View to list all news articles with AJAX pagination."""
    news_items = NewsPage.objects.live().order_by('-first_published_at')
    paginator = Paginator(news_items, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # AJAX request: return only the news items HTML
        return render(request, 'news/includes/news_items.html', {
            'news_items': page_obj,
        })
    # Normal request: render full page
    return render(request, 'news/news_list.html', {
        'news_items': page_obj,
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
