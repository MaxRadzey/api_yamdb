from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoriesViewSet,
    GeneresViewSet,
    TitlesViewSet,
    ReviewsViewSet,
    CommentsViewSet
)

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
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('genres', GeneresViewSet, basename='genres')
router_v1.register('titles', TitlesViewSet, basename='titles')

api_v1_patterns = [
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(api_v1_patterns))
]
