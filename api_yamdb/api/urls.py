from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoriesViewSet,
    GenresViewSet,
    TitlesViewSet,
    ReviewsViewSet,
    CommentsViewSet
)
from users.views import UserView

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    r'categories',
    CategoriesViewSet,
    basename='categories'
)
router_v1.register(
    r'genres',
    GenresViewSet,
    basename='genres'
)
router_v1.register(
    'titles',
    TitlesViewSet,
    basename='titles'
)
router_v1.register(
    'users',
    UserView,
    basename='users'
)


api_v1_patterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('users.urls')),
]

urlpatterns = [
    path('v1/', include(api_v1_patterns))
]
