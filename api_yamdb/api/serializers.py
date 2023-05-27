from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title

from .validators import validate_year


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        lookup_field = 'slug'
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        lookup_field = 'slug'
        exclude = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
        required=False,
        default=None
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        required=False,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = '__all__'
        unique_together = ('title', 'author')

    def validate(self, data):
        """
        Проверка на то, что пользователь может оставить не больше одного отзыва
        на произведение.
        """
        if (self.context.get('request').method == 'POST'
                and Review.objects.filter(
                    author=self.context.get('request').user,
                    title__id=self.context.get(
                        'view').kwargs.get('title_id')).exists()):
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение'
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False,
        required=True,
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )
    year = serializers.IntegerField(validators=(validate_year,))

    class Meta:
        fields = '__all__'
        model = Title


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(many=False, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        obj = obj.reviews.all().aggregate(rating=Avg('score'))

        return obj['rating']
