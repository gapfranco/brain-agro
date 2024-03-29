import pytest

from api.serializers.fazenda_serializer import FazendaSerializer


class TestFazendaSerializers:
    """Fazenda serializers"""

    # @pytest.mark.django_db(reset_sequences=True)
    def test_fazenda_valida(
        self,
        get_payload_fazenda: pytest.fixture,
    ):
        """Test serializer with success"""
        request = get_payload_fazenda
        incoming_request = FazendaSerializer(
            data={
                **request,
            }
        )
        assert incoming_request.is_valid()

    def test_fazenda_invalida(
        self,
        get_payload_fazenda: pytest.fixture,
    ):
        """Test serializer with success"""
        request = get_payload_fazenda
        request["codigo"] = "12345678901234"
        incoming_request = FazendaSerializer(
            data={
                **request,
            }
        )
        assert not incoming_request.is_valid()
        assert "codigo" in incoming_request.errors
