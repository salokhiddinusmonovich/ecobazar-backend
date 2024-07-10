from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from product.models import Product
from .permissions import IsOrderOwner
from .serializers import OrderSerializer
from order.models import Order, OrderItem
from rest_framework.views import APIView
from django.db.models import F

from ...services import inc_or_dec


class CartByOwnerListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOrderOwner]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class AddOrderView(APIView):
    permission_classes = [IsOrderOwner]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(self.request, product)

        if product.quantity <= 0:
            return Response({'message': "Product is not available"}, status=status.HTTP_200_OK)

        order, created = Order.objects.get_or_create(customer=request.user, ordered=False)

        orderitem, item_created = OrderItem.objects.get_or_create(product=product, customer=request.user, ordered=False)

        if not item_created:
            orderitem.quantity = F('quantity') + 1
            orderitem.save()
        else:
            order.orderitem.add(orderitem)

        product.quantity = F('quantity') - 1
        product.save()

        return Response({"message": "Ok"}, status=status.HTTP_201_CREATED)


class RemoveOrderView(APIView):
    permission_classes = [IsOrderOwner]
    def post(self, request, pk):
        orderitem = get_object_or_404(OrderItem, pk=pk)
        order = Order.objects.filter(orderitem=orderitem, ordered=False).first()
        self.check_object_permissions(self.request, orderitem)
        orderitem.product.quantity = F('quantity') + F('orderitem.quantity')
        orderitem.product.save()
        order.orderitem.remove(orderitem)
        orderitem.delete()
        return Response({"message": 'Ok'}, status=status.HTTP_204_NO_CONTENT)


class OrderItemIncremintAPIView(APIView):
    permission_classes = [IsOrderOwner]

    def post(self, request, pk):
        orderitem = get_object_or_404(OrderItem, pk=pk)
        self.check_object_permissions(self.request, orderitem)
        if orderitem.product.quantity <= 0:
            return Response({'message': "Product qolmadi!"}, status=status.HTTP_200_OK)
        inc_or_dec(obj=orderitem, num=1, is_inc=True)
        inc_or_dec(obj=orderitem.product, num=1, is_inc=False)
        return Response({"message": "Ok"}, status=status.HTTP_200_OK)


class OrderItemDecrementAPIView(APIView):
    permission_classes = [IsOrderOwner]

    def post(self, request, pk):
        orderitem = get_object_or_404(OrderItem, pk=pk)
        self.check_object_permissions(self.request, orderitem)
        if orderitem.quantity == 1:
            orderitem.product.quantity = F('quantity') + 1
            orderitem.product.save()
            orderitem.delete()
            return Response({'message': "Order deleted"}, status=status.HTTP_204_NO_CONTENT)
        orderitem.quantity = F('quantity') - 1
        orderitem.save()
        orderitem.product.quantity = F('quantity') + 1
        orderitem.product.save()
        return Response({"message": "Ok"}, status=status.HTTP_200_OK)

increase_order = OrderItemIncremintAPIView.as_view()
decrease_order = OrderItemDecrementAPIView.as_view()
delete_order = RemoveOrderView.as_view()
add_order = AddOrderView.as_view()
cart = CartByOwnerListAPIView.as_view()