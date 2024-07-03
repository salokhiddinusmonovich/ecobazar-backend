from django.urls import path

from .views import (
    category_list,
    product_list,
    prduct_by_category,
    product_detail,
    feedback_create
)

app_name = 'product_app'

urlpatterns = [
    path('create/feedback/', feedback_create, name='feedback-create'),

    path('categories/list/', category_list, name='categories-list'),
    path('products/list/', product_list, name='products-list'),
    path('products_by_category/<int:pk>/', prduct_by_category, name='products_by_category'),
    path('products_detail/<int:pk>/', product_detail, name='product_detail')
]