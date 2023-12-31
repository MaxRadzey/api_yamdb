from rest_framework import serializers

from titles.models import Categories, Generes, Titles, Reviews, Comments


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GeneresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""
    class Meta:
        fields = ('name', 'slug')
        model = Generes


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""
    rating = ...
    genere = ...
    category = ...

    class Meta:
        fields = '__all__'
        model = Titles


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
