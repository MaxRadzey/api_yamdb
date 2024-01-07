from django_filters import rest_framework as filters
from reviews.models import Title


class TitlesFilter(filters.FilterSet):
    """Класс для фильтрации произведений."""

    name = filters.CharFilter(field_name='name')
    year = filters.NumberFilter(field_name='year')

    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']
