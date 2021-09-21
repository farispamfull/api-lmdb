from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    empty_value_display = '-empty-'


@admin.register(Genre)
class AdminGenre(admin.ModelAdmin):
    empty_value_display = '-empty-'


@admin.register(Title)
class AdminTitle(admin.ModelAdmin):
    empty_value_display = '-empty-'


@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    empty_value_display = '-empty-'


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    empty_value_display = '-empty-'