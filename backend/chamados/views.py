from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chamado
from .serializers import ChamadoSerializer


class ChamadoListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria chamados.

    Limitações intencionais:
    - Não filtra chamados por status.
    - Não há tratamento adicional para parâmetros inválidos.
    """

    queryset = Chamado.objects.all().order_by("-criado_em")
    serializer_class = ChamadoSerializer


class ChamadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer


class ChamadoIndicadoresView(APIView):
    """
    Retorna indicadores agregados sobre o volume de chamados.
    """

    def get(self, request):
        queryset = Chamado.objects.all()

        return Response(
            {
                "total": queryset.count(),
                "abertos": queryset.filter(status=Chamado.Status.ABERTO).count(),
                "em_andamento": queryset.filter(
                    status=Chamado.Status.EM_ANDAMENTO
                ).count(),
                "concluidos": queryset.filter(
                    status=Chamado.Status.CONCLUIDO
                ).count(),
            }
        )