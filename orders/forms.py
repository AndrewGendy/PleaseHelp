from django import forms
from .models import Order, OrderType, OrderDifficulty
from dal import autocomplete


class OrderForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        queryset=OrderType.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='orders/order-type-autocomplete',
            attrs={'data-minimum-input-length': 0},  # optional, to remove the need to type before seeing options
        ),
    )

    class Meta:
        model = Order
        fields = [
            "order_name",
            "description",
            "difficulty",
            "address",
            "type",
            "location",
            "special_requests",
        ]
        widgets = {
            "order_name": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
            "address": forms.TextInput(attrs={'class': 'form-control'}),
            "location": forms.TextInput(attrs={'class': 'form-control'}),
            "special_requests": forms.Textarea(attrs={'class': 'form-control'}),
        }


    def clean_type(self):
        type_value = self.cleaned_data['type']
        type_obj, created = OrderType.objects.get_or_create(name=type_value)
        return type_obj