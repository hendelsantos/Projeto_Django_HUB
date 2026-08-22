from django.db.models import Count
from django.utils import timezone

from chamados_ti.models import ChamadoTI
from headcount.models import HeadcountImport
from roupeiro.models import Armario
from tarefas.models import Tarefa
from treinamentos.models import TreinamentoSeguranca
from zeladoria.models import ChamadoZeladoria


STATUS_FINALIZADOS = ('concluido', 'cancelado')
STATUS_FINAIS_TAREFAS = (Tarefa.Status.CONCLUIDA, Tarefa.Status.CANCELADA)


def count_by_field(queryset, field_name, choices=None):
    labels = dict(choices or [])
    rows = queryset.values(field_name).annotate(total=Count('id')).order_by('-total', field_name)

    return [
        {
            'label': labels.get(row[field_name], row[field_name] or 'Nao informado'),
            'total': row['total'],
        }
        for row in rows
    ]


def get_ti_source(ano, numero_mes):
    chamados = ChamadoTI.objects.filter(criado_em__year=ano, criado_em__month=numero_mes)
    return {
        'nome': 'Chamados de TI',
        'slug': 'ti',
        'tipo': 'Metricas e exportacao',
        'tem_dados_consolidados': True,
        'pendentes_rotulo': 'pendentes',
        'total': chamados.count(),
        'concluidos': chamados.filter(status=ChamadoTI.Status.CONCLUIDO).count(),
        'cancelados': chamados.filter(status=ChamadoTI.Status.CANCELADO).count(),
        'pendentes': chamados.exclude(status__in=STATUS_FINALIZADOS).count(),
        'sem_ticket': chamados.filter(ticket_oficial='').exclude(status__in=STATUS_FINALIZADOS).count(),
        'por_status': count_by_field(chamados, 'status', ChamadoTI.Status.choices),
        'por_categoria': count_by_field(chamados, 'categoria', ChamadoTI.Categoria.choices),
        'items': [
            {
                'area': 'TI',
                'titulo': chamado.titulo,
                'solicitante': chamado.solicitante,
                'referencia': chamado.setor or chamado.get_categoria_display(),
                'status': chamado.get_status_display(),
                'ticket': chamado.ticket_oficial,
                'data': chamado.criado_em,
                'detalhe': chamado.descricao,
                'follow_up': chamado.solucao,
            }
            for chamado in chamados
        ],
    }


def get_zeladoria_source(ano, numero_mes):
    chamados = ChamadoZeladoria.objects.filter(criado_em__year=ano, criado_em__month=numero_mes)
    return {
        'nome': 'Zeladoria Predial',
        'slug': 'zeladoria',
        'tipo': 'Relatorio e exportacao',
        'tem_dados_consolidados': True,
        'pendentes_rotulo': 'pendentes',
        'total': chamados.count(),
        'concluidos': chamados.filter(status=ChamadoZeladoria.Status.CONCLUIDO).count(),
        'cancelados': chamados.filter(status=ChamadoZeladoria.Status.CANCELADO).count(),
        'pendentes': chamados.exclude(status__in=STATUS_FINALIZADOS).count(),
        'sem_ticket': chamados.filter(ticket_oficial='').exclude(status__in=STATUS_FINALIZADOS).count(),
        'por_status': count_by_field(chamados, 'status', ChamadoZeladoria.Status.choices),
        'por_categoria': [],
        'items': [
            {
                'area': 'Zeladoria',
                'titulo': chamado.titulo,
                'solicitante': chamado.solicitante,
                'referencia': chamado.local,
                'status': chamado.get_status_display(),
                'ticket': chamado.ticket_oficial,
                'data': chamado.criado_em,
                'detalhe': chamado.descricao,
                'follow_up': chamado.observacoes,
            }
            for chamado in chamados
        ],
    }


def get_extrator_scanner_source(_ano, _numero_mes):
    return {
        'nome': 'Scanner para Excel',
        'slug': 'extrator-scanner',
        'tipo': 'Geracao de planilha',
        'tem_dados_consolidados': False,
        'pendentes_rotulo': 'pendentes',
        'total': 0,
        'concluidos': 0,
        'cancelados': 0,
        'pendentes': 0,
        'sem_ticket': 0,
        'por_status': [],
        'por_categoria': [],
        'items': [],
        'observacao': 'Gera Excel sob demanda, mas ainda nao salva historico para consolidacao mensal.',
    }


