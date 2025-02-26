from rest_framework import serializers
from .models import Movie, Actor, Genre, Category  
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'movies']

class MovieSerializer(serializers.ModelSerializer):
    directors = serializers.PrimaryKeyRelatedField(many=True, queryset=Actor.objects.all())
    actors = serializers.PrimaryKeyRelatedField(many=True, queryset=Actor.objects.all())
    genres = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'tagline', 'description', 'poster', 
            'year', 'country', 'directors', 'actors', 'genres', 
            'world_premiere', 'budget', 'fees_in_usa', 'fees_in_world',  # Исправлено здесь
            'category', 'url', 'draft'
        ]

    def create(self, validated_data):
        """Create and return a new `Movie` instance, given the validated data."""
        directors_data = validated_data.pop('directors')
        actors_data = validated_data.pop('actors')
        genres_data = validated_data.pop('genres')
        
        movie = Movie.objects.create(**validated_data)
        movie.directors.set(directors_data)
        movie.actors.set(actors_data)
        movie.genres.set(genres_data)
        return movie

    def update(self, instance, validated_data):
        """Update and return an existing `Movie` instance, given the validated data."""
        directors_data = validated_data.pop('directors', None)
        actors_data = validated_data.pop('actors', None)
        genres_data = validated_data.pop('genres', None)

        instance.title = validated_data.get('title', instance.title)
        instance.tagline = validated_data.get('tagline', instance.tagline)
        instance.description = validated_data.get('description', instance.description)
        instance.poster = validated_data.get('poster', instance.poster)
        instance.year = validated_data.get('year', instance.year)
        instance.country = validated_data.get('country', instance.country)
        instance.world_premiere = validated_data.get('world_premiere', instance.world_premiere)
        instance.budget = validated_data.get('budget', instance.budget)
        instance.fees_in_usa = validated_data.get('fees_in_usa', instance.fees_in_usa)
        instance.fees_in_world = validated_data.get('fees_in_world', instance.fees_in_world)  # Исправлено здесь
        instance.category = validated_data.get('category', instance.category)
        instance.url = validated_data.get('url', instance.url)
        instance.draft = validated_data.get('draft', instance.draft)
        
        instance.save()
        
        if directors_data is not None:
            instance.directors.set(directors_data)
        if actors_data is not None:
            instance.actors.set(actors_data)
        if genres_data is not None:
            instance.genres.set(genres_data)

        return instance