from datetime import datetime
import re

from rest_framework import serializers
from rest_framework.validators import ValidationError

from reviews.models import Categories, Genres, Title, Review, Comments


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    class Meta:
        fields = ('name', 'slug')
        model = Categories

    def validate_slug(self, value):
        reg_slug = '^[-a-zA-Z0-9_]+$'
        if re.match(reg_slug, value):
            return value


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""
    class Meta:
        fields = ('name', 'slug')
        model = Genres

    def validate_slug(self, value):
        reg_slug = '^[-a-zA-Z0-9_]+$'
        if re.match(reg_slug, value):
            return value


class TitlesViewSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""

    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Title


class TitlesCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создание произведений."""
    rating = ...
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genres.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Title

        def validate_year(self, value):
            if value < 0 and value > datetime.now().year:
                raise ValidationError(
                    'Укажите верную дату.'
                )
            return value


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        read_only_fields = ('author', 'pub_date')
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta():
        model = Comments
        fields = ['id', 'text', 'author', 'pub_date']
        read_only_fields = ('author', 'pub_date')
