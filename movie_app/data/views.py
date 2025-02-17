from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Review, Watchlist
from .forms import ReviewForm
from .LoginSerializer import LoginSerializer  # Import LoginSerializer
from .UserSerializer import UserSerializer 
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .LoginSerializer import LoginSerializer, UserSerializer
from rest_framework import serializers  # ✅ Ensure this is imported
from .LoginSerializer import LoginSerializer, UserSerializer  # ✅ Import from the correct file
from rest_framework.decorators import api_view
from drf_yasg import openapi  # This line is necessary for openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Creating a default user for testing (if you don't already have one)
default_user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'password': make_password('testpassword')}  # Hashing the password
)


@swagger_auto_schema(method='get', operation_summary="Retrieve items")
@api_view(['GET'])
def your_view(request):
    # You can replace the following with your actual logic
    data = {
        'message': 'This is your API view'
    }
    return JsonResponse(data)@swagger_auto_schema(method='get', operation_summary="Retrieve JSON data")
@swagger_auto_schema(method='get', operation_summary="Retrieve JSON data")
@api_view(['GET'])
def json_view(request):
    movies = Movie.objects.all()  # Query all movies

    # Convert movie objects to JSON format
    movies_list = [
        {
            "id": movie.id,
            "title": movie.title,
            "release_date": movie.release_date.strftime("%Y-%m-%d"),  # Convert DateField to string
            "poster": movie.poster.url if movie.poster else None,  # Return full URL if poster exists
            "rating": movie.rating,
            "genres": [genre.name for genre in movie.genres.all()],# Convert ManyToManyField
            "movie_detail": {
                "title": movie.title,
                "release_date": movie.release_date.strftime("%Y-%m-%d"),
                "overview": movie.overview,
                "poster": movie.poster.url if movie.poster else None,
                "trailer_url": movie.trailer_url
            },
            "trailer_url": movie.trailer_url
        }
        for movie in movies
    ]

    data = {
        "message": "List of movies",
        "status": "success",
        "movies": movies_list
    }

    return JsonResponse(data, safe=False)


def update_movie_poster(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.poster = 'path/to/your/image.jpg'  
    movie.save()

    return render(request, 'some_template.html', {'movie': movie})
def movie_list(request):
    movies = Movie.objects.all()  # Assuming you're querying movies from the database
    return render(request, 'movies/movie_list.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all()
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'reviews': reviews})

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = ReviewForm()
    return render(request, 'movies/add_review.html', {'form': form, 'movie': movie})

@login_required
def add_to_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user, movie=movie)
    if not created:
      messages.info(request, "This movie is already in your watchlist.")
    return redirect('movie_detail', movie_id=movie.id)


@login_required
def watchlist(request):
    watchlist_movies = Watchlist.objects.filter(user=request.user)
    return render(request, 'movies/watchlist.html', {'watchlist_movies': watchlist_movies})

class LoginAPI(APIView):
    permission_classes = []  # Do not require authentication for login
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        operation_description="User login endpoint to obtain JWT tokens",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response('Login Successful', UserSerializer),
            400: openapi.Response('Invalid Credentials'),
            401: openapi.Response('Invalid Login Credentials'),
        }
    )
    def post(self, request):
        if not request.data:
            return Response({"error": "No data received. Ensure Content-Type is application/json."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # Authenticate the user with provided credentials
            user = authenticate(username=username, password=password)
            
            if user:
                # Generate Refresh and Access Tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)  # Generate Access Token

                return Response({
                    'access': access_token,
                    'refresh': str(refresh),  # Return the Refresh Token
                    'user': UserSerializer(user).data  # Return user info (optional)
                }, status=status.HTTP_200_OK)
            
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

def login_view(request):
    return render(request, 'movies/login.html')    
