from django.urls import path
from philbizz_api.views.account_views import AccountCreationView, AccountLoginView
from philbizz_api.views.menu.menu_views import MenuView, MenuListView
from philbizz_api.views.blog.blog_views import BlogView, BlogLikeView, CommentView
from philbizz_api.views.cms.cms_views import CMSView
from philbizz_api.views.navbar.navbar_view import NavbarView, NavbarListView
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from philbizz_api.views.auth.auth_views import ValidateTokenizeView
from rest_framework_simplejwt.views import TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Philbizz API",
        default_version="v1",
        description="Philbizz API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="devopsbyte60@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "accounts/create", AccountCreationView.as_view(), name="account_create"
    ),  # Adjusted path
    path("accounts/login", AccountLoginView.as_view(), name="account_login"),
    path(
        "auth/validate-tokenize-information",
        ValidateTokenizeView.as_view(),
        name="account_validate-tokenize-information",
    ),
    path("auth/menus/creation", MenuView.as_view(), name="account_menu"),
    path("app/get-menus", MenuListView.as_view(), name="app_get_menus"),
    path("app/blogs", BlogView.as_view(), name="blog-list-create"),
    path("app/blogs/<uuid:blog_id>/like/", BlogLikeView.as_view(), name="blog-like"),
    path("app/blogs/<uuid:blog_id>/likes/", BlogLikeView.as_view(), name="blog-likes"),
    path(
        "app/blogs/<uuid:blog_id>/comments/",
        CommentView.as_view(),
        name="blog-comments",
    ),
    path("auth/post-card-content/", CMSView.as_view(), name="auth_post_card_content"),
    path("auth/navbar/creation", NavbarView.as_view(), name="auth_post_navbar_content"),
    path("app/navbar-list", NavbarListView.as_view(), name="navbar-list"),
    path("app/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "swagger.json/", schema_view.without_ui(cache_timeout=0), name="schema-json"
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]
