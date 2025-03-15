from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from movies.views import api_root, MovieViewSet, UserViewSet,UserList
from movies import views
from rest_framework import renderers
from django.contrib.auth.models import User
from movies.serializers import UserSerializer
from rest_framework.generics import ListCreateAPIView

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

# URL-шаблоны
urlpatterns = [
    path('', include(router.urls)),
    path("", views.MoviesView.as_view()),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path("search/", views.Search.as_view(), name='search'),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail"),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("json-filter/", views.JsonFilterMoviesView.as_view(), name='json_filter'),
]

urlpatterns += format_suffix_patterns([
    path('', api_root),
    path('movies/', movie_list, name='movie-list'),
    path('movies/<int:pk>/', movie_detail, name='movie-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
])

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]