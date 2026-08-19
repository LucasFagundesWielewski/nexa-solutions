from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Chamado


class ChamadoIndicadoresTests(APITestCase):
    def setUp(self):
        self.url = reverse("chamado-indicadores")

    def test_indicadores_with_no_chamados_returns_zeroed_counts(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"total": 0, "abertos": 0, "em_andamento": 0, "concluidos": 0},
        )

    def test_indicadores_counts_chamados_by_status(self):
        Chamado.objects.create(titulo="Chamado 1", status=Chamado.Status.ABERTO)
        Chamado.objects.create(titulo="Chamado 2", status=Chamado.Status.ABERTO)
        Chamado.objects.create(
            titulo="Chamado 3", status=Chamado.Status.EM_ANDAMENTO
        )
        Chamado.objects.create(titulo="Chamado 4", status=Chamado.Status.CONCLUIDO)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"total": 4, "abertos": 2, "em_andamento": 1, "concluidos": 1},
        )
