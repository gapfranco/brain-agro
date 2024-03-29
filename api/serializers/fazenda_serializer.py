from django.db.models import Sum
from rest_framework import serializers

from base.models import Cultura, Fazenda
from base.util import valida_areas, valida_cnpj_cpf


class CulturaSerializer(serializers.ModelSerializer):
    cultura = serializers.CharField(source="tipo_cultura")

    class Meta:
        model = Cultura
        fields = [
            "cultura",
            "area",
        ]

    def validate_cultura(self, value):
        if value not in [tipo[0] for tipo in Cultura.TIPOS_CULTURA]:
            raise serializers.ValidationError(f"Cultura inválida: {value}")
        return value

    def validate_area(self, value):
        if value <= 0:
            raise serializers.ValidationError("Área deve ser maior que zero")
        return value


class FazendaSerializer(serializers.ModelSerializer):
    culturas = CulturaSerializer(many=True, read_only=False)

    class Meta:
        model = Fazenda
        fields = [
            "id",
            "codigo",
            "nome_fazenda",
            "nome_produtor",
            "cidade",
            "uf",
            "area_total",
            "area_vegetacao",
            "area_cultura",
            "culturas",
        ]

    def validate_codigo(self, value):
        if not valida_cnpj_cpf(value):
            raise serializers.ValidationError("CPF ou CNPJ inválido")
        return value

    def validate(self, data):
        if (
            "area_total" in data
            and "area_cultura" in data
            and "area_vegetacao" in data
        ):
            msgs = valida_areas(
                data["area_total"],
                data["area_cultura"],
                data["area_vegetacao"],
            )
            if msgs:
                raise serializers.ValidationError(msgs)
        return data

    def create(self, validated_data):
        culturas = validated_data.pop("culturas")
        fazenda = Fazenda(**validated_data)
        plantio = sum(cult["area"] for cult in culturas)
        if plantio > fazenda.area_cultura:
            raise serializers.ValidationError("Área total de cultura inválido")
        fazenda.save()
        for cult in culturas:
            Cultura.objects.create(fazenda=fazenda, **cult)
        return fazenda

    def update(self, instance, validated_data):
        culturas = []
        if "culturas" in validated_data:
            plantio = sum(cult["area"] for cult in culturas)
            culturas = validated_data.pop("culturas")
        else:
            tot_culturas = Cultura.objects.filter(fazenda=instance).aggregate(
                Sum("area")
            )
            plantio = tot_culturas["area__sum"]

        for field, value in validated_data.items():
            setattr(instance, field, value)
        msgs = valida_areas(
            instance.area_total, instance.area_cultura, instance.area_vegetacao
        )
        if msgs:
            raise serializers.ValidationError(msgs)
        if plantio > instance.area_cultura:
            raise serializers.ValidationError(
                "Área total de culturas inválida"
            )
        instance.save()
        if culturas:
            Cultura.objects.filter(fazenda=instance).delete()
            for cult in culturas:
                Cultura.objects.create(fazenda=instance, **cult)
        return instance
