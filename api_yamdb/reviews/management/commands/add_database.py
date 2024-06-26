import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, Review, Comments, User


class Command(BaseCommand):
    help = ('Импорт данных из csv файла в БД.'
            'Перед импортом данных необходимо удалить БД.')

    def handle(self, *args, **options):
        self.stdout.write('Добавление базы данных!')
        relative_path = "static/data"
        absolute_path = os.path.abspath(relative_path)  # Путь к папке с файлам

        CSV_DATA_AND_MODELS = (
            ('category.csv', {}, Category),
            ('genre.csv', {}, Genre),
            ('users.csv', {}, User),
            ('titles.csv', {'category': 'category_id'}, Title),
            (
                'genre_title.csv',
                {},
                Title.genre.through
            ),
            ('review.csv', {'author': 'author_id'}, Review),
            ('comments.csv', {'author': 'author_id'}, Comments),
        )

        for file_name, columns_name, models in CSV_DATA_AND_MODELS:
            with open(
                f'{absolute_path}/{file_name}', 'r', encoding='utf-8'
            ) as csvfile:
                data = csv.DictReader(csvfile)
                list_to_add_in_db = []
                for row in data:
                    for old_name, new_name in columns_name.items():
                        row[new_name] = row.pop(old_name)
                    list_to_add_in_db.append(models(**row))
                models.objects.bulk_create(list_to_add_in_db)
        self.stdout.write('База данных добавлена!')
