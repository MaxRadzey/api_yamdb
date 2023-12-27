from django.db import models

from titles.constants import SYMBOL_LIMIT


class Categories(models.Model):

    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Слаг категории', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:SYMBOL_LIMIT]


class Generes(models.Model):

    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Слаг жанра', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:SYMBOL_LIMIT]


class Titles(models.Model):

    name = models.CharField('Название произведения', max_length=256)
    year = models.DateTimeField('Дата выхода произведения',)
    description = models.TextField('Описание произведения',)
    genre = models.ForeignKey(
        Generes, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:SYMBOL_LIMIT]
