"""
URL mappings for the user API.
"""

from django.urls import path

from api.views import (
    AlteraFazendaView,
    CriaFazendaView,
    DeletaFazendaView,
    QueryView,
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
]
