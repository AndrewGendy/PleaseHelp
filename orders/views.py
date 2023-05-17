from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Order
from.forms import OrderForm




class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'  # change this to your actual template path
    context_object_name = 'order_list'  # change this to the context name you want to use in your template
    
class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'  # Assuming you have this template
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