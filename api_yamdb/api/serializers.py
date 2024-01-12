from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import ValidationError

from reviews.models import Category, Comments, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleViewSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""

    rating = serializers.IntegerField(read_only=True, default=None)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True,)

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
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    year = serializers.IntegerField()

    class Meta:
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category'
        )
        model = Title

    def validate_year(self, value):
        if value < 0 or value > datetime.now().year:
            raise ValidationError(
                'Укажите верную дату.'
            )
        return value

    def to_representation(self, instance):
        return TitleViewSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

        def validate(self, data):
            """Проверка на уникальность отзыва."""
            if not self.instance:
                title_id = self.context['view'].kwargs.get('title_id')
                if Review.objects.filter(
                    title_id=title_id,
                    author=self.context['request'].user
                ).exists():
                    raise serializers.ValidationError(
                        'Вы уже оставили отзыв на это произведение.'
                    )
            return data


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta():
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author',)
