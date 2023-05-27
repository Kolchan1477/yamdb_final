from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, get_token, registration

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router = DefaultRouter()
router.register('categories', CategoryViewSet, 'categories')
router.register('users', UserViewSet, 'users')
router.register('genres', GenreViewSet, 'genres')
router.register('titles', TitleViewSet, 'titles')
router.register(r'titles/(?P<title_id>[\d]+)/reviews', ReviewViewSet,
                'reviews')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    'comments'
)

api_version = 'v1'

urlpatterns = [
    path(f'{api_version}/', include(router.urls)),
    path(f'{api_version}/auth/signup/', registration, name='registration'),
    path(f'{api_version}/auth/token/', get_token, name='auth_token'),
]
