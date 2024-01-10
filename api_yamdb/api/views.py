from rest_framework import viewsets, filters, mixins, serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import serializers
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (
    CategoriesSerializer, GenresSerializer,
    TitlesViewSerializer, CommentsSerializer,
    ReviewsSerializer, TitlesCreateSerializer
)
from reviews.models import Categories, Genres, Title, Review
from api.permissions import IsAdmin, IsAuthorOrAdminOrModerator
from .filters import TitlesFilter
from .utils import get_title, get_review


class BaseViewSet(mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """Базовый вьюсет."""

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PUT', 'PATCH']:
            self.permission_classes = [IsAdmin]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super(BaseViewSet, self).get_permissions()


class CategoriesViewSet(BaseViewSet):
    """Вьюсет для категорий."""

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(BaseViewSet):
    """Вьюсет для жанров."""

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(
    BaseViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
):
    """Вьюсет для произведений."""

    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitlesCreateSerializer
        return TitlesViewSerializer

    def get_object(self):
        title_id = self.kwargs['pk']
        title = Title.objects.filter(pk=title_id).annotate(
            rating=models.Avg('reviews__score')
        )
        return title


class ReviewsViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""
    serializer_class = ReviewsSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = (IsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        """Получение всех отзывов или конкретного отзыва."""
        title = get_title(self.kwargs)
        review = title.reviews.all()
        return review

    def perform_create(self, serializer):
        """Cоздание отзыва."""
        title = get_title(self.kwargs)
        if Review.objects.filter(
            author=self.request.user, title=title
        ).exists():

            raise serializers.ValidationError(
                'You have already reviewed this title.'
            )
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentsSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = (IsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        """Получение всех комментариев или конкретного комментария."""
        review = get_review(self.kwargs)
        comment = review.comments.all()
        return comment

    def perform_create(self, serializer):
        """Создание комментариев."""
        review = get_review(self.kwargs)
        serializer.save(author=self.request.user, review=review)
