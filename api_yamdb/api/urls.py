from django.urls import include, path
from rest_framework import routers

from api.views import CategoriesViewSet, GeneresViewSet, TitlesViewSet
from users.views import CreateUserView

router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('genres', GeneresViewSet, basename='genres')
router_v1.register('titles', TitlesViewSet, basename='titles')

api_v1_patterns = [
    path('', include(router_v1.urls)),
    path(
        'users/',
        CreateUserView.as_view(),
        name='create_user'
    ),
    path('auth/', include('users.urls')),
]

urlpatterns = [
    path('v1/', include(api_v1_patterns))
]
