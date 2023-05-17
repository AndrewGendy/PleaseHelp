from django.forms import ModelForm
from .models import Order


class OrderForm(ModelForm):
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