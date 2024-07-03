from django.db.models import Prefetch, OuterRef, Subquery
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsOwner
from .serializers import CategorySerializer, ProductSerializer, ProductDetailSerializer, FeedbackCreateSerializer
from category.models import Category, Type, Tag, StockStatus, Color
from ...models import Product, Feedback, Images

class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        return Category.objects.all()


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


    def get_queryset(self):
        main_image_subquery = Images.objects.filter(
            product=OuterRef('pk'),
            is_main=True
        ).values('image')[:1]


        products = Product.objects.annotate(
            main_image=Subquery(main_image_subquery)
        )

        return products


class ProductByCategory(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        main_image_subquery = Images.objects.filter(
            product=OuterRef('pk'),
            is_main=True
        ).values('image')[:1]

        prosucts_by_catregory = Product.objects.filter(category_id=category_id).annotate(
            main_image_subquery=Subquery(main_image_subquery)
        )

        return prosucts_by_catregory


class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Product.objects.select_related('category'
                                                      ).prefetch_related('images_set').all()
        return queryset



class FeedbackCreateAPIView(generics.CreateAPIView):
    serializer_class = FeedbackCreateSerializer
    queryset = Feedback.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentDeleteAPIView(generics.DestroyAPIView):
    queryset = Feedback.objects.all()
    permission_classes = [IsOwner]
    lookup_field = 'id'


comment_delete = CommentDeleteAPIView.as_view()
feedback_create = FeedbackCreateAPIView.as_view()
product_detail = ProductDetailAPIView.as_view()
prduct_by_category = ProductByCategory.as_view()
category_list = CategoryListAPIView.as_view()
product_list = ProductListAPIView.as_view()







