from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from . import forms
from django.contrib import messages


# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})


class RegisterView(CreateView):
    form_class = forms.UserSignupForm
    success_url = reverse_lazy('login')
    template_name ='accounts/register.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        errors = form.errors.as_data()
        for field, error in errors.items():
            for e in error:
                messages.error(self.request, f"{field}: {str(e)}")
        return response
    

class UserProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        return context
    
class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = forms.UserProfileForm
    template_name = 'account/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs['username'])

    def test_func(self):
        return self.get_object() == self.request.user