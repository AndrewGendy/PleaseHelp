from decimal import Decimal
from django.contrib import messages
from dal import autocomplete
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Order, OrderType, OrderStatus
from .forms import OrderForm
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from feedback.models import Feedback


ORDER_DETAIL_PAGE = "orders:order-detail"


class OrderTypeAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = OrderType.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

    def create(self, text):
        return self.get_queryset().get_or_create(name=text)

    def post(self, request, *args, **kwargs):
        text = request.POST.get("text", None)
        if text is not None:
            instance, _ = self.create(text)
            return JsonResponse(
                {
                    "id": instance.pk,
                    "text": str(instance),
                }
            )
        return JsonResponse({}, status=400)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "order_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.is_client():
                queryset = queryset.filter(client=self.request.user)
            elif self.request.user.is_vendor():
                queryset = queryset.filter(Q(vendor=self.request.user) | Q(client=self.request.user) | Q(status=OrderStatus.objects.get(name="Listed")))
        return queryset


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()

        feedbacks = Feedback.objects.filter(order=self.object, reviewer=self.request.user)
        context["feedback_submitted"] = feedbacks.exists()

        user = self.request.user
        context["is_client_or_vendor"] = user in [order.client, order.vendor]

        # Calculate the visibility conditions for the client price input
        client_price_change = order.status.pk >= 10 and order.status.pk < 30
        # Calculate the visibility conditions for the vendor price input
        vendor_price_change = order.status.pk >= 30 and order.status.pk < 50
        context["client_price_change"] = client_price_change
        context["vendor_price_change"] = vendor_price_change

        return context


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(ORDER_DETAIL_PAGE, kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"

    def form_valid(self, form):
        order = form.instance
        order.status = OrderStatus.objects.get(pk=11)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(OrderUpdateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type.pk < 40:
            return redirect("error_page")  # or whatever page we want to redirect non-staff members to
        return super(OrderUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(ORDER_DETAIL_PAGE, kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order


class ClientAcceptPriceView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs["pk"])
        priced_status_id = OrderStatus.objects.get(name="Priced")
        accepted_by_client_status_id = OrderStatus.objects.get(name="Accepted By Client")
        if request.user.is_client and order.status == priced_status_id and request.user == order.client:
            order.status = accepted_by_client_status_id
            order.save()
        return redirect(ORDER_DETAIL_PAGE, pk=kwargs["pk"])


class VendorAcceptOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs["pk"])
        listed_status_id = OrderStatus.objects.get(name="Listed")
        accepted_by_vendor_status_id = OrderStatus.objects.get(name="Accepted By Vendor")
        if request.user.is_vendor and order.status == listed_status_id:
            order.vendor = request.user
            order.status = accepted_by_vendor_status_id
            order.save()
        return redirect(ORDER_DETAIL_PAGE, pk=kwargs["pk"])


# Custom view for updating the price of an order
class OrderUpdatePriceView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"

    def dispatch(self, request, *args, **kwargs):
        # Check if the user has the required permissions
        if request.user.user_type.pk < 40:
            return redirect("error_page")  # or whatever page we want to redirect non-staff members to
        return super(OrderUpdatePriceView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        # Pass the user and order_status to the form
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["order_status"] = self.object.status
        return kwargs

    # Override the post method to update the order status directly
    def post(self, request, *args, **kwargs):
        # Get the order instance
        order = get_object_or_404(Order, pk=kwargs["pk"])

        # Update the order status based on the current status
        if order.status.pk >= 10 and order.status.pk < 30:
            order.status = OrderStatus.objects.get(name="Priced")
            client_price = request.POST.get("client_price")
            if client_price is not None and Decimal(client_price) >= 10:
                order.client_price = client_price
            else:
                messages.error(request, "Client price must be a decimal greater than or equal to 10.")
                return redirect(ORDER_DETAIL_PAGE, pk=kwargs["pk"])
        elif order.status.pk >= 30 and order.status.pk < 50:
            order.status = OrderStatus.objects.get(name="Listed")
            vendor_price = request.POST.get("vendor_price")
            if vendor_price is not None and Decimal(vendor_price) >= 10:
                order.vendor_price = vendor_price
            else:
                messages.error(request, "Vendor price must be a decimal greater than or equal to 10.")
                return redirect(ORDER_DETAIL_PAGE, pk=kwargs["pk"])

        order.save()

        # Redirect to the order detail page
        return redirect(ORDER_DETAIL_PAGE, pk=kwargs["pk"])
