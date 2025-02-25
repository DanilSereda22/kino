# serializers.py
from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'tagline', 'description', 'poster', 
            'year', 'country', 'directors', 'actors', 'genres', 
            'world_premiere', 'budget', 'fees_in_usa', 'fess_in_world', 
            'category', 'url', 'draft'
        ]

    def create(self, validated_data):
        """Create and return a new `Movie` instance, given the validated data."""
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update and return an existing `Movie` instance, given the validated data."""
        instance.title = validated_data.get('title', instance.title)
        instance.tagline = validated_data.get('tagline', instance.tagline)
        instance.description = validated_data.get('description', instance.description)
        instance.poster = validated_data.get('poster', instance.poster)
        instance.year = validated_data.get('year', instance.year)
        instance.country = validated_data.get('country', instance.country)
        instance.directors.set(validated_data.get('directors', instance.directors.all()))
        instance.actors.set(validated_data.get('actors', instance.actors.all()))
        instance.genres.set(validated_data.get('genres', instance.genres.all()))
        instance.world_premiere = validated_data.get('world_premiere', instance.world_premiere)
        instance.budget = validated_data.get('budget', instance.budget)
        instance.fees_in_usa = validated_data.get('fees_in_usa', instance.fees_in_usa)
        instance.fess_in_world = validated_data.get('fess_in_world', instance.fess_in_world)
        instance.category = validated_data.get('category', instance.category)
        instance.url = validated_data.get('url', instance.url)
        instance.draft = validated_data.get('draft', instance.draft)
        instance.save()
        return instance