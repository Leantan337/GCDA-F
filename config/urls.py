"""
URL Configuration for NGO Website.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from apps.core.views import index

urlpatterns = [
    # Django Admin
    path('django-admin/', admin.site.urls),

    # Wagtail Admin
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    # User authentication
    path('accounts/', include('allauth.urls')),

    # Comments
    path('comments/', include('apps.comments.urls')),

    # Landing page
    path('', index, name='index'),

    # Wagtail serves other pages
    path('pages/', include(wagtail_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
