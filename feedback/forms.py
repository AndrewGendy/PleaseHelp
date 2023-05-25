from django import forms
from django.core.exceptions import ValidationError
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None or rating < 1:
            raise ValidationError('Please select your rating.')
        return rating