from rest_framework import viewsets

from api.serializers import (CategoriesSerializer, GeneresSerializer,
                             TitlesSerializer)
from titles.models import Categories, Generes, Titles


class CategoriesViewSet(viewsets.ModelViewSet):

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GeneresViewSet(viewsets.ModelViewSet):

    queryset = Generes.objects.all()
    serializer_class = GeneresSerializer


class TitlesViewSet(viewsets.ModelViewSet):

    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
