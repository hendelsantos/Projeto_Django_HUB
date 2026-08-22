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
    }
