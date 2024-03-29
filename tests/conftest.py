"""Main tests configuration"""

# Put this in your conftest.py
from pytest import fixture
from rest_framework.test import APIClient

from base.models import Fazenda, User


@fixture
def api_client():
    """ApiClient Fixture"""
    return APIClient


@fixture
def user_password():
    return "testpass123"


@fixture
def user(user_password):
    test_username = "testuser@test.com"
    user = User.objects.create_user(
        email=test_username, password=user_password
    )
    return user


@fixture
def get_payload_fazenda():
    return {
        "codigo": "07164374813",
        "nome_fazenda": "Kiwi",
        "nome_produtor": "Aurora",
        "cidade": "Ribeirão Preto",
        "uf": "SP",
        "area_total": 300,
        "area_vegetacao": 80,
        "area_cultura": 200,
        "culturas": [
            {"cultura": "Soja", "area": 100},
            {"cultura": "Cana", "area": 30},
            {"cultura": "Algodão", "area": 40},
        ],
    }


@fixture
def get_fields_fazenda():
    return {
        "codigo": "07164374813",
        "nome_fazenda": "Kiwi",
        "nome_produtor": "Aurora",
        "cidade": "Ribeirão Preto",
        "uf": "SP",
        "area_total": 300,
        "area_vegetacao": 80,
        "area_cultura": 200,
    }


@fixture
def cria_fazendas(get_fields_fazenda):
    payload = get_fields_fazenda
    fazenda = Fazenda(**payload)
    fazenda.save()
