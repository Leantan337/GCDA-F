"""
Core views for the NGO website.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from apps.news.models import NewsPage

def index(request):
    """
    View for the homepage.
    """
    # Get latest news items for the homepage
    try:
        latest_news = NewsPage.objects.live().order_by('-first_published_at')[:3]
    except:
        latest_news = []
        
    context = {
        'latest_news': latest_news,
    }
    return render(request, 'core/home.html', context)

def contact(request):
    """
    View for handling contact form submissions.
    """
    if request.method == 'POST':
        # Process the form submission
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # Here you would typically save to database or send an email
        # For now, just return a success message
        
        messages.success(request, 'Your message has been sent successfully!')
        return redirect(reverse('core:home'))
        
    # If not POST, redirect to home with contact section
    return redirect(reverse('core:home') + '#contact')

def test_page(request):
    """
    Simple test page to verify development server configuration.
    """
    return render(request, 'test.html')
