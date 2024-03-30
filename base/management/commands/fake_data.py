"""Gera fake data"""

import random

from django.core.management.base import BaseCommand
from faker import Faker

from base.models import Cultura, Fazenda


class Command(BaseCommand):  # pragma: no cover
    help = "Gerador de dados fake"

    def handle(self, *args, **kwargs):
        fake = Faker("pt_BR")
        for _ in range(10):
            area_total = fake.random_int(min=50, max=500)
            area_cultura = fake.random_int(min=10, max=150)
            area_vegetacao = area_total - area_cultura
            fazenda = Fazenda.objects.create(
                codigo=fake.cpf(),
                nome_fazenda=fake.company(),
                nome_produtor=fake.name(),
                cidade=fake.city(),
                uf=fake.state_abbr(),
                area_total=area_total,
                area_cultura=area_cultura,
                area_vegetacao=area_vegetacao,
            )

            qtd_cult = fake.random_int(min=1, max=4)
            areas = self.divide_number(area_cultura, qtd_cult)
            for area in areas:
                Cultura.objects.create(
                    fazenda=fazenda,
                    tipo_cultura=fake.random_element(Cultura.TIPOS_CULTURA)[0],
                    area=area,
                )

    def divide_number(self, total, slices):
        # Gera n-1 pontos de divisão no intervalo 1...total
        div_points = sorted(random.sample(range(1, total), slices - 1))
        # Acrescenta os pontos finais do intervalo
        div_points = [0] + div_points + [total]
        # Calcula a diferença entre pontos de divisão
        # consecutivos para obter as 'fatias'
        return [div_points[i + 1] - div_points[i] for i in range(slices)]
