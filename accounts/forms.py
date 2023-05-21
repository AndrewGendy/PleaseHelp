from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserSignupForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].lable = 'Display Name'
        self.fields['email'].lable = 'Email Address'
        self.fields['password1'].lable = 'Password'
        self.fields['password2'].lable = 'Confirm Password'

class UserProfileForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'address', 'phone']

class AvatarForm(forms.Form):
    avatar = forms.ImageField(required=False)

