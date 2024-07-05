from django.urls import path

from .views import BlogListAPIView, BlogDetailAPIView #,BlogCreateAPIView

app_name = 'blog_api'

urlpatterns = [
    path('list/', BlogListAPIView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>/', BlogDetailAPIView.as_view(), name='blog_detail')
    # path('create/', BlogCreateAPIView.as_view(), name='blog-create'),
]