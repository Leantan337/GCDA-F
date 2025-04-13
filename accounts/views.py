from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserChangeForm

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {
        'form': form
    })

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomLoginForm, CustomRegistrationForm

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('core:home')  # Update this line

from django.contrib.auth import login
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings

class CustomRegistrationView(CreateView):
    form_class = CustomRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return response