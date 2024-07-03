from django.db.models import Prefetch, OuterRef, Subquery
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .permissions import IsOwner
from .serializers import CategorySerializer, ProductSerializer, ProductDetailSerializer, FeedbackCreateSerializer, \
    FeedbackUpdateSerializer
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

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Feedback created', 'data': response.data}, status=status.HTTP_201_CREATED)


class CommentDeleteAPIView(generics.DestroyAPIView):
    queryset = Feedback.objects.all()
    permission_classes = [IsOwner]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Feedback deleted successfully'}, status=status.HTTP_200_OK)

class FeedbackUpdateAPIView(generics.UpdateAPIView):
    serializer_class = FeedbackUpdateSerializer
    queryset = Feedback.objects.all()
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'message': 'Feedback updated', 'data': serializer.data}, status=status.HTTP_200_OK)


feedback_update = FeedbackUpdateAPIView().as_view()
feedback_delete = CommentDeleteAPIView.as_view()
feedback_create = FeedbackCreateAPIView.as_view()
product_detail = ProductDetailAPIView.as_view()
product_by_category = ProductByCategory.as_view()
category_list = CategoryListAPIView.as_view()
product_list = ProductListAPIView.as_view()







