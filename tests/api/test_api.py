import pytest

from base.models import Fazenda


class TestApiFazenda:
    @pytest.mark.django_db(reset_sequences=True)
    def test_cria_fazenda(
        self, get_payload_fazenda: pytest.fixture, api_client
    ):
        client = api_client()
        payload = get_payload_fazenda
        response = client.post(
            path="/api/cria_fazenda/", data=payload, format="json"
        )
        assert response.status_code == 201

    @pytest.mark.django_db(reset_sequences=True)
    def test_lista_fazendas(self, cria_fazendas: pytest.fixture, api_client):
        client = api_client()
        cria_fazendas
        cria_fazendas
        payload = {}
        response = client.post(path="/api/query/", data=payload, format="json")
        assert response.status_code == 200
        assert len(response.json()) == 1

    @pytest.mark.django_db(reset_sequences=True)
    def test_altera_fazenda(self, cria_fazendas: pytest.fixture, api_client):
        client = api_client()
        cria_fazendas
        payload = {"nome_fazenda": "nova"}
        response = client.patch(
            path="/api/altera_fazenda/1", data=payload, format="json"
        )
        assert response.status_code == 200
        retorno = response.json()
        assert retorno["nome_fazenda"] == "nova"

    @pytest.mark.django_db(reset_sequences=True)
    def test_exclui_fazenda(self, cria_fazendas: pytest.fixture, api_client):
        client = api_client()
        cria_fazendas
        response = client.delete(path="/api/exclui_fazenda/1", format="json")
        assert response.status_code == 204
        assert not Fazenda.objects.exists()
