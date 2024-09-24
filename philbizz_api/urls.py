from django.urls import path
from philbizz_api.views.account_views import AccountCreationView, AccountLoginView
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Philbizz API",
        default_version='v1',
        description="Philbizz API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="devopsbyte60@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('accounts/create', AccountCreationView.as_view(), name='account_create'),  # Adjusted path
    path('accounts/login', AccountLoginView.as_view(), name='account_login'),
]

if settings.DEBUG:
    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]