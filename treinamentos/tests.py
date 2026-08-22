from unittest.mock import patch

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

    def test_calendario_abre_cadastro_com_data_preenchida(self):
        data = timezone.localdate().replace(day=15)

        calendario = self.client.get(reverse('treinamentos:calendario'), {'mes': data.strftime('%Y-%m')})
        cadastro = self.client.get(reverse('treinamentos:criar'), {'data': data.isoformat()})

        self.assertContains(calendario, f'?data={data.isoformat()}')
        self.assertContains(cadastro, f'value="{data.isoformat()}"')

    def test_calendario_destaca_terca_quinta_com_horarios_preferenciais(self):
        data = timezone.datetime(2026, 9, 1).date()

        calendario = self.client.get(reverse('treinamentos:calendario'), {'mes': data.strftime('%Y-%m')})
        cadastro = self.client.get(
            reverse('treinamentos:criar'),
            {'data': data.isoformat(), 'hora': '09:30'},
        )

        self.assertContains(calendario, f'?data={data.isoformat()}&hora=09:30')
        self.assertContains(calendario, '13:30')
        self.assertContains(calendario, 'Preferencial')
        self.assertContains(cadastro, 'value="09:30"')

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

    def test_pdf_digital_preenche_participantes_e_exporta_excel_individual(self):
        with patch(
            'treinamentos.services.extract_text_from_document',
            return_value='Ana Pereira; 456; B; Preparacao; Paint Shop\nCarlos Lima; 789; C; Cabine; Paint Shop',
        ):
            response = self.client.post(
                reverse('treinamentos:criar'),
                {
                    'titulo': 'PDF digital de seguranca',
                    'categoria': TreinamentoSeguranca.Categoria.SEGURANCA,
                    'status': TreinamentoSeguranca.Status.AGENDADO,
                    'data': timezone.localdate().isoformat(),
                    'hora_inicio': '10:00',
                    'empresa': 'Paint Shop',
                    'area': 'Pintura',
                    'instrutor': 'Hendel',
                    'documento': make_document(),
                    'texto_participantes': '',
                },
            )

        treinamento = TreinamentoSeguranca.objects.get(titulo='PDF digital de seguranca')
        exportacao = self.client.get(reverse('treinamentos:exportar_treinamento_excel', args=[treinamento.pk]))

        self.assertRedirects(response, reverse('treinamentos:detalhe', args=[treinamento.pk]))
        self.assertIn('Ana Pereira', treinamento.texto_participantes)
        self.assertEqual(treinamento.total_participantes, 2)
        self.assertEqual(exportacao.status_code, 200)
