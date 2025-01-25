from django.urls import path
from article import views
urlpatterns = [
    path('api/capitals/', views.GetCapitalInfoView.as_view()),
    path('main/', views.main_page, name='main_page'),
]