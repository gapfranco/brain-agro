from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.fazenda_serializer import FazendaSerializer
from api.serializers.query_serializers import QuerySerializer
from base.models import Fazenda


class QueryView(APIView):
    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid():
            cidade = request.data.get("cidade")
            uf = request.data.get("uf")
            culturas = request.data.get("culturas")
            lista_culturas = [item.strip() for item in culturas.split(",")]
            fazendas = Fazenda.objects.all()
            if cidade:
                fazendas = fazendas.filter(Q(cidade__iexact=cidade))
            if uf:
                fazendas = fazendas.filter(Q(uf__iexact=uf))
            if culturas:
                fazendas = fazendas.filter(
                    culturas__tipo_cultura__in=lista_culturas
                )

            serializer = FazendaSerializer(fazendas, many=True)
            return JsonResponse(serializer.data, safe=False)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CriaFazendaView(APIView):
    def post(self, request):
        serializer = FazendaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlteraFazendaView(APIView):
    def patch(self, request, fazenda_id):
        fazenda = Fazenda.objects.get(id=fazenda_id)
        serializer = FazendaSerializer(
            fazenda, partial=True, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletaFazendaView(APIView):
    def delete(self, request, fazenda_id):
        fazenda = Fazenda.objects.get(id=fazenda_id)
        fazenda.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
