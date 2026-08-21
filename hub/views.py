from io import BytesIO

from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from chamados_ti.models import ChamadoTI
from zeladoria.models import ChamadoZeladoria


STATUS_FINALIZADOS = ('concluido', 'cancelado')


def get_month_filter(request):
    mes = request.GET.get('mes', timezone.localdate().strftime('%Y-%m'))

    try:
        ano, numero_mes = mes.split('-')
        return mes, int(ano), int(numero_mes)
    except (TypeError, ValueError):
        messages.error(request, 'Filtro de mes invalido.')
        mes = timezone.localdate().strftime('%Y-%m')
        ano, numero_mes = mes.split('-')
        return mes, int(ano), int(numero_mes)


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


def build_report_items(ti_chamados, zeladoria_chamados):
    items = []

    for chamado in ti_chamados:
        items.append(
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
        )

    for chamado in zeladoria_chamados:
        items.append(
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
        )

    return sorted(items, key=lambda item: item['data'], reverse=True)


def home(request):
    tools = [
        {
            'name': 'Scanner para Excel',
            'description': 'Suba um PDF escaneado da pintura e gere uma planilha Excel com os dados extraidos.',
            'details': 'Use quando receber arquivos de scanner e precisar transformar o conteudo em uma planilha para conferencia ou tratamento.',
            'url_name': 'extrator_scanner:index',
            'status': 'Primeiro app',
            'icon': 'PDF',
        },
        {
            'name': 'Zeladoria Predial',
            'description': 'Cadastre melhorias do predio, acompanhe tickets oficiais e exporte chamados por mes.',
            'details': 'Ideal para registrar pedidos da equipe sobre estrutura predial, inserir foto, fazer follow-up e controlar o que ainda esta aberto.',
            'url_name': 'zeladoria:index',
            'status': 'Novo app',
            'icon': 'ZEL',
        },
        {
            'name': 'Chamados de TI',
            'description': 'Controle atendimentos de TI, contas, sistemas e equipamentos com metricas mensais.',
            'details': 'Organiza demandas como abertura de conta, acesso a sistemas, verificacao de equipamentos e relatorio de atendimentos do mes.',
            'url_name': 'chamados_ti:index',
            'status': 'Gestao',
            'icon': 'TI',
        },
    ]
    return render(request, 'hub/home.html', {'tools': tools})


def relatorios(request):
    mes, ano, numero_mes = get_month_filter(request)
    ti_mes = ChamadoTI.objects.filter(criado_em__year=ano, criado_em__month=numero_mes)
    zeladoria_mes = ChamadoZeladoria.objects.filter(criado_em__year=ano, criado_em__month=numero_mes)

    ti_total = ti_mes.count()
    zeladoria_total = zeladoria_mes.count()
    total_geral = ti_total + zeladoria_total
    concluidos = (
        ti_mes.filter(status=ChamadoTI.Status.CONCLUIDO).count()
        + zeladoria_mes.filter(status=ChamadoZeladoria.Status.CONCLUIDO).count()
    )
    cancelados = (
        ti_mes.filter(status=ChamadoTI.Status.CANCELADO).count()
        + zeladoria_mes.filter(status=ChamadoZeladoria.Status.CANCELADO).count()
    )
    pendentes = total_geral - concluidos - cancelados
    sem_ticket = (
        ti_mes.filter(ticket_oficial='').exclude(status__in=STATUS_FINALIZADOS).count()
        + zeladoria_mes.filter(ticket_oficial='').exclude(status__in=STATUS_FINALIZADOS).count()
    )
    taxa_conclusao = round((concluidos / total_geral) * 100) if total_geral else 0
    itens_recentes = build_report_items(ti_mes, zeladoria_mes)[:12]

    context = {
        'mes': mes,
        'total_geral': total_geral,
        'concluidos': concluidos,
        'pendentes': pendentes,
        'cancelados': cancelados,
        'sem_ticket': sem_ticket,
        'taxa_conclusao': taxa_conclusao,
        'areas': [
            {'nome': 'Chamados de TI', 'total': ti_total, 'pendentes': ti_mes.exclude(status__in=STATUS_FINALIZADOS).count()},
            {
                'nome': 'Zeladoria Predial',
                'total': zeladoria_total,
                'pendentes': zeladoria_mes.exclude(status__in=STATUS_FINALIZADOS).count(),
            },
        ],
        'ti_por_status': count_by_field(ti_mes, 'status', ChamadoTI.Status.choices),
        'ti_por_categoria': count_by_field(ti_mes, 'categoria', ChamadoTI.Categoria.choices),
        'zeladoria_por_status': count_by_field(zeladoria_mes, 'status', ChamadoZeladoria.Status.choices),
        'itens_recentes': itens_recentes,
    }

    return render(request, 'hub/relatorios.html', context)


def exportar_relatorio_geral(request):
    mes, ano, numero_mes = get_month_filter(request)
    ti_mes = ChamadoTI.objects.filter(criado_em__year=ano, criado_em__month=numero_mes)
    zeladoria_mes = ChamadoZeladoria.objects.filter(criado_em__year=ano, criado_em__month=numero_mes)
    itens = build_report_items(ti_mes, zeladoria_mes)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Relatorio Geral'

    sheet.merge_cells('A1:J1')
    sheet['A1'] = f'Relatorio Geral Paint Hub - {mes}'
    sheet['A1'].font = Font(bold=True, size=16, color='FFFFFF')
    sheet['A1'].fill = PatternFill('solid', fgColor='17212B')
    sheet['A1'].alignment = Alignment(horizontal='center')

    headers = [
        'Area',
        'Data',
        'Titulo',
        'Solicitante',
        'Referencia',
        'Status',
        'Ticket oficial',
        'Descricao',
        'Follow-up',
        'Mes',
    ]
    sheet.append(headers)

    header_fill = PatternFill('solid', fgColor='E8F3EF')
    for cell in sheet[2]:
        cell.font = Font(bold=True, color='17212B')
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')

    for item in itens:
        sheet.append(
            [
                item['area'],
                timezone.localtime(item['data']).strftime('%d/%m/%Y %H:%M'),
                item['titulo'],
                item['solicitante'],
                item['referencia'],
                item['status'],
                item['ticket'],
                item['detalhe'],
                item['follow_up'],
                mes,
            ]
        )

    for row in sheet.iter_rows(min_row=3):
        for cell in row:
            cell.alignment = Alignment(vertical='top', wrap_text=True)

    widths = [16, 18, 32, 24, 28, 20, 18, 46, 42, 12]
    for index, width in enumerate(widths, start=1):
        sheet.column_dimensions[get_column_letter(index)].width = width

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    filename = f"relatorio_geral_paint_hub_{mes.replace('-', '_')}.xlsx"
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
