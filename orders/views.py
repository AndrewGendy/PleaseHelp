from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from decimal import Decimal
from dal import autocomplete
from feedback.models import Feedback
from .models import Order, OrderType, OrderStatus
from .forms import OrderForm


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
        # Using select_related to fetch the foreign key fields in one query
        queryset = queryset.select_related("difficulty", "type", "client", "vendor", "status")
        return queryset


class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        # Use select_related to fetch the foreign key fields in one query
        return super().get_queryset().select_related("difficulty", "type", "client", "vendor", "status")

    def test_func(self):
        # Store the order object in a variable
        self.order = self.get_object()
        user = self.request.user
        # Check if the user is the client or the vendor of the order
        return user == self.order.client or user == self.order.vendor or user.user_type.pk >= 30 or (self.order.status.pk == 40 and user.user_type.pk >= 20)

    def handle_no_permission(self):
        # Redirect to the error_page if the test fails
        return redirect("error_page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Use the order object from the variable
        order = self.order

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


class OrderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"
    success_message = "Order Created Successfully!"

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(ORDER_DETAIL_PAGE, kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class OrderUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"
    success_message = "Order Updated Successfully!"

    def form_valid(self, form):
        order = form.instance
        order.status = OrderStatus.objects.get(pk=11)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(OrderUpdateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs["pk"])
        if request.user == order.client:
            return super(OrderUpdateView, self).dispatch(request, *args, **kwargs)
        return redirect("error_page")  # or whatever page we want to redirect non-staff members to

    def get_success_url(self):
        return reverse_lazy(ORDER_DETAIL_PAGE, kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class OrderDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Order


class ClientAcceptPriceView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs["pk"])
        priced_status_id = OrderStatus.objects.get(name="Priced")
        accepted_by_client_status_id = OrderStatus.objects.get(name="Accepted By Client")
        if request.user.is_client and order.status == priced_status_id and request.user == order.client:
            order.status = accepted_by_client_status_id
            order.save()
            messages.success(request, "Price Accepted!")
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
            messages.success(request, "Order Accepted!")
        return redirect(ORDER_DETAIL_PAGE, pk=kwargs["pk"])


class VendorCompleteOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs["pk"])
        if request.user.is_vendor and request.user == order.vendor and order.status.pk == 50:
            order.status = OrderStatus.objects.get(name="Order Complete")
            order.save()
            messages.success(request, "Order Completed Successfully! Your payment will be processed shortly.")
        return redirect(ORDER_DETAIL_PAGE, pk=kwargs["pk"])


# Custom view for updating the price of an order
class OrderUpdatePriceView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    success_message = "Price Updated Successfully!"
    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"

    def dispatch(self, request, *args, **kwargs):
        # Check if the user has the required permissions
        if request.user.user_type.pk < 40:
            return redirect("error_page")  # or whatever page we want to redirect non-staff members to
        return super(OrderUpdatePriceView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        # Pass the user and order status to the form
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["status"] = self.object.status
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
                messages.success(request, "Client's Price added correctly.")
            else:
                messages.error(request, "Client price must be greater than or equal to 10.")
                return redirect(ORDER_DETAIL_PAGE, pk=kwargs["pk"])
        elif order.status.pk >= 30 and order.status.pk < 50:
            order.status = OrderStatus.objects.get(name="Listed")
            vendor_price = request.POST.get("vendor_price")
            if vendor_price is not None and Decimal(vendor_price) >= 10:
                order.vendor_price = vendor_price
                messages.success(request, "Vendor's Price added correctly.")
            else:
                messages.error(request, "Vendor price must be greater than or equal to 10.")
                return redirect(ORDER_DETAIL_PAGE, pk=kwargs["pk"])

        order.save()

        # Redirect to the order detail page
        return redirect(ORDER_DETAIL_PAGE, pk=kwargs["pk"])
