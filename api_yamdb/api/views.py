from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404

from api.serializers import (
    CategoriesSerializer, GeneresSerializer,
    TitlesSerializer, CommentsSerializer,
    ReviewsSerializer
)
from titles.models import Categories, Generes, Titles, Comments, Reviews
from api.permissions import IsAuthorOrReadOnlyPermission


class CategoriesViewSet(viewsets.ModelViewSet):

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GeneresViewSet(viewsets.ModelViewSet):

    queryset = Generes.objects.all()
    serializer_class = GeneresSerializer


class TitlesViewSet(viewsets.ModelViewSet):

    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

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
    permission_classes = (IsAuthorOrReadOnlyPermission,)

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
