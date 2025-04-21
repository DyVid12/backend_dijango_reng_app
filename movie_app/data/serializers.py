# movie_app/data/serializers.py

from rest_framework import serializers
from .models import  Watchlist
from .models import Movie
from .models import Review  # Assuming your Review model is in models.py

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)  # Include the username

    class Meta:
        model = Review
        fields = ['id', 'movie', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'movie', 'created_at']

        
class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ['user', 'movie']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_date', 'poster', 'rating', 'overview', 'trailer_url']         