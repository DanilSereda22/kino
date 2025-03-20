from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from movies.views import api_root, MovieViewSet, UserViewSet


router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'users', UserViewSet, basename='user')


# Базовые представления для ViewSet
movie_list = MovieViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
movie_detail = MovieViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', api_root, name='api-root'), 
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls'))
]
urlpatterns += router.urls

urlpatterns += format_suffix_patterns([
    path('movies/', movie_list, name='movie-list'),
    path('movies/<int:pk>/', movie_detail, name='movie-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
])