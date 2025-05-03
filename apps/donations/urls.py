"""
URL configuration for donations app.
"""
from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('', views.donation_page, name='donation_page'),
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaigns/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('donate/', views.make_donation, name='make_donation'),
    path('thank-you/', views.donation_thank_you, name='thank_you'),
]
