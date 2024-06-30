from django.contrib import admin
from .models import Images, Product, Feedback, LikedFeedback

admin.site.register(Product)
admin.site.register(Images)
admin.site.register(Feedback)
admin.site.register(LikedFeedback)