"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", views.IndexView.as_view(), name="index"),
    path("auth/", include("djoser.urls")),
    # path("auth/", include('djoser.urls.jwt')),
    path("accounts/", include("accounts.urls")),
    # path("accounts/", include("django.contrib.auth.urls")),
    path("orders/", include("orders.urls")),
    path("messages/", include("chat_messages_system.urls")),
    path("feedback/", include("feedback.urls")),
    path("error_page", views.ErrorView.as_view(), name="error_page"),
]
