from django.db import models
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    overview = models.TextField()
    poster = models.ImageField(upload_to='movies/posters/', null=True, blank=True)
    rating = models.FloatField(default=0.0)
    genres = models.ManyToManyField(Genre)
    trailer_url = models.URLField(blank=True, null=True)  # Added trailer URL field

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating}/10)"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlists')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

class Actor(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='actors/', blank=True, null=True)

    def __str__(self):
        return self.name

class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='cast')
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.actor.name} as {self.role} in {self.movie.title}"
class MovieListView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of top movies",
        responses={200: openapi.Response("Success")}
    )
    def get(self, request):
        return Response({"message": "List of movies"})
    
class CustomLogin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # You can store hashed passwords in a real app

    def __str__(self):
        return self.username


