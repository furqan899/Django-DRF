import django_filters
from api.models import Product
from rest_framework import filters

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