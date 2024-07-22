from django.urls import path

from blog.api.v1 import views

app_name = 'blog_api'

urlpatterns = [
    path('create/', views.BlogCreateAPIView.as_view()),
    path('', views.BlogListAPIView.as_view()),
    path('comments/', views.CommentListAPIView.as_view()),
    path('tags/', views.TagListAPIView.as_view()),
    path('categories/', views.CategoryListAPIView.as_view()),
    path('detail/<int:pk>/', views.BlogDetailAPIView.as_view()),
    path('comments/detail/<int:pk>/', views.CommentDetailAPIView.as_view()),
    path('tags/detail/<int:pk>/', views.TagDetailAPIView.as_view()),
    path('categories/detail/<int:pk>/', views.CategoryDetailAPIView.as_view()),
    path('comments/create/', views.CommentCreateAPIView.as_view()),
    path('tags/create/', views.TagCreateAPIView.as_view()),
    path('categories/create/', views.CategoryCreateAPIView.as_view()),
    path('update/<int:pk>/', views.BlogUpdateAPIView.as_view()),
    path('comments/update/<int:pk>/', views.CommentUpdateAPIView.as_view()),
    path('tags/update/<int:pk>/', views.TagUpdateAPIView.as_view()),
    path('categories/update/<int:pk>/', views.CategoryUpdateAPIView.as_view()),
    path('delete/<int:pk>/', views.BlogDeleteAPIView.as_view()),
    path('comments/delete/<int:pk>/', views.CommentDeleteAPIView.as_view()),
    path('tags/delete/<int:pk>/', views.TagDeleteAPIView.as_view()),
    path('categories/delete/<int:pk>/', views.CategoryDeleteAPIView.as_view()),
]