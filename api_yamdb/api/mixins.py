from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminOrReadOnly


class BaseViewSet(mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """Базовый вьюсет."""

    permission_classes = (IsAdminOrReadOnly,)


class CategoryGenreBaseViewSet(BaseViewSet):

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
