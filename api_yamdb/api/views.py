from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination

from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (
    CategorySerializer, GenreSerializer,
    TitleViewSerializer, CommentsSerializer,
    ReviewSerializer, TitlesCreateSerializer
)
from reviews.models import Category, Genre, Title
from api.permissions import IsAuthorOrAdminOrModerator
from api.filters import TitlesFilter
from api.mixins import BaseViewSet, CategoryGenreBaseViewSet
from api.utils import get_title, get_review


class CategoryViewSet(CategoryGenreBaseViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreBaseViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    BaseViewSet
):
    """Вьюсет для произведений."""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleViewSerializer
        return TitlesCreateSerializer

    def get_queryset(self):
        titles = Title.objects.annotate(
            rating=models.Avg('reviews__score')
        )
        return titles


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = (IsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        """Получение всех отзывов или конкретного отзыва."""
        title = get_title(self.kwargs)
        review = title.reviews.all()
        return review


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
