from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_name', 'client', 'vendor', 'created_date', 'status')
    list_filter = ('created_date','status', 'vendor')
    search_fields = ('order_name', 'client__name','vendor__name')
    list_per_page = 10


admin.site.register(models.OrderType)
admin.site.register(models.OrderStatus)
admin.site.register(models.OrderDifficulty)
