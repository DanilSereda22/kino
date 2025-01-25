from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('article.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('pages/',include('django.contrib.flatpages.urls')),
    path("",include("movies.urls")),
    path("",include("article.urls")),
    path('', include('snippets.urls')),
]

urlpatterns += i18n_patterns(
    path('accounts/', include('allauth.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path("", include("movies.urls")),
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)