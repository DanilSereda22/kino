from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from movies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path("", views.MoviesView.as_view(), name='home'),  # Main page with movies
    path("api/", include("movies.urls")),  # API endpoints - moved up for priority
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path("search/", views.Search.as_view(), name='search'),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),  # Moved below api/
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail"),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("json-filter/", views.JsonFilterMoviesView.as_view(), name='json_filter'),
]

urlpatterns += i18n_patterns(
    path('accounts/', include('allauth.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)