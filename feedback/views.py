from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.shortcuts import get_object_or_404, redirect
from .models import Feedback
from orders.models import Order
from .forms import FeedbackForm


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = "feedback/feedback_form.html"
    success_message = "Feedback Submitted Successfully!"

    def dispatch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs["order_pk"])
        if request.user not in [order.client, order.vendor] or order.status.pk < 60:
            return redirect("error_page")  # or whatever page we want to redirect non-staff members to
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.order = get_object_or_404(Order, id=self.kwargs["order_pk"])
        feedback.reviewer = self.request.user
        if feedback.reviewer.is_client():
            feedback.reviewed = feedback.order.vendor
        else:
            feedback.reviewed = feedback.order.client

        feedback.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("feedback:feedback_success")


class FeedbackListView(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = "feedback/feedback_list.html"
    context_object_name = "feedbacks"

    def get_queryset(self):
        return Feedback.objects.filter(reviewed=self.request.user).order_by("-created_at")
