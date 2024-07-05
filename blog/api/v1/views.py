from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from blog.api.v1.permissions import IsAdmin
from blog.api.v1.serializers import BlogListSerializer, BlogDetailSerializer  # , BlogCreateSerializer
from blog.models import Blog


class BlogListAPIView(generics.ListAPIView):
    serializer_class = BlogListSerializer

    def get_queryset(self):
        return Blog.objects.all()

# class BlogCreateAPIView(generics.CreateAPIView):
#     serializer_class = BlogCreateSerializer
#     queryset = Blog.objects.all()
#     permission_classes = (IsAuthenticated, IsAdmin)
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

class BlogDetailAPIView(generics.RetrieveAPIView):
    serializer_class = BlogDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Blog.objects.select_related('category').all()
        return queryset

