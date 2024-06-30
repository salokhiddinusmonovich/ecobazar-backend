from django.contrib import admin
from .models import Order, TimeStampModel, OrderItem


admin.site.register(Order)
admin.site.register(OrderItem)
