from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from .models import TreinamentoSeguranca


def make_document():
    return SimpleUploadedFile(
        'treinamento.pdf',
        b'%PDF-1.4 treinamento seguranca pintura',
        content_type='application/pdf',
    )


class TreinamentoTests(TestCase):
    def test_cria_treinamento_com_participantes(self):
        response = self.client.post(
            reverse('treinamentos:criar'),
            {
                'titulo': 'Seguranca na pintura',
                'categoria': TreinamentoSeguranca.Categoria.SEGURANCA,
                'status': TreinamentoSeguranca.Status.AGENDADO,
                'data': timezone.localdate().isoformat(),
                'hora_inicio': '08:00',
                'hora_fim': '09:00',
                'empresa': 'Paint Shop',
                'area': 'Pintura',
                'instrutor': 'Hendel',
                'carga_horaria': '2h',
                'documento': make_document(),
                'texto_participantes': 'Maria Silva; 123; A; Cabine; Paint Shop\nJoao Santos',
                'observacoes': 'Treinamento aplicado.',
            },
        )

        treinamento = TreinamentoSeguranca.objects.get()
        self.assertRedirects(response, reverse('treinamentos:detalhe', args=[treinamento.pk]))
        self.assertEqual(treinamento.total_participantes, 2)
        self.assertEqual(treinamento.status, TreinamentoSeguranca.Status.REALIZADO)
        self.assertEqual(treinamento.participantes.count(), 2)

    def test_agenda_treinamento_sem_documento(self):
        response = self.client.post(
            reverse('treinamentos:criar'),
            {
                'titulo': 'Agenda de bloqueio de energias',
                'categoria': TreinamentoSeguranca.Categoria.SEGURANCA,
                'status': TreinamentoSeguranca.Status.AGENDADO,
                'data': timezone.localdate().isoformat(),
                'hora_inicio': '14:30',
                'hora_fim': '15:30',
                'empresa': 'Paint Shop',
                'area': 'Pintura',
                'instrutor': 'Instrutor Segurança',
                'carga_horaria': '1h',
                'texto_participantes': '',
                'observacoes': 'Agendado para proxima turma.',
            },
        )

        treinamento = TreinamentoSeguranca.objects.get(titulo='Agenda de bloqueio de energias')
        calendario = self.client.get(reverse('treinamentos:calendario'), {'mes': timezone.localdate().strftime('%Y-%m')})

        self.assertRedirects(response, reverse('treinamentos:detalhe', args=[treinamento.pk]))
        self.assertEqual(treinamento.status, TreinamentoSeguranca.Status.AGENDADO)
        self.assertFalse(treinamento.documento)
        self.assertContains(calendario, 'Agenda de bloqueio de energias')
        self.assertContains(calendario, '14:30 - 15:30')

    def test_painel_e_exportacao_carregam(self):
        TreinamentoSeguranca.objects.create(
            titulo='Uso de EPI',
            categoria=TreinamentoSeguranca.Categoria.SEGURANCA,
            status=TreinamentoSeguranca.Status.REALIZADO,
            data=timezone.localdate(),
            hora_inicio='08:00',
            empresa='Paint Shop',
            area='Pintura',
            documento=make_document(),
        )

        painel = self.client.get(reverse('treinamentos:painel'), {'busca': 'EPI'})
        exportacao = self.client.get(reverse('treinamentos:exportar_excel'))

        self.assertContains(painel, 'Uso de EPI')
        self.assertEqual(exportacao.status_code, 200)
