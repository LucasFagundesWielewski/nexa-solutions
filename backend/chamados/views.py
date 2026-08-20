from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import Chamado
from .serializers import ChamadoSerializer


class ChamadoListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria chamados.

    A listagem aceita filtro opcional por status via `?status=`.
    """

    serializer_class = ChamadoSerializer

    def get_queryset(self):
        queryset = Chamado.objects.all().order_by("-criado_em")
        status_param = self.request.query_params.get("status")

        if status_param:
            valid_statuses = Chamado.Status.values
            if status_param not in valid_statuses:
                raise ValidationError(
                    {
                        "status": (
                            f"Status inválido: '{status_param}'. "
                            f"Valores aceitos: {', '.join(valid_statuses)}."
                        )
                    }
                )
            queryset = queryset.filter(status=status_param)

        return queryset


class ChamadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer