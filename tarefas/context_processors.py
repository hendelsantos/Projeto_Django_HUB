from django.urls import reverse

from .models import Tarefa


def followup_toasts(request):
    tarefas = (
        Tarefa.objects.exclude(status__in=[Tarefa.Status.CONCLUIDA, Tarefa.Status.CANCELADA])
        .order_by('prazo', '-prioridade', '-criado_em')[:5]
    )

    return {
        'followup_toasts': tarefas,
        'followup_toasts_total': Tarefa.objects.exclude(
            status__in=[Tarefa.Status.CONCLUIDA, Tarefa.Status.CANCELADA]
        ).count(),
        'followup_toast_payload': [
            {
                'id': tarefa.pk,
                'titulo': tarefa.titulo,
                'prioridade': tarefa.get_prioridade_display(),
                'responsavel': tarefa.responsavel or 'Sem responsavel',
                'prazo': tarefa.prazo.strftime('%d/%m/%Y') if tarefa.prazo else '',
                'status': tarefa.get_status_display(),
                'vencida': tarefa.esta_vencida,
                'venceHoje': tarefa.vence_hoje,
                'url': reverse('tarefas:detalhe', args=[tarefa.pk]),
            }
            for tarefa in tarefas
        ],
    }
