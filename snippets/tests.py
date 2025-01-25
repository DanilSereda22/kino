from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from snippets import views
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)
urlpatterns = [
    path(r'', include(router.urls)),
    path('admin/', admin.site.urls),
]