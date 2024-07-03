from django.contrib import admin
from .models import Color, Type, Tag, Category, StockStatus

admin.site.register(Color)
admin.site.register(Type)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(StockStatus)

