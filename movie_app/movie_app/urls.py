from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from data.views import LoginAPI
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from data.views import movie_list, movie_detail, add_review, add_to_watchlist, watchlist, json_view,login_view 



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
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Movie_data/', json_view, name='json_view'),
    path('', movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/review/', add_review, name='add_review'),
    path('movies/<int:movie_id>/watchlist/', add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/', watchlist, name='watchlist'),
    path("Authorization/login", LoginAPI.as_view(), name="login"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
