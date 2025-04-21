from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Review, Watchlist
from .forms import ReviewForm
from .LoginSerializer import LoginSerializer  # Import LoginSerializer
from .UserSerializer import UserSerializer 
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .LoginSerializer import LoginSerializer, UserSerializer
from rest_framework import serializers  # ✅ Ensure this is imported
from .LoginSerializer import LoginSerializer, UserSerializer  # ✅ Import from the correct file
from rest_framework.decorators import api_view,permission_classes
from drf_yasg import openapi  # This line is necessary for openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import WatchlistSerializer

from .serializers import ReviewSerializer
from .models import Watchlist, Movie
from .serializers import WatchlistSerializer, MovieSerializer

from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# Creating a default user for testing (if you don't already have one)
default_user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'password': make_password('testpassword')}  # Hashing the password

)


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
                                "rating": 8.5,
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
                    "rating": movie.rating,
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
                "id": 5,
                "title": "Creator of the Gods 2",
                "release_date": "2025-01-29",
                "poster": "/media/movies/posters/250111_CreationoftheGodsIIDemonForce_big.webp",
                "rating": 8,
                "trailer_url": "https://www.youtube.com/watch?v=nbYvqpf7A6M",
                "overview": "An epic sequel about gods and warriors battling for the fate of the world."  # ✅ ADD OVERVIEW HERE
            }
        ],
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
                                    "rating": 8.5,
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
def search_movies_by_category(request, category):
    """
    Retrieves movies filtered by a specific category.
    """
    movies = Movie.objects.filter(genres__name__iexact=category)  # Adjust field name if necessary

    if not movies.exists():
        return JsonResponse({"status": "error", "message": "Category not found"}, status=404)

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
                "overview": movie.overview if movie.overview and movie.overview.strip() else "No overview available",
                "rating": movie.rating,
                "poster": movie.poster.url if movie.poster else None,
                "trailer_url": movie.trailer_url
            }
        }
        for movie in movies
    ]

    return JsonResponse({
        "status": "success",
        "movies_by_category": {category: movies_list}
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
                "rating": movie.rating,
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

@swagger_auto_schema(
    method='post',
    operation_description="Add a review for a movie",
    request_body=ReviewSerializer,
    responses={201: "Review Created", 400: "Invalid Data"},
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=['post'],
    operation_description="Add a movie to the watchlist",
    responses={201: "Movie added to your watchlist!", 400: "Bad Request"}
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])  # ✅ Use JWT authentication
@permission_classes([IsAuthenticated])
def add_to_watchlist(request, movie_id):
    print(f"User: {request.user}")  
    print(f"Authenticated: {request.user.is_authenticated}")  
    print(f"Authorization Header: {request.headers.get('Authorization')}")  

    if not request.user.is_authenticated:
        return Response({'message': 'Authentication required to add to watchlist.'}, status=status.HTTP_401_UNAUTHORIZED)

    movie = get_object_or_404(Movie, id=movie_id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user, movie=movie)

    if not created:
        return Response({'message': 'This movie is already in your watchlist.'}, status=status.HTTP_200_OK)

    return Response({'message': 'Movie added to your watchlist!'}, status=status.HTTP_201_CREATED)



@swagger_auto_schema(
    method='get',
    operation_description="Retrieve the list of movies in the user's watchlist with detailed information",
    responses={200: MovieSerializer(many=True)}
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])  # ✅ Ensure JWT is used
@permission_classes([IsAuthenticated])
def watchlist(request):
    """
    Returns the list of movies with detailed information in the authenticated user's watchlist.
    """
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({'message': 'Authentication required.'}, status=401)

    # Fetch movies from the user's watchlist
    watchlist_movies = Watchlist.objects.filter(user=request.user)
    
    # Retrieve movie details based on the movies in the watchlist
    movies = []
    for entry in watchlist_movies:
        movie = Movie.objects.get(id=entry.movie.id)  # Assuming 'movie' is a ForeignKey in Watchlist
        movie_data = MovieSerializer(movie).data
        
        # Create a nested 'movie_detail' field
        movie_detail = {
            "title": movie_data['title'],
            "release_date": movie_data['release_date'],
            "overview": movie_data['overview'],
            "rating": movie_data['rating'],
            "poster": movie_data['poster'],
            "trailer_url": movie_data['trailer_url']
        }

        # Append to the movie list with 'movie_detail' nested
        movies.append({
            "id": movie_data['id'],
            "title": movie_data['title'],
            "release_date": movie_data['release_date'],
            "poster": movie_data['poster'],
            "rating": movie_data['rating'],
            "movie_detail": movie_detail  # Nested movie details
        })

    # Return the response with movie details
    return Response({
        'status': 'success',
        'movies': movies
    })
   

class LoginAPI(APIView):
    permission_classes = []  # Do not require authentication for login
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        operation_description="User login endpoint to obtain JWT tokens",
        request_body=LoginSerializer,
        responses={200: openapi.Response('Login Successful', UserSerializer),
                   400: openapi.Response('Invalid Credentials'),
                   401: openapi.Response('Invalid Login Credentials')}
    )
    def post(self, request):
        if not request.data:
            return Response({"error": "No data received. Ensure Content-Type is application/json."}, 
                             status=status.HTTP_400_BAD_REQUEST)

        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user:
                # Generate Refresh and Access Tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)  # Generate Access Token

                return Response({
                    'access': access_token,
                    'refresh': str(refresh),  # Return the Refresh Token
                    'user': UserSerializer(user).data  # This line should include the user's gender
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

def movie_data_view(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return JsonResponse({'success': True, 'data': serializer.data}, safe=False)


@swagger_auto_schema(
    method='get',
    operation_description="Retrieve all reviews for a specific movie",
    responses={200: ReviewSerializer(many=True)},
)
@api_view(['GET'])
def get_reviews_for_movie(request, movie_id):
    """
    Retrieves all reviews for a specific movie.
    """
    movie = get_object_or_404(Movie, id=movie_id)  # Fetch the movie based on movie_id
    reviews = Review.objects.filter(movie=movie)  # Get all reviews for this movie
    serializer = ReviewSerializer(reviews, many=True)  # Serialize reviews
    return Response(serializer.data, status=status.HTTP_200_OK)