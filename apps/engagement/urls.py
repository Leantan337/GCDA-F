"""
URL configuration for engagement app.
"""
from django.urls import path
from . import views

app_name = 'engagement'

urlpatterns = [
    path('subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('unsubscribe/<str:email>/', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
    path('track/', views.track_engagement, name='track_engagement'),
]
