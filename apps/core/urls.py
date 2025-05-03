"""
URL patterns for the core app.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact'),
    path('test/', views.test_page, name='test'),
]