def get_roupeiro_source(_ano, _numero_mes):
    armarios = Armario.objects.all()
    ocupados = armarios.filter(status=Armario.Status.OCUPADO).count()
    total = armarios.count()

    def format_size(label, numeric):
        if label and numeric:
            return f'{label} / {numeric}'
        return label or numeric or '-'

    return {
        'nome': 'Gestao de Roupeiro',
        'slug': 'roupeiro',
        'tipo': 'Metricas e exportacao',
        'tem_dados_consolidados': True,
        'pendentes_rotulo': 'livres',
        'total': total,
        'concluidos': ocupados,
        'cancelados': armarios.filter(status=Armario.Status.INATIVO).count(),
        'pendentes': armarios.filter(status=Armario.Status.LIVRE).count(),
        'sem_ticket': armarios.filter(status=Armario.Status.MANUTENCAO).count(),
        'por_status': count_by_field(armarios, 'status', Armario.Status.choices),
        'por_categoria': count_by_field(armarios.exclude(turno=''), 'turno', Armario.Turno.choices),
        'items': [
            {
                'area': 'Roupeiro',
                'titulo': f'Armario #{armario.numero}',
                'solicitante': armario.usuario or 'Sem usuario',
                'referencia': armario.get_turno_display() if armario.turno else 'Sem turno',
                'status': armario.get_status_display(),
                'ticket': '',
                'data': armario.atualizado_em,
                'detalhe': (
                    f"Camisa: {format_size(armario.get_tamanho_camisa_display() if armario.tamanho_camisa else '', armario.tamanho_camisa_numero)}; "
                    f"Calca: {format_size(armario.get_tamanho_calca_display() if armario.tamanho_calca else '', armario.tamanho_calca_numero)}; "
                    f"Macacao: {format_size(armario.get_tamanho_macacao_display() if armario.tamanho_macacao else '', armario.tamanho_macacao_numero)}"
                ),
                'follow_up': armario.observacoes,
            }
            for armario in armarios
        ],
    }


def get_headcount_source(ano, numero_mes):
    importacao = (
        HeadcountImport.objects.filter(mes__year=ano, mes__month=numero_mes)
        .order_by('-criado_em')
        .first()
    )

    if not importacao:
        return {
            'nome': 'Headcount e Aniversariantes',
            'slug': 'headcount',
            'tipo': 'Metricas e exportacao',
            'tem_dados_consolidados': True,
            'pendentes_rotulo': 'sem base',
            'total': 0,
            'concluidos': 0,
            'cancelados': 0,
            'pendentes': 0,
            'sem_ticket': 0,
            'por_status': [],
            'por_categoria': [],
            'items': [],
        }

    lista = importacao.listas_aniversariantes.first()
    aniversariantes = lista.nomes.select_related('membro') if lista else []

    return {
        'nome': 'Headcount e Aniversariantes',
        'slug': 'headcount',
        'tipo': 'Metricas e exportacao',
        'tem_dados_consolidados': True,
        'pendentes_rotulo': 'na pintura',
        'total': importacao.total_membros,
        'concluidos': importacao.total_membros,
        'cancelados': 0,
        'pendentes': 0,
        'sem_ticket': 0,
        'por_status': [],
        'por_categoria': count_by_field(importacao.membros.exclude(turno=''), 'turno'),
        'items': [
            {
                'area': 'Headcount',
                'titulo': f'Aniversariante - {aniversariante.nome}',
                'solicitante': aniversariante.nome,
                'referencia': aniversariante.membro.area if aniversariante.membro else 'Nao encontrado no headcount',
                'status': 'Encontrado' if aniversariante.membro else 'Pendente',
                'ticket': '',
                'data': importacao.criado_em,
                'detalhe': f'Turno: {aniversariante.membro.turno}' if aniversariante.membro else 'Nome nao localizado na base mensal.',
                'follow_up': f'Base {importacao.mes.strftime("%m/%Y")}',
            }
            for aniversariante in aniversariantes
        ],
    }


