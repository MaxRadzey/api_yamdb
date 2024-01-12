from rest_framework import viewsets, filters, mixins, serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (
    CategorySerializer, GenreSerializer,
    TitleViewSerializer, CommentsSerializer,
    ReviewSerializer, TitlesCreateSerializer
)
from reviews.models import Category, Genre, Title, Review
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

    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleViewSerializer
        elif self.action in ['create', 'partial_update']:
            return TitlesCreateSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
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
