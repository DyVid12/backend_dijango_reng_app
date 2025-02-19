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
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# Creating a default user for testing (if you don't already have one)
default_user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'password': make_password('testpassword')}  # Hashing the password

)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from django.db.models import Q
from .models import Movie

# Define the Swagger parameters for the search query
search_query_param = openapi.Parameter(
    'q', openapi.IN_QUERY,
    description="Search for a movie by title",
    type=openapi.TYPE_STRING
)

search_query_param = openapi.Parameter(
    'q', openapi.IN_QUERY,
    description="Search for a movie by title",
    type=openapi.TYPE_STRING
)

@swagger_auto_schema(
    method='get',
    operation_description="Search movies by title",
    manual_parameters=[search_query_param],  # Add query parameter for documentation
    responses={
        200: openapi.Response(
            description="Movies matching the search criteria",
            examples={
                "application/json": {
                    "status": "success",
                    "movies": [
                        {
                            "id": 1,
                            "title": "Movie Title",
                            "release_date": "2025-02-19",
                            "poster": "https://example.com/poster.jpg",
                            "rating": 8.5,
                            "movie_detail": {
                                "title": "Movie Title",
                                "release_date": "2025-02-19",
                                "overview": "This is a brief overview of the movie.",
                                "poster": "https://example.com/poster.jpg",
                                "trailer_url": "https://example.com/trailer.mp4"
                            }
                        }
                    ]
                }
            }
        )
    }
)
@api_view(['GET'])
def search_movies_by_title(request):
    query = request.GET.get('q', None)  # Get the search query from the URL parameter 'q'
    
    if query:
        # Filter movies where the title contains the query (case-insensitive)
        movies = Movie.objects.filter(Q(title__icontains=query))
        movies_list = [
            {
                "id": movie.id,
                "title": movie.title,
                "release_date": movie.release_date.strftime("%Y-%m-%d"),
                "poster": movie.poster.url if movie.poster else None,
                "rating": movie.rating,
                "movie_detail": {
                    "title": movie.title,
                    "release_date": movie.release_date.strftime("%Y-%m-%d"),
                    "overview": movie.overview if hasattr(movie, 'overview') else "No overview available",
                    "poster": movie.poster.url if movie.poster else None,
                    "trailer_url": movie.trailer_url
                }
            }
            for movie in movies
        ]
        return JsonResponse({"status": "success", "movies": movies_list}, safe=False)
    else:
        # If no query, return an empty list
        return JsonResponse({"status": "success", "movies": []}, safe=False)
# Assuming group_movies_by_category() is a function that returns categorized movie data
def group_movies_by_category():
    return {
        "Action": [
            {
                "id": 1,
                "title": "Movie Title",
                "release_date": "2025-02-19",
                "poster": "https://example.com/poster.jpg",
                "rating": 8.5,
                "trailer_url": "https://example.com/trailer.mp4"
            }
        ],
        # More categories (e.g., Romance, Comedy, etc.) can go here
    }

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve movies grouped by category",
    responses={ 
        200: openapi.Response(
            description="Movies grouped by category",
            examples={ 
                "application/json": {
                    "status": "success",
                    "movies_by_category": {
                        "Action": [
                            {
                                "id": 1,
                                "title": "Movie Title",
                                "release_date": "2025-02-19",
                                "poster": "https://example.com/poster.jpg",
                                "rating": 8.5,
                                "movie_detail": {
                                    "title": "Movie Title",
                                    "release_date": "2025-02-19",
                                    "overview": "This is a brief overview of the movie.",
                                    "poster": "https://example.com/poster.jpg",
                                    "trailer_url": "https://example.com/trailer.mp4"
                                }
                            }
                        ]
                    }
                }
            }
        )
    }
)
@api_view(['GET'])
def movies_by_category(request, category):
    # Fetch movies grouped by category
    categorized_movies = group_movies_by_category()

    if category not in categorized_movies:
        return JsonResponse({"status": "error", "message": "Category not found"}, status=404)

    movies_in_category = categorized_movies[category]
    
    # Format the categorized movies to include 'movie_detail' for each movie
    result = []
    for movie in movies_in_category:
        # Build the movie_detail dictionary
        movie_detail = {
            "title": movie['title'],
            "release_date": movie['release_date'],
            "overview": movie.get('overview', 'No overview available'),
            "poster": movie['poster'],
            "trailer_url": movie['trailer_url']  # Keep trailer_url in movie_detail
        }
        
        # Remove trailer_url from the main movie object
        movie.pop('trailer_url', None)

        # Add movie_detail to the movie
        movie['movie_detail'] = movie_detail

        result.append(movie)

    return JsonResponse({
        "status": "success",
        "movies_by_category": {category: result}
    }, safe=False)




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

class CustomRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

swagger_security_scheme = {
    "type": "apiKey",
    "in": "header",
    "name": "Authorization",
    "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
}

drf_yasg_security = [swagger_security_scheme]

class CustomRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

class RegisterAPI(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        operation_description="User registration endpoint",
        security=drf_yasg_security,
        request_body=CustomRegisterSerializer,
        responses={
            201: openapi.Response('Registration Successful'),
            400: openapi.Response('Invalid Data'),
        }
    )
    def post(self, request):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            gender = serializer.validated_data['gender']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(email=email).exists():
                return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "gender": gender,
                    "role": "user"
                },
                "access_token": access_token
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def register_view(request):
    return render(request, 'movies/register.html')

def group_movies_by_category():
    categories = {}
    movies = Movie.objects.all()
    
    for movie in movies:
        for genre in movie.genres.all():  # Assuming a ManyToMany relationship
            if genre.name not in categories:
                categories[genre.name] = []
            
            categories[genre.name].append({
                "id": movie.id,
                "title": movie.title,
                "release_date": movie.release_date.strftime("%Y-%m-%d"),
                "poster": movie.poster.url if movie.poster else None,
                "rating": movie.rating,
                "trailer_url": movie.trailer_url
            })
    
    return categories