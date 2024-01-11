from django.contrib import admin

from reviews.models import Category, Genre, Title, Comments, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug'
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug'
    )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'year', 'description', 'category'
    )


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'author', 'pub_date', 'review'
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'author', 'score', 'pub_date', 'title'
    )
