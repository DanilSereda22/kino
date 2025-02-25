from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('movies/', views.movie_list),
    path('movies/<int:pk>/', views.movie_detail),
    path("", views.MoviesView.as_view()),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path("search/", views.Search.as_view(), name='search'),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail"),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("json-filter/", views.JsonFilterMoviesView.as_view(), name='json_filter'),
]
urlpatterns = format_suffix_patterns(urlpatterns)