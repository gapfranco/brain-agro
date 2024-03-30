from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.fazenda_serializer import FazendaSerializer
from api.serializers.query_serializers import QuerySerializer
from base.models import Cultura, Fazenda


class QueryView(APIView):
    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid():
            id = request.data.get("id")
            cidade = request.data.get("cidade")
            uf = request.data.get("uf")
            culturas = request.data.get("culturas")
            if culturas:
                lista_culturas = [item.strip() for item in culturas.split(",")]
            else:
                lista_culturas = []
            fazendas = Fazenda.objects.all()
            if id:
                fazendas = fazendas.filter(id=id)
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
        try:
            fazenda = Fazenda.objects.get(id=fazenda_id)
            fazenda.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(
                "Erro de leitura da fazenda (existe?)",
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeletaCulturasView(APIView):
    def get(self, request, fazenda_id):
        try:
            Cultura.objects.filter(fazenda_id=fazenda_id).delete()
            fazenda = Fazenda.objects.get(id=fazenda_id)
            serializer = FazendaSerializer(fazenda)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                "Erro de leitura da fazenda (existe?)",
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResumoView(APIView):
    def get(self, request):
        res = Fazenda.objects.all().aggregate(
            fazendas=Count("id"),
            area_total=Sum("area_cultura"),
            area_cultura=Sum("area_cultura"),
            area_vegetacao=Sum("area_vegetacao"),
        )
        return Response(res, status=status.HTTP_200_OK)


class ResumoEstadosView(APIView):
    def get(self, request):
        res = Fazenda.objects.values("uf").annotate(
            fazendas=Count("id"),
            area_total=Sum("area_total"),
            area_cultura=Sum("area_cultura"),
            area_vegetacao=Sum("area_vegetacao"),
        )
        return Response(res, status=status.HTTP_200_OK)


class ResumoCulturasUFView(APIView):
    def get(self, request):
        res = Cultura.objects.values("tipo_cultura", "fazenda__uf").annotate(
            total_area=Sum("area"),
        )
        return Response(res, status=status.HTTP_200_OK)


class ResumoCulturasView(APIView):
    def get(self, request):
        res = Cultura.objects.values("tipo_cultura").annotate(
            total_area=Sum("area"),
        )
        return Response(res, status=status.HTTP_200_OK)
