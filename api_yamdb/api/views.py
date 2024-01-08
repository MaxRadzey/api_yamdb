from rest_framework import viewsets, filters, mixins, serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (
    CategoriesSerializer, GenresSerializer,
    TitlesViewSerializer, CommentsSerializer,
    ReviewsSerializer, TitlesCreateSerializer
)
from reviews.models import Categories, Genres, Title, Comments, Review
from api.permissions import IsAdmin, IsAuthorOrAdminOrModerator
from .filters import TitlesFilter


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
        if self.action in ['list', 'retrieve']:
            return TitlesViewSerializer
        elif self.action in ['create', 'partial_update']:
            return TitlesCreateSerializer
        return TitlesViewSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""
    serializer_class = ReviewsSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            self.permission_classes = [IsAuthorOrAdminOrModerator]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super(ReviewsViewSet, self).get_permissions()

    def get_queryset(self):
        """Получение всех отзывов или конкретного отзыва."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id', False)
        if review_id:
            review = get_object_or_404(
                Title, title=title, pk=review_id
            )
            return review
        reviews = Review.objects.filter(title=title)
        return reviews

    def perform_create(self, serializer):
        """Cоздание отзыва."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
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

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            self.permission_classes = [IsAuthorOrAdminOrModerator]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super(CommentsViewSet, self).get_permissions()

    def get_queryset(self):
        """Получение всех комментариев или конкретного комментария."""
        review_id = self.kwargs.get('review_id', False)
        comment_id = self.kwargs.get('comment_id', False)
        queryset = Comments.objects.all()
        if review_id:
            queryset = queryset.filter(review_id=review_id)
        if comment_id:
            queryset = queryset.filter(pk=comment_id)
        return queryset

    def perform_create(self, serializer):
        """Создание комментариев."""
        review_id = self.kwargs.get('review_id', False)
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
