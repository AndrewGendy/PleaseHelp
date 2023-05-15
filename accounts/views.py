from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms
from django.contrib import messages


# Create your views here.
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