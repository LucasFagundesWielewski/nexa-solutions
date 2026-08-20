from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Chamado


class ChamadoTitleValidationTests(APITestCase):
    def setUp(self):
        self.url = reverse("chamado-list-create")

    def test_create_chamado_with_title_succeeds(self):
        payload = {
            "titulo": "Impressora não liga",
            "descricao": "A impressora do setor financeiro não liga.",
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chamado.objects.count(), 1)
        self.assertEqual(Chamado.objects.get().titulo, payload["titulo"])

    def test_create_chamado_without_title_returns_400(self):
        payload = {"descricao": "Chamado enviado sem título."}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("titulo", response.data)
        self.assertEqual(Chamado.objects.count(), 0)

    def test_create_chamado_with_blank_title_returns_400(self):
        payload = {"titulo": "", "descricao": "Chamado enviado com título vazio."}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("titulo", response.data)
        self.assertEqual(Chamado.objects.count(), 0)


class ChamadoStatusFilterTests(APITestCase):
    def setUp(self):
        self.url = reverse("chamado-list-create")

        Chamado.objects.create(titulo="Chamado aberto", status=Chamado.Status.ABERTO)
        Chamado.objects.create(
            titulo="Chamado em andamento", status=Chamado.Status.EM_ANDAMENTO
        )
        Chamado.objects.create(
            titulo="Chamado concluído", status=Chamado.Status.CONCLUIDO
        )

    def test_list_without_filter_returns_all_chamados(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_status_returns_only_matching_chamados(self):
        response = self.client.get(self.url, {"status": Chamado.Status.ABERTO})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], Chamado.Status.ABERTO)

    def test_filter_by_invalid_status_returns_400(self):
        response = self.client.get(self.url, {"status": "STATUS_INEXISTENTE"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)
