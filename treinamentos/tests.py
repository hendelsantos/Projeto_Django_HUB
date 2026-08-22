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
                'data': timezone.localdate().isoformat(),
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
        self.assertEqual(treinamento.participantes.count(), 2)

    def test_painel_e_exportacao_carregam(self):
        TreinamentoSeguranca.objects.create(
            titulo='Uso de EPI',
            categoria=TreinamentoSeguranca.Categoria.SEGURANCA,
            data=timezone.localdate(),
            empresa='Paint Shop',
            area='Pintura',
            documento=make_document(),
        )

        painel = self.client.get(reverse('treinamentos:painel'), {'busca': 'EPI'})
        exportacao = self.client.get(reverse('treinamentos:exportar_excel'))

        self.assertContains(painel, 'Uso de EPI')
        self.assertEqual(exportacao.status_code, 200)
