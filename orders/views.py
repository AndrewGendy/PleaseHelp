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


ORDER_DETAIL_PAGE = 'orders:order-detail'

class OrderTypeAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = OrderType.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

    def create(self, text):
        return self.get_queryset().get_or_create(name=text)
    
    def post(self, request, *args, **kwargs):
        text = request.POST.get('text', None)
        if text is not None:
            instance, created = self.create(text)
            return JsonResponse({
                'id': instance.pk,
                'text': str(instance),
            })
        return JsonResponse({}, status=400)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html' 
    context_object_name = 'order_list' 

    def get_queryset(self):
        queryset = super().get_queryset()
        # if the user is logged in and the user is a client, show only his orders
        if self.request.user.is_authenticated:
            if self.request.user.is_client():
                queryset = queryset.filter(client=self.request.user)
            elif self.request.user.is_vendor():
                queryset = queryset.filter(Q(vendor=self.request.user) | Q(client=self.request.user) | Q(status=OrderStatus.objects.get(name='Listed')))
        return queryset


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html' 
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feedbacks = Feedback.objects.filter(order=self.object, reviewer=self.request.user)
        context['feedback_submitted'] = feedbacks.exists()
        return context
    

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(ORDER_DETAIL_PAGE, kwargs={'pk': self.object.pk})


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    
    def form_valid(self, form):
        order = form.instance
        order.status = OrderStatus.objects.get(pk=11)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(ORDER_DETAIL_PAGE, kwargs={'pk': self.object.pk})

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order


class AcceptOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['pk'])
        listed_status_id = OrderStatus.objects.get(name='Listed')
        accepted_by_vendor_status_id = OrderStatus.objects.get(name='Accepted By Vendor')
        if request.user.is_vendor and order.status == listed_status_id:
            order.vendor = request.user
            order.status = accepted_by_vendor_status_id
            order.save()
        return redirect(ORDER_DETAIL_PAGE, pk=kwargs['pk'])