"""
Core views for the NGO website.
"""
from django.shortcuts import render

def index(request):
    """
    View for the homepage.
    """
    return render(request, 'index.html')

# Create your views here.
