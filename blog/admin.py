from django.contrib import admin
from .models import Blog, LikedComment, LikedBlog, Comment

admin.site.register(Blog)
admin.site.register(LikedBlog)
admin.site.register(Comment)
admin.site.register(LikedComment)