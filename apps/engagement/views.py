from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from apps.engagement.models import NewsletterSubscription, EngagementEvent

@require_POST
def newsletter_subscribe(request):
    """Handle newsletter subscription."""
    email = request.POST.get('email')
    name = request.POST.get('name', '')
    
    try:
        validate_email(email)
        subscription, created = NewsletterSubscription.objects.get_or_create(
            email=email,
            defaults={'name': name}
        )
        
        if created:
            messages.success(request, 'Thank you for subscribing to our newsletter!')
        else:
            if not subscription.is_active:
                subscription.is_active = True
                subscription.save()
                messages.success(request, 'Your subscription has been reactivated!')
            else:
                messages.info(request, 'You are already subscribed to our newsletter.')
                
    except ValidationError:
        messages.error(request, 'Please enter a valid email address.')
    except Exception as e:
        messages.error(request, 'There was an error processing your subscription.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

def newsletter_unsubscribe(request, email):
    """Handle newsletter unsubscription."""
    try:
        subscription = get_object_or_404(NewsletterSubscription, email=email)
        subscription.unsubscribe()
        messages.success(request, 'You have been unsubscribed from our newsletter.')
    except Exception as e:
        messages.error(request, 'There was an error processing your unsubscription.')
    
    return redirect('core:home')

@require_POST
def track_engagement(request):
    """Track user engagement events."""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Authentication required'}, status=401)

    event_type = request.POST.get('event_type')
    page_id = request.POST.get('page_id')
    content_type = request.POST.get('content_type')
    object_id = request.POST.get('object_id')
    metadata = request.POST.get('metadata', {})

    try:
        event = EngagementEvent.objects.create(
            user=request.user,
            event_type=event_type,
            page_id=page_id,
            content_type=content_type,
            object_id=object_id,
            metadata=metadata
        )
        return JsonResponse({'status': 'success', 'event_id': event.id})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
