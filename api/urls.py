"""
URL mappings for the user API.
"""

from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.views import (
    AlteraFazendaView,
    CriaFazendaView,
    DeletaCulturasView,
    DeletaFazendaView,
    QueryView,
    ResumoCulturasUFView,
    ResumoCulturasView,
    ResumoEstadosView,
    ResumoView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Agro API",
        default_version="v1",
        description="Agro",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="gapfranco@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("query/", QueryView.as_view(), name="query"),
    path("cria_fazenda/", CriaFazendaView.as_view(), name="cria"),
    path(
        "altera_fazenda/<int:fazenda_id>",
        AlteraFazendaView.as_view(),
        name="altera",
    ),
    path(
        "exclui_fazenda/<int:fazenda_id>",
        DeletaFazendaView.as_view(),
        name="exclui",
    ),
    path(
        "exclui_culturas/<int:fazenda_id>",
        DeletaCulturasView.as_view(),
        name="exclui",
    ),
    path("resumo/", ResumoView.as_view(), name="resumo"),
    path(
        "resumo_estados/", ResumoEstadosView.as_view(), name="resumo_estados"
    ),
    path(
        "resumo_culturas/",
        ResumoCulturasView.as_view(),
        name="resumo_culturas",
    ),
    path(
        "resumo_uf_culturas/",
        ResumoCulturasUFView.as_view(),
        name="resumo_culturas",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
