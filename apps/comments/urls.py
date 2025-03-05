from django.urls import path
from . import views

urlpatterns = [
    path('add-comment/<int:page_id>/', views.add_comment, name='add_comment'),
] 