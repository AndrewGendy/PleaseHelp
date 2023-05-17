from django.urls import path
from django.contrib.auth import views as auth_views
from. import views

app_name ='orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path('order-list', views.OrderListView.as_view(), name='order-list'),
    path('order-detail/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('order-create', views.OrderCreateView.as_view(), name='order-create'),
    path('order-update/<int:pk>', views.OrderUpdateView.as_view(), name='order-update'),
    
]