from django.db import models
from django.conf import settings


# start of order model
class OrderType(models.Model):
    # Use verbose_name to provide a human-readable name for the model field
    name = models.CharField(max_length=50, verbose_name="Order type")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        # Use verbose_name and verbose_name_plural to provide human-readable names for the model and its instances
        verbose_name = "Order type"
        verbose_name_plural = "Order types"


class OrderStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name="Order status")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["pk"]
        verbose_name = "Order status"
        verbose_name_plural = "Order statuses"


class OrderDifficulty(models.Model):
    name = models.CharField(max_length=50, verbose_name="Order difficulty")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["pk"]
        verbose_name = "Order difficulty"
        verbose_name_plural = "Order difficulties"


class Order(models.Model):
    # Use help_text to provide a description or guidance for the model field
    order_name = models.CharField(max_length=100, help_text="The name of the order")
    description = models.TextField(help_text="The description of the order")
    order_difficulty = models.ForeignKey(OrderDifficulty, on_delete=models.PROTECT, related_name="order_difficulties", help_text="The difficulty level of the order")
    address = models.CharField(max_length=200, help_text="The address where the order will be delivered or performed")
    order_type = models.ForeignKey(OrderType, on_delete=models.PROTECT, related_name="order_types", help_text="The type of the order")
    location = models.CharField(max_length=200, blank=True, help_text="The location of the order")
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, related_name="client_orders", help_text="The user who created the order")
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="vendor_orders", help_text="The user who accepted the order")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    special_requests = models.TextField(blank=True, default="None", help_text="Any special requests from the client")
    additional_info = models.TextField(blank=True, default="None", help_text="Any additional information from the client")
    prefered_complete_date = models.DateTimeField(null=True, blank=True, help_text="The preferred date for completing the order")
    order_status = models.ForeignKey(OrderStatus, default=10, on_delete=models.PROTECT, related_name="order_status", help_text="The current status of the order")
    client_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="The price that the client is willing to pay")
    vendor_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="The price that the vendor is asking for")

    class Meta:
        ordering = ["-updated_date", "-created_date"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.order_name


# start of picture model
class Picture(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="pictures", help_text="The order that the picture belongs to")
    url = models.CharField(max_length=255, help_text="The url of the picture")
    description = models.CharField(max_length=255, blank=True, help_text="The name or description of the picture")
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pictures", help_text="The user who uploaded the picture")

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "Picture"
        verbose_name_plural = "Pictures"

    def __str__(self):
        return f"{self.description or ''} - Order# {self.order.pk} - Order Name: {self.order.order_name}"
