from rest_framework import serializers


class QuerySerializer(serializers.Serializer):
    cidade = serializers.CharField(
        max_length=256, required=False, allow_blank=True
    )
    uf = serializers.CharField(max_length=2, required=False, allow_blank=True)
    culturas = serializers.CharField(
        max_length=256, required=False, allow_blank=True
    )
