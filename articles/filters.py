import django_filters
from .models import *
from django_filters import CharFilter


class ArticleFilter(django_filters.FilterSet):

    p_id = CharFilter(field_name='pubmed_id', lookup_expr='32112886')


    class Meta:
        model = article
        fields = ['pubmed_id']
