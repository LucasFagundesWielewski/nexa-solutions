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
