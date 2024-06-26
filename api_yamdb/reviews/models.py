from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import (NAME_MAX_LENGTH, SYMBOL_LIMIT,
                               MAX_REVIEW_SCORE, MIN_REVIEW_SCOR)
from reviews.base_models import (AuthorPubDateAbstractModel,
                                 GenreAndCategoryAbstractModel)
from reviews.validators import validate_year

User = get_user_model()


class Category(GenreAndCategoryAbstractModel):

    class Meta(GenreAndCategoryAbstractModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(GenreAndCategoryAbstractModel):

    class Meta(GenreAndCategoryAbstractModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):

    name = models.CharField(
        'Название произведения',
        max_length=NAME_MAX_LENGTH
    )
    year = models.PositiveSmallIntegerField(
        'Дата выхода произведения',
        validators=[validate_year]
    )
    description = models.TextField('Описание произведения', blank=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:SYMBOL_LIMIT]


class Review(AuthorPubDateAbstractModel):

    score = models.PositiveSmallIntegerField(
        default=MIN_REVIEW_SCOR,
        validators=[
            MaxValueValidator(
                MAX_REVIEW_SCORE, message='Оценка не должна быть больше 10!'
            ),
            MinValueValidator(
                MIN_REVIEW_SCOR, message='Оценка не должна быть меньше 1!'
            )
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
        default_related_name = 'reviews'
        constraints = (models.UniqueConstraint(
            fields=['author', 'title'], name='unique_review'
        ),
        )


class Comments(AuthorPubDateAbstractModel):

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )

    class Meta(AuthorPubDateAbstractModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
