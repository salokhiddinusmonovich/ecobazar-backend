from django.contrib import admin
from .models import Images, Product, Feedback, StarModels

admin.site.register(Product)
admin.site.register(Images)
admin.site.register(Feedback)
admin.site.register(StarModels)
