from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from titles.constants import SYMBOL_LIMIT

User = get_user_model()


class Categories(models.Model):

    name = models.CharField('Название категории', max_length=256, unique=True)
    slug = models.SlugField('Слаг категории', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:SYMBOL_LIMIT]


class Genres(models.Model):

    name = models.CharField('Название жанра', max_length=256, unique=True)
    slug = models.SlugField('Слаг жанра', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:SYMBOL_LIMIT]


class Titles(models.Model):

    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField(
        'Дата выхода произведения',
        validators=[
            MaxValueValidator(datetime.now().year),
            MinValueValidator(0)
        ]
    )
    description = models.TextField('Описание произведения', blank=True)
    genre = models.ManyToManyField(Genres, verbose_name='Жанр')
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    rating = models.IntegerField(
        'Рейтинг произведения', null=True, validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:SYMBOL_LIMIT]


class Reviews(models.Model):
    text = models.TextField('Текст отзыва',)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    score = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comments(models.Model):
    text = models.TextField('Текст комментария',)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:SYMBOL_LIMIT]
