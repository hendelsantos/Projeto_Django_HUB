from io import BytesIO

from django.test import TestCase
from django.urls import reverse
from openpyxl import load_workbook

from .models import ChamadoZeladoria


class ZeladoriaTests(TestCase):
    def test_index_page_loads(self):
        response = self.client.get(reverse('zeladoria:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Zeladoria Predial')

    def test_create_chamado_without_login(self):
        response = self.client.post(
            reverse('zeladoria:criar'),
            {
                'titulo': 'Iluminacao fraca',
                'solicitante': 'Hendel Santos',
                'local': 'Predio 1',
                'descricao': 'Melhorar iluminacao do corredor.',
            },
        )

        chamado = ChamadoZeladoria.objects.get()
        self.assertRedirects(response, reverse('zeladoria:detalhe', args=[chamado.pk]))
        self.assertEqual(chamado.status, ChamadoZeladoria.Status.NOVO)

    def test_follow_up_updates_ticket_and_status(self):
        chamado = ChamadoZeladoria.objects.create(
            titulo='Ajuste na cabine',
            solicitante='Equipe Pintura',
            local='Cabine',
            descricao='Ajuste na area de limpeza.',
        )

        response = self.client.post(
            reverse('zeladoria:editar', args=[chamado.pk]),
            {
                'status': ChamadoZeladoria.Status.TICKET_ABERTO,
                'ticket_oficial': 'REQ-123',
                'observacoes': 'Requisicao aberta no sistema oficial.',
            },
        )

        chamado.refresh_from_db()
        self.assertRedirects(response, reverse('zeladoria:painel'))
        self.assertEqual(chamado.ticket_oficial, 'REQ-123')
        self.assertEqual(chamado.status, ChamadoZeladoria.Status.TICKET_ABERTO)

    def test_export_excel_contains_chamado(self):
        ChamadoZeladoria.objects.create(
            titulo='Parede danificada',
            solicitante='Hendel Santos',
            local='Predio 2',
            descricao='Pintura de parede danificada.',
            ticket_oficial='REQ-999',
        )

        response = self.client.get(reverse('zeladoria:exportar_excel'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

        workbook = load_workbook(BytesIO(response.content))
        sheet = workbook.active
        self.assertEqual(sheet['A1'].value, 'Relatorio de Zeladoria Predial')
        self.assertEqual(sheet['B3'].value, 'Parede danificada')
        self.assertEqual(sheet['E3'].value, 'Hendel Santos')
        self.assertEqual(sheet['I3'].value, 'REQ-999')

# Create your tests here.
