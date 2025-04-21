from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from data.views import LoginAPI,RegisterAPI
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from data.views import movie_list, movie_detail, add_review, add_to_watchlist, watchlist, json_view,search_movies_by_category,search_movies_by_title,movie_data_view,get_reviews_for_movie
# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Rerng App API",
        default_version='v1',
        description="API documentation for Rerng _រឿង movie tracking app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Allow public access to Swagger
)

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('movie_data/', movie_data_view, name='movie_data'),
    path('Movie_data/', json_view, name='json_view'),
    path('', movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/review/', add_review, name='add_review'),
    path('movies/<int:movie_id>/watchlist/', add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/', watchlist, name='watchlist'),
    path('Authorization/register', RegisterAPI.as_view(), name='register'),
    path('Movie_data/search_movies_by_category/<str:category>/', search_movies_by_category, name='search_movies_by_category'),
    path('Movie_data/search_movies_by_title/', search_movies_by_title, name='search_movies_by_title'),
     path('movie/<int:movie_id>/reviews/', get_reviews_for_movie, name='get_reviews_for_movie'),
    # Custom login API
    path('Authorization/login', LoginAPI.as_view(), name='login'),
    # Swagger UI and ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^rerngapp(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
