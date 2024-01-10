from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from reviews.constants import SYMBOL_LIMIT
from .mixins import AuthorPubDateAbstractModel


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


class Title(models.Model):

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

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:SYMBOL_LIMIT]


class Review(AuthorPubDateAbstractModel):

    text = models.TextField('Текст отзыва',)
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MaxValueValidator(10, message='Оценка не должна быть больше 10!'),
            MinValueValidator(1, message='Оценка не должна быть меньше 1!')
        ]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'

    )

    class Meta(AuthorPubDateAbstractModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (models.UniqueConstraint(
            fields=['author', 'title'], name='unique_review'
        ),
        )


class Comments(AuthorPubDateAbstractModel):
    text = models.TextField('Текст комментария',)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )

    class Meta(AuthorPubDateAbstractModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:SYMBOL_LIMIT]
