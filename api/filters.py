import django_filters
from api.models import Product
from rest_framework import filters
from api.models import Order

class InStockFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'contains'],
            'price': ['gt', 'lt'],
        }

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['gt', 'lt', 'exact', 'range'],
        }