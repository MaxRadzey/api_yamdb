from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (
    CategoriesSerializer, GenresSerializer,
    TitlesViewSerializer, CommentsSerializer,
    ReviewsSerializer, TitlesCreateSerializer
)
from titles.models import Categories, Genres, Titles, Comments, Reviews
from api.permissions import IsAuthorOrReadOnlyPermission, IsAdminOrReadOnly, IsAdmin, IsModerator, IsAuthorOrReadOnly
from .filters import TitlesFilter


class BaseViewSet(viewsets.ModelViewSet):
    """Базовый вьюсет."""
    pagination_class = LimitOffsetPagination

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
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(BaseViewSet):
    """Вьюсет для жанров."""

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Titles.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
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

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsAuthorOrReadOnly]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsModerator | IsAdmin]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super(ReviewsViewSet, self).get_permissions()

    def get_queryset(self):
        """Получение всех отзывов или конкретного отзыва."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        review_id = self.kwargs.get('review_id', False)
        if review_id:
            review = get_object_or_404(
                Titles, title=title, pk=review_id
            )
            return review
        reviews = Reviews.objects.filter(title=title)
        return reviews

    def perform_create(self, serializer):
        """Cоздание отзыва."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentsSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsAuthorOrReadOnly]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsModerator | IsAdmin]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super(ReviewsViewSet, self).get_permissions()

    def get_queryset(self):
        """Получение всех комментариев или конкретного комментария."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        review_id = self.kwargs.get('review_id', False)
        review = get_object_or_404(Reviews, title=title, pk=review_id)
        comment_id = self.kwargs.get('comment_id', False)
        if comment_id:
            comment = get_object_or_404(
                Comments, review=review, pk=comment_id
            )
            return comment
        comments = Comments.objects.filter(review=review)
        return comments

    def perform_create(self, serializer):
        """Создание комментариев."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        review_id = self.kwargs.get('review_id', False)
        review = get_object_or_404(Reviews, title=title, pk=review_id)
        serializer.save(author=self.request.user, review=review)
