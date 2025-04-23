from typing import Any
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Movie, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm
from .serializers import MovieSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User
from movies.serializers import UserSerializer,PasswordSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer
from rest_framework.renderers import JSONRenderer,TemplateHTMLRenderer
from rest_framework.views import APIView

    
class UserCountView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        user_count = User.objects.filter(active=True).count()
        content = {'user_count': user_count}
        return Response(content)
    
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'movies': reverse('movie-list', request=request, format=format)
    })

class UserCountView(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        user_count = User.objects.filter(active=True).count()
        content = {'user_count': user_count}
        return Response(content)

           
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, AdminRenderer]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def set_groups(self, request, pk=None):
        user = self.get_object()
        
        if not request.user.is_superuser:  # Предположим, только админы могут менять группы
            return Response(
                {'error': 'У вас нет прав для изменения групп.'},
                status=status.HTTP_403_FORBIDDEN
            )

        group_ids = request.data.get('group_ids', [])
        groups = Group.objects.filter(id__in=group_ids)
        user.groups.set(groups)  # Правильное использование метода set()

        return Response({'status': 'Группы обновлены'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        if request.user.is_superuser:
            self.perform_destroy(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.user == user:
            self.perform_destroy(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'error': 'Вы можете удалить только свою учетную запись или должны быть администратором.'},
            status=status.HTTP_403_FORBIDDEN
        )

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')
        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, AdminRenderer]

    @action(detail=True)
    def highlight(self, request, *args, **kwargs):
        movie = self.get_object()
        return Response(movie.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'user': self.object}, template_name='user_detail.html')


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GenreYear:
    """Жанры и года выхода фильма"""
    def get_genres(self):
        return Genre.objects.all()
    def get_years(self):
        return Movie.objects.order_by("-year").values_list("year", flat=True).distinct()
    
class MoviesView(GenreYear,ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movies.html"
    paginate_by = 6
             
class MovieDetailView(GenreYear,DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = "url" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm
        return context

class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie  # Установите фильм для отзыва
            form.save()
        return redirect(movie.get_absolute_url())
    
class ActorView(GenreYear,DetailView):
    """Вывод информации о актере"""    
    model=Actor
    template_name="movies/actor.html"
    slug_field="name"
    
class FilterMoviesView(GenreYear,ListView):
    """Фильтр фильмов"""
    paginate_by = 3
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context
    
class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)

class Search(ListView):
    """Поиск фильмов"""
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
    