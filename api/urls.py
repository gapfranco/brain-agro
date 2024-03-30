"""
URL mappings for the user API.
"""

from django.urls import path

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
]
