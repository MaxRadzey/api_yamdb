from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from titles.constants import SYMBOL_LIMIT

User = get_user_model()


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
    rating = models.DecimalField(
        'Рейтинг произведения',
        max_digits=3, decimal_places=2,
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:SYMBOL_LIMIT]


class Reviews(models.Model):
    grade = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comments(models.Model):
    text = models.TextField('Текст комментария')
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:SYMBOL_LIMIT]
