from django.test import TestCase
from django.urls import reverse

from .models import Armario


class ArmarioModelTests(TestCase):
    def test_armario_com_usuario_fica_ocupado(self):
        armario = Armario.objects.create(numero=1, usuario='Maria Silva')

        self.assertEqual(armario.status, Armario.Status.OCUPADO)


class RoupeiroViewsTests(TestCase):
    def test_index_carrega_resumo(self):
        response = self.client.get(reverse('roupeiro:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Armarios e uniformes')

    def test_criar_armario(self):
        response = self.client.post(
            reverse('roupeiro:criar'),
            {
                'numero': 10,
                'usuario': 'Joao Santos',
                'turno': Armario.Turno.PRIMEIRO,
                'tamanho_camisa': Armario.TamanhoRoupa.M,
                'tamanho_camisa_numero': 40,
                'tamanho_calca': Armario.TamanhoRoupa.G,
                'tamanho_calca_numero': 42,
                'tamanho_macacao': Armario.TamanhoRoupa.G,
                'tamanho_macacao_numero': 44,
                'status': Armario.Status.LIVRE,
                'observacoes': '',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Armario.objects.filter(numero=10, usuario='Joao Santos', tamanho_calca_numero=42).exists())

    def test_exportar_excel(self):
        Armario.objects.create(numero=2, usuario='Ana Souza')

        response = self.client.get(reverse('roupeiro:exportar_excel'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

    def test_liberar_armario(self):
        armario = Armario.objects.create(
            numero=3,
            usuario='Carlos Lima',
            turno=Armario.Turno.SEGUNDO,
            tamanho_camisa=Armario.TamanhoRoupa.G,
            tamanho_camisa_numero=42,
        )

        response = self.client.post(reverse('roupeiro:liberar', args=[armario.pk]))
        armario.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(armario.status, Armario.Status.LIVRE)
        self.assertEqual(armario.usuario, '')
        self.assertIsNone(armario.tamanho_camisa_numero)

# Create your tests here.
