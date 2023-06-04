from django import forms
from django.core.validators import MinValueValidator
from .models import Order, OrderType
from dal import autocomplete


class OrderForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        queryset=OrderType.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="orders/order-type-autocomplete",
            attrs={"data-minimum-input-length": 1},  # optional, to make it require one character before seeing options
        ),
    )
    client_price = forms.CharField(
        validators=[MinValueValidator(10)],
        widget=forms.TextInput(attrs={"class": "form-control", "pattern": "\d+(\.\d{2})?", "inputmode": "decimal"}),
    )
    vendor_price = forms.CharField(
        validators=[MinValueValidator(5)],
        widget=forms.TextInput(attrs={"class": "form-control", "pattern": "\d+(\.\d{2})?", "inputmode": "decimal"}),
    )

    class Meta:
        model = Order
        fields = [
            "order_name",
            "description",
            "order_difficulty",
            "address",
            "order_type",
            "location",
            "special_requests",
            "additional_info",
            "client_price",
            "vendor_price",
        ]
        widgets = {
            "order_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "special_requests": forms.Textarea(attrs={"class": "form-control"}),
            "additional_info": forms.Textarea(attrs={"class": "form-control"}),
        }

    def clean_type(self):
        type_value = self.cleaned_data["type"]
        type_obj, _ = OrderType.objects.get_or_create(name=type_value)
        return type_obj

    def clean(self):
        cleaned_data = super().clean()
        vendor_price = cleaned_data.get("vendor_price")
        client_price = cleaned_data.get("client_price")

        if client_price is None:
            self.add_error("Error getting Client Price", "Client Price is required")
        elif vendor_price is not None and vendor_price >= client_price - 5:
            self.add_error("vendor_price", "Vendor price must be at least $5 below client price")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        order = kwargs.get("instance", None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if user and (user.user_type.pk < 40 or order is None or user in [order.client, order.vendor]):
            self.fields.pop("client_price")
            self.fields.pop("vendor_price")
