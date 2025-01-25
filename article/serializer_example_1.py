import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from rest_framework import serializers


class User: 
    def __init__(self, username):
        self.username = username


class Capital: 
    def __init__(self, country, capital_city, capital_population, user: User):
        self.country = country
        self.capital_city = capital_city
        self.capital_population = capital_population
        self.author = user


author_obj = User('test_user') 
capital_1 = Capital('Norway', 'Oslo', 693500, author_obj)
capital_2 = Capital('Sweden ', 'Stockholm', 961600, author_obj)
capital_3 = Capital('Finland', 'Helsinki', 655300, author_obj)
capital_4 = Capital('Iceland', 'Reykjavik', 128800, author_obj)
queryset = [capital_1, capital_2, capital_3, capital_4]


class CapitalSerializer(serializers.Serializer):
    capital_city = serializers.CharField(max_length=200)
    capital_population = serializers.IntegerField()
    author = serializers.CharField(source='author.username',
                                   max_length=200)
serializer_obj = CapitalSerializer(instance=queryset, many=True)
print(serializer_obj.data)