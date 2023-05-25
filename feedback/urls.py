from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name ='feedback'

urlpatterns = [
    path('', views.FeedbackListView.as_view(), name='feedback_list'),
    path('new/<int:order_pk>', views.FeedbackCreateView.as_view(), name='feedback_new'),
    path('success/', TemplateView.as_view(template_name='feedback/feedback_success.html'), name='feedback_success'),
    path('feedbacks/', views.FeedbackListView.as_view(), name='feedback_list'),
]
