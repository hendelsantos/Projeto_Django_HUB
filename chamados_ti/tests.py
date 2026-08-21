from io import BytesIO

from django.test import TestCase
from django.urls import reverse
from openpyxl import load_workbook

from .models import ChamadoTI


class ChamadosTITests(TestCase):
    def test_index_page_loads(self):
        response = self.client.get(reverse('chamados_ti:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chamados de TI e Equipamentos')

    def test_create_chamado_ti(self):
        response = self.client.post(
            reverse('chamados_ti:criar'),
            {
                'titulo': 'Criar conta de sistema',
                'solicitante': 'Hendel Santos',
                'setor': 'Pintura',
                'categoria': ChamadoTI.Categoria.CONTA,
                'prioridade': ChamadoTI.Prioridade.MEDIA,
                'descricao': 'Novo membro precisa de acesso.',
            },
        )

        chamado = ChamadoTI.objects.get()
        self.assertRedirects(response, reverse('chamados_ti:detalhe', args=[chamado.pk]))
        self.assertEqual(chamado.status, ChamadoTI.Status.NOVO)

    def test_follow_up_concludes_chamado(self):
        chamado = ChamadoTI.objects.create(
            titulo='Verificar equipamento',
            solicitante='Equipe Pintura',
            categoria=ChamadoTI.Categoria.EQUIPAMENTO,
            descricao='Computador nao liga.',
        )

        response = self.client.post(
            reverse('chamados_ti:editar', args=[chamado.pk]),
            {
                'status': ChamadoTI.Status.CONCLUIDO,
                'ticket_oficial': 'TI-123',
                'solucao': 'Equipamento testado e substituido.',
            },
        )

        chamado.refresh_from_db()
        self.assertRedirects(response, reverse('chamados_ti:painel'))
        self.assertEqual(chamado.ticket_oficial, 'TI-123')
        self.assertIsNotNone(chamado.concluido_em)

    def test_metrics_page_counts_chamados(self):
        ChamadoTI.objects.create(
            titulo='Acesso ao e-mail',
            solicitante='Hendel Santos',
            categoria=ChamadoTI.Categoria.EMAIL,
            descricao='Liberar acesso.',
            status=ChamadoTI.Status.CONCLUIDO,
        )

        response = self.client.get(reverse('chamados_ti:metricas'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Atendidos')

    def test_export_excel_contains_chamado(self):
        ChamadoTI.objects.create(
            titulo='Criar conta',
            solicitante='Hendel Santos',
            setor='Pintura',
            categoria=ChamadoTI.Categoria.CONTA,
            descricao='Criar conta para novo membro.',
            ticket_oficial='TI-999',
        )

        response = self.client.get(reverse('chamados_ti:exportar_excel'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

        workbook = load_workbook(BytesIO(response.content))
        sheet = workbook.active
        self.assertEqual(sheet['A1'].value, 'Relatorio de Chamados de TI')
        self.assertEqual(sheet['C3'].value, 'Criar conta')
        self.assertEqual(sheet['J3'].value, 'TI-999')

# Create your tests here.
