from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Metsenat',
        description='Metsenat loyihasi nusxasi',
        default_version='v1',
        terms_of_service='https://www.google.com/policies/terms',
        contact=openapi.Contact(email='xurshidolimov017@gmail.com'),
        license=openapi.License(name='Metsenat litsenziyasi'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('user/', include('dj_rest_auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc'),
]
