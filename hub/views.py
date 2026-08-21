from io import BytesIO

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from .report_sources import build_consolidated_report


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
        {
            'name': 'Gestao de Roupeiro',
            'description': 'Controle armarios, usuarios, turnos e tamanhos de uniforme em um painel unico.',
            'details': 'Use para saber quais armarios estao livres, ocupados, em manutencao e quais pessoas possuem armario cadastrado.',
            'url_name': 'roupeiro:index',
            'status': 'Novo app',
            'icon': 'ARM',
        },
    ]
    return render(request, 'hub/home.html', {'tools': tools})


def relatorios(request):
    mes, ano, numero_mes = get_month_filter(request)
    report = build_consolidated_report(ano, numero_mes)
    ti_source = next((source for source in report['sources'] if source['slug'] == 'ti'), None)
    zeladoria_source = next((source for source in report['sources'] if source['slug'] == 'zeladoria'), None)

    context = {
        'mes': mes,
        'total_geral': report['total'],
        'concluidos': report['concluidos'],
        'pendentes': report['pendentes'],
        'cancelados': report['cancelados'],
        'sem_ticket': report['sem_ticket'],
        'taxa_conclusao': report['taxa_conclusao'],
        'fontes_relatorio': report['sources'],
        'areas': report['consolidated_sources'],
        'ti_por_status': ti_source['por_status'] if ti_source else [],
        'ti_por_categoria': ti_source['por_categoria'] if ti_source else [],
        'zeladoria_por_status': zeladoria_source['por_status'] if zeladoria_source else [],
        'itens_recentes': report['items'][:12],
    }

    return render(request, 'hub/relatorios.html', context)


def exportar_relatorio_geral(request):
    mes, ano, numero_mes = get_month_filter(request)
    report = build_consolidated_report(ano, numero_mes)
    itens = report['items']

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
