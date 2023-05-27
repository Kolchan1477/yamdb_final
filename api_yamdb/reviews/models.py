from api.validators import validate_year
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    """Модель Категория"""
    name = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    class Meta:
        db_table = 'category'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель Жанр"""
    name = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    class Meta:
        db_table = 'genre'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель Произведение"""
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год релиза',
        validators=(validate_year,)
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
        blank=True,
        related_name='titles',
        db_column='category'
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        to=Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр',
        db_table='genre_title'
    )

    class Meta:
        db_table = 'titles'
        ordering = ('-year',)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_column='author'
    )
    score = models.IntegerField(
        validators=(
            MaxValueValidator(10),
            MinValueValidator(1)
        ),
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        verbose_name='Время создания отзыва',
        auto_now_add=True,
        db_index=True
    )
    title = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        db_table = 'review'
        ordering = ('-pub_date', 'score')
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            ),
        )


class Comment(models.Model):
    review = models.ForeignKey(
        to=Review,
        verbose_name='Идентификатор отзыва',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments',
        db_column='author'
    )
    pub_date = models.DateTimeField(
        verbose_name='Время создания отзыва',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        db_table = 'comments'
        ordering = ('-pub_date',)
