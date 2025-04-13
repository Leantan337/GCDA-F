from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.CustomRegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(
        next_page='core:home',
        template_name='accounts/logout.html'
    ), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
]