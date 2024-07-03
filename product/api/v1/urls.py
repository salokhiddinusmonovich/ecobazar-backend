from django.urls import path

from .views import (
    category_list,
    product_list,
    product_by_category,
    product_detail,
    feedback_create,
    feedback_delete,
    feedback_update
)

app_name = 'product_app'

urlpatterns = [
    path('create/feedback/', feedback_create, name='feedback-create'),
    path('delete/feedback/<int:pk>/', feedback_delete, name='feedback_delete'),
    path('update/feedback/<int:pk>/', feedback_update, name='feedback_update'),

    path('categories/list/', category_list, name='categories-list'),
    path('products/list/', product_list, name='products_list'),
    path('products_by_category/<int:pk>/', product_by_category, name='products_by_category'),
    path('products_detail/<int:pk>/', product_detail, name='product_detail')
]