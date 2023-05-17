from dal import autocomplete
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Order, OrderType
from .forms import OrderForm
from django.http import JsonResponse
from django.db.models import Q


class OrderTypeAutocomplete(autocomplete.Select2QuerySetView):
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


class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html' 
    context_object_name = 'order_list' 

    def get_queryset(self):
        queryset = super().get_queryset()
        # if the user is logged in and the user is a client, show only his orders
        if self.request.user.is_authenticated and self.request.user.is_client():
            queryset = queryset.filter(client=self.request.user)
        elif self.request.user.is_authenticated and self.request.user.is_vendor():
            queryset = queryset.filter(Q(vendor=self.request.user) | Q(client=self.request.user) | Q(status=4))
        return queryset


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html' 
    context_object_name = 'order'

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('orders:order-detail', kwargs={'pk': self.object.pk})


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    
    def get_success_url(self):
        return reverse_lazy('orders:order-detail', kwargs={'pk': self.object.pk})

class OrderDeleteView(DeleteView):
    model = Order