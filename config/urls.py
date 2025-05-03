"""
URL Configuration for NGO Website.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

# Main URL patterns
urlpatterns = [
    # Admin URLs
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    
    # Wagtail URLs
    path('documents/', include(wagtaildocs_urls)),
    
    # App URLs
    path('', include('apps.core.urls', namespace='core')),
    path('news/', include('apps.news.urls')),
    path('comments/', include(('apps.comments.urls', 'comments'), namespace='comments')),
    path('donations/', include('apps.donations.urls')),
    path('engagement/', include('apps.engagement.urls')),
    
    # Wagtail catch-all URL
    path('', include(wagtail_urls)),
]

# Add static/media serving for development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug toolbar URLs (only added in debug mode)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
