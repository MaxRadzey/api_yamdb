from rest_framework import serializers

from titles.models import Categories, Generes, Titles


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GeneresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Generes


class TitlesSerializer(serializers.ModelSerializer):

    rating = ...
    genere = ...
    category = ...

    class Meta:
        fields = '__all__'
        model = Titles