def get_tarefas_source(ano, numero_mes):
    tarefas = Tarefa.objects.filter(criado_em__year=ano, criado_em__month=numero_mes)

    return {
        'nome': 'Tarefas e Follow-up',
        'slug': 'tarefas',
        'tipo': 'Metricas e exportacao',
        'tem_dados_consolidados': True,
        'pendentes_rotulo': 'abertas',
        'total': tarefas.count(),
        'concluidos': tarefas.filter(status=Tarefa.Status.CONCLUIDA).count(),
        'cancelados': tarefas.filter(status=Tarefa.Status.CANCELADA).count(),
        'pendentes': tarefas.exclude(status__in=STATUS_FINAIS_TAREFAS).count(),
        'sem_ticket': tarefas.exclude(status__in=STATUS_FINAIS_TAREFAS).filter(prazo__isnull=True).count(),
        'por_status': count_by_field(tarefas, 'status', Tarefa.Status.choices),
        'por_categoria': count_by_field(tarefas.exclude(area=''), 'area'),
        'items': [
            {
                'area': 'Follow-up',
                'titulo': tarefa.titulo,
                'solicitante': tarefa.responsavel or 'Sem responsavel',
                'referencia': tarefa.area or tarefa.origem or 'Sem referencia',
                'status': tarefa.get_status_display(),
                'ticket': '',
                'data': tarefa.criado_em,
                'detalhe': tarefa.descricao,
                'follow_up': tarefa.follow_up or (f'Prazo: {tarefa.prazo.strftime("%d/%m/%Y")}' if tarefa.prazo else 'Sem prazo definido'),
            }
            for tarefa in tarefas
        ],
    }


def get_treinamentos_source(ano, numero_mes):
    treinamentos = TreinamentoSeguranca.objects.filter(data__year=ano, data__month=numero_mes)
    total_participantes = sum(treinamento.total_participantes for treinamento in treinamentos)

    return {
        'nome': 'Treinamentos de Seguranca',
        'slug': 'treinamentos',
        'tipo': 'Metricas e exportacao',
        'tem_dados_consolidados': True,
        'pendentes_rotulo': 'vencidos',
        'total': treinamentos.count(),
        'concluidos': total_participantes,
        'cancelados': 0,
        'pendentes': treinamentos.filter(validade__lt=timezone.localdate()).count(),
        'sem_ticket': treinamentos.filter(total_participantes=0).count(),
        'por_status': count_by_field(treinamentos, 'categoria', TreinamentoSeguranca.Categoria.choices),
        'por_categoria': count_by_field(treinamentos.exclude(empresa=''), 'empresa'),
        'items': [
            {
                'area': 'Treinamentos',
                'titulo': treinamento.titulo,
                'solicitante': treinamento.instrutor or treinamento.empresa,
                'referencia': treinamento.empresa,
                'status': f'{treinamento.get_status_display()} - {treinamento.total_participantes} participantes',
                'ticket': '',
                'data': treinamento.criado_em,
                'detalhe': f'Data: {treinamento.data.strftime("%d/%m/%Y")} | Horario: {treinamento.horario} | Area: {treinamento.area}',
                'follow_up': treinamento.observacoes or 'Documento escaneado armazenado.',
            }
            for treinamento in treinamentos
        ],
    }


REPORT_SOURCE_BUILDERS = [
    get_ti_source,
    get_zeladoria_source,
    get_extrator_scanner_source,
    get_roupeiro_source,
    get_headcount_source,
    get_tarefas_source,
    get_treinamentos_source,
]


def get_report_sources(ano, numero_mes):
    return [builder(ano, numero_mes) for builder in REPORT_SOURCE_BUILDERS]


def build_consolidated_report(ano, numero_mes):
    sources = get_report_sources(ano, numero_mes)
    consolidated_sources = [source for source in sources if source['tem_dados_consolidados']]
    items = [
        item
        for source in consolidated_sources
        for item in source['items']
    ]

    total = sum(source['total'] for source in consolidated_sources)
    concluidos = sum(source['concluidos'] for source in consolidated_sources)
    cancelados = sum(source['cancelados'] for source in consolidated_sources)
    pendentes = sum(source['pendentes'] for source in consolidated_sources)
    sem_ticket = sum(source['sem_ticket'] for source in consolidated_sources)

    return {
        'sources': sources,
        'consolidated_sources': consolidated_sources,
        'items': sorted(items, key=lambda item: item['data'], reverse=True),
        'total': total,
        'concluidos': concluidos,
        'cancelados': cancelados,
        'pendentes': pendentes,
        'sem_ticket': sem_ticket,
        'taxa_conclusao': round((concluidos / total) * 100) if total else 0,
    }
