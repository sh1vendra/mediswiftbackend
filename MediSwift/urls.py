from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

# Schema view for Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="MediSwift API",
        default_version="v1",
        description="API documentation for MediSwift",
        contact=openapi.Contact(email="nirmankhadka.aifiverse@gmail.com"),
        license=openapi.License(name="MediSwift License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# API URL patterns
api_urlpatterns = [
    path('v01/', include('v01.urls')),
]

# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger route
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
