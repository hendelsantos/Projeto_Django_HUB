from django.db.models import Count

from chamados_ti.models import ChamadoTI
from zeladoria.models import ChamadoZeladoria


STATUS_FINALIZADOS = ('concluido', 'cancelado')


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


REPORT_SOURCE_BUILDERS = [
    get_ti_source,
    get_zeladoria_source,
    get_extrator_scanner_source,
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
