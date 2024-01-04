from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import ValidationError

from titles.models import Categories, Genres, Titles, Reviews, Comments


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""
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
        model = Titles

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
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta():
        model = Comments
        fields = ['id', 'text', 'author', 'pub_date']
        read_only_fields = ('author', 'pub_date')
