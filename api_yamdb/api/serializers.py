from datetime import datetime
import re

from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.contrib.auth import get_user_model

from reviews.models import Categories, Genres, Title, Review, Comments


User = get_user_model()


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
    rating = serializers.IntegerField(read_only=True,)
    genre = GenresSerializer(many=True, read_only=True,)
    category = CategoriesSerializer(read_only=True,)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Title


class TitlesCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создание произведений."""
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
            'id', 'name', 'year',
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
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('pub_date',)
        model = Review
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('author', 'title')
        #     )
        # ]


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta():
        model = Comments
        fields = ['id', 'text', 'author', 'pub_date']
        read_only_fields = ('author', 'pub_date')
