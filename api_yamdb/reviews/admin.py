from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title

reviews_models = (Title, Category, Genre, Review, Comment)
admin.site.register(reviews_models)
