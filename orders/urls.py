from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.OrderListView.as_view(), name="order-list"),
    path("order-list", views.OrderListView.as_view(), name="order-list"),
    path("order-detail/<int:pk>", views.OrderDetailView.as_view(), name="order-detail"),
    path("order-create", views.OrderCreateView.as_view(), name="order-create"),
    path("order-update/<int:pk>", views.OrderUpdateView.as_view(), name="order-update"),
    path("order/<int:pk>/client-accept-price/", views.ClientAcceptPriceView.as_view(), name="client-accept-price"),
    path("order/<int:pk>/vendor-accept-order/", views.VendorAcceptOrderView.as_view(), name="vendor-accept-order"),
    path("order/<int:pk>/vendor-complete-order/", views.VendorCompleteOrderView.as_view(), name="vendor-complete-order"),
    path("order/<int:pk>/update-price/", views.OrderUpdatePriceView.as_view(), name="order-update-price"),
    path("order-type-autocomplete/", views.OrderTypeAutocomplete.as_view(), name="order-type-autocomplete"),
]
