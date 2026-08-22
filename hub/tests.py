from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from chamados_ti.models import ChamadoTI
from roupeiro.models import Armario
from zeladoria.models import ChamadoZeladoria

from .models import AccessLog


class HubHomeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='operador',
            password='senha-teste-123',
        )

    def test_home_page_loads_for_anonymous_user(self):
        response = self.client.get(reverse('hub:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Scanner para Excel')

    def test_access_log_records_page_view(self):
        self.client.get(reverse('hub:home'))

        self.assertTrue(AccessLog.objects.filter(path='/').exists())

    def test_global_search_finds_locker(self):
        Armario.objects.create(numero=12, usuario='Maria Oliveira')

        response = self.client.get(reverse('hub:buscar'), {'q': 'Maria'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Armario #12')
        self.assertContains(response, 'Roupeiro')

    def test_global_search_finds_ti_ticket(self):
        chamado = ChamadoTI.objects.create(
            titulo='Notebook sem rede',
            solicitante='Carlos Lima',
            descricao='Equipamento nao conecta',
            ticket_oficial='TI-123',
        )

        response = self.client.get(reverse('hub:buscar'), {'q': 'TI-123'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, chamado.titulo)
        self.assertContains(response, 'TI')

    def test_global_search_finds_building_care(self):
        chamado = ChamadoZeladoria.objects.create(
            titulo='Porta com problema',
            solicitante='Ana Souza',
            local='Predio 2',
            descricao='Porta nao fecha corretamente',
        )

        response = self.client.get(reverse('hub:buscar'), {'q': 'Predio 2'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, chamado.titulo)
        self.assertContains(response, 'Zeladoria')

# Create your tests here.
