from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views import defaults as default_views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="P2P network API",
        default_version="v1",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="tinenourelhouda@@gmail.com"),
        license=openapi.License(name="Propritary License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("", include("p2p_app.urls", namespace="api")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
