from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Tarefa


class TarefaTests(TestCase):
    def test_cria_tarefa_e_exibe_no_painel(self):
        response = self.client.post(
            reverse('tarefas:criar'),
            {
                'titulo': 'Cobrar retorno do fornecedor',
                'descricao': 'Acompanhar resposta pendente',
                'responsavel': 'Hendel',
                'area': 'Pintura',
                'origem': 'Reuniao diaria',
                'prioridade': Tarefa.Prioridade.ALTA,
                'prazo': timezone.localdate().isoformat(),
            },
        )

        tarefa = Tarefa.objects.get()
        self.assertRedirects(response, reverse('tarefas:detalhe', args=[tarefa.pk]))
        painel = self.client.get(reverse('tarefas:painel'))
        self.assertContains(painel, 'Cobrar retorno do fornecedor')

    def test_concluir_tarefa_remove_das_pendencias(self):
        tarefa = Tarefa.objects.create(titulo='Validar relatorio', prioridade=Tarefa.Prioridade.MEDIA)

        response = self.client.post(reverse('tarefas:concluir', args=[tarefa.pk]))
        tarefa.refresh_from_db()

        self.assertRedirects(response, reverse('tarefas:painel'))
        self.assertEqual(tarefa.status, Tarefa.Status.CONCLUIDA)
        self.assertIsNotNone(tarefa.concluido_em)
