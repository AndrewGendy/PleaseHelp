from django.urls import path
from . import views

app_name ='orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path('order-list', views.OrderListView.as_view(), name='order-list'),
    path('order-detail/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('order-create', views.OrderCreateView.as_view(), name='order-create'),
    path('order-update/<int:pk>', views.OrderUpdateView.as_view(), name='order-update'),

    path('order-type-autocomplete/', views.OrderTypeAutocomplete.as_view(), name='order-type-autocomplete'),
]