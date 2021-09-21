from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField('Категория', max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Title(models.Model):
    name = models.CharField('Название', max_length=100)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[MaxValueValidator(datetime.now().year)])
    description = models.TextField('Описание', null=True, blank=True)
    category = models.ForeignKey(
        Category, verbose_name='Категория', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    genre = models.ManyToManyField(Genre, verbose_name='жанры',
                                   related_name='titles')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Review(models.Model):
    pub_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        unique_together = ['author', 'title']


class Comment(models.Model):
    pub_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    text = models.TextField(
        verbose_name='Текст',
        max_length=255,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
