from django.contrib.auth import get_user_model
from django.db import models

from reviews.constants import NAME_MAX_LENGTH, SYMBOL_LIMIT

User = get_user_model()


class AuthorPubDateAbstractModel(models.Model):

    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:SYMBOL_LIMIT]


class GenreAndCategoryAbstractModel(models.Model):
    """Абстрактная модель."""

    name = models.CharField(
        'Название',
        max_length=NAME_MAX_LENGTH,
        unique=True
    )
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:SYMBOL_LIMIT]
