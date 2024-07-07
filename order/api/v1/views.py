from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from product.models import Product
from .permissions import IsOrderOwner
from .serializers import OrderSerializer
from order.models import Order, OrderItem
from rest_framework.views import APIView


class CartByOwnerListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)








cart = CartByOwnerListAPIView.as_view()