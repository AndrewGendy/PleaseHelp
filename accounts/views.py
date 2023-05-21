from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.views import View
from django.http import JsonResponse
from . import forms
import cloudinary.uploader
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
    template_name = 'accounts/profile_update.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs['username'])

    def test_func(self):
        return self.get_object() == self.request.user
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ChangeAvatarView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = forms.AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('avatar')
            if image is not None:
                user_folder = f'PleaseHelp/UserProfiles/{request.user.username}'
                upload_result = cloudinary.uploader.upload(image, folder=user_folder)
                request.user.avatar = upload_result['url']
                request.user.save()
                return JsonResponse({'status': 'success', 'avatar_url': upload_result['url']})
            else:
                return JsonResponse({'status': 'error', 'message': 'No image provided'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form'}, status=400)
        
