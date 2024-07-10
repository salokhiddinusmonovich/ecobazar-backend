from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add/<int:pk>/', views.add_order, name='add_order'),
    path('remove/<int:pk>/', views.delete_order, name='remove_order'),
    path('increment/<int:pk>/', views.increase_order, name='order_inc'),
    path('decrement/<int:pk>/', views.decrease_order, name='order_dec'),

]
