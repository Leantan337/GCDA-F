from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from apps.donations.models import DonationPage, DonationCampaign, Donation

def donation_page(request):
    """Display the main donation page."""
    try:
        page = DonationPage.objects.first()
        campaigns = DonationCampaign.objects.filter(is_active=True)
        return render(request, 'donations/donation_page.html', {
            'page': page,
            'campaigns': campaigns
        })
    except DonationPage.DoesNotExist:
        messages.error(request, 'Donation page is not set up yet.')
        return redirect('core:home')

def campaign_list(request):
    """List all active donation campaigns."""
    campaigns = DonationCampaign.objects.filter(is_active=True)
    return render(request, 'donations/campaign_list.html', {
        'campaigns': campaigns
    })

def campaign_detail(request, pk):
    """Show details of a specific campaign."""
    campaign = get_object_or_404(DonationCampaign, pk=pk)
    return render(request, 'donations/campaign_detail.html', {
        'campaign': campaign
    })

@login_required
def make_donation(request):
    """Handle donation submission."""
    if request.method == 'POST':
        # This is a placeholder for payment processing
        # In production, integrate with a payment gateway
        campaign_id = request.POST.get('campaign')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method', 'card')
        is_anonymous = request.POST.get('is_anonymous', False)

        try:
            campaign = None
            if campaign_id:
                campaign = DonationCampaign.objects.get(pk=campaign_id)

            donation = Donation.objects.create(
                campaign=campaign,
                donor=request.user,
                amount=amount,
                payment_method=payment_method,
                is_anonymous=is_anonymous,
                status='completed'  # In production, this would be set after payment confirmation
            )

            messages.success(request, 'Thank you for your donation!')
            return redirect('donations:thank_you')

        except Exception as e:
            messages.error(request, 'There was an error processing your donation.')
            return redirect('donations:donation_page')

    return redirect('donations:donation_page')

def donation_thank_you(request):
    """Display thank you page after successful donation."""
    try:
        page = DonationPage.objects.first()
        return render(request, 'donations/thank_you.html', {
            'page': page
        })
    except DonationPage.DoesNotExist:
        messages.success(request, 'Thank you for your donation!')
        return redirect('core:home')
