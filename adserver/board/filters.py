from django_filters import rest_framework as filters
from board.models import Category, Ad
import django_filters


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    author = filters.NumberFilter(field_name="author", lookup_expr='id')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    state = NumberInFilter(field_name="adress__region__city__state__id", lookup_expr='in')
    city = NumberInFilter(field_name="adress__region__city__id", lookup_expr='in')
    region = NumberInFilter(field_name="adress__region__id", lookup_expr='in')
    category = filters.NumberFilter(field_name='category__id__in', method='filter_category')

 
    class Meta:
        model = Ad
        fields = ('author', 'title', 'price', 'category','state', 'city', 'region')

    def filter_category(self, queryset, field_name, value):
        try:
            value = Category.objects.get(id=value).get_descendants(include_self=True)
        except Category.DoesNotExist:
            value = []

        return queryset.filter(**{field_name: value}).select_related('category')
        