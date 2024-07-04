import django_filters
from django.db.models import Avg
from ...models import Product, Feedback, StarModels


class ProductFilter(django_filters.FilterSet):
    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name')
    tag = django_filters.CharFilter(method='filter_by_tag')
    min_rating = django_filters.NumberFilter(method='filter_by_min_rating')
    max_rating = django_filters.NumberFilter(method='filter_by_max_rating')

    class Meta:
        model = Product
        fields = ['price_gte', 'price_lte', 'category', 'tag', 'min_rating', 'max_rating']

    def filter_by_tag(self, queryset, name, value):
        return queryset.filter(teg__name=value)

    def filter_by_min_rating(self, queryset, name, value):
        return queryset.filter(rating__star__gte=value)

    def filter_by_max_rating(self, queryset, name, value):
        return queryset.filter(rating__star__lte=value)
