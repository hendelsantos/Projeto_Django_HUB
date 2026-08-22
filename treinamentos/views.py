from io import BytesIO

from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from .forms import TreinamentoForm
from .models import TreinamentoSeguranca
from .services import sync_participants


def index(request):
    hoje = timezone.localdate()
    treinamentos_mes = TreinamentoSeguranca.objects.filter(data__year=hoje.year, data__month=hoje.month)
    total_participantes_mes = sum(item.total_participantes for item in treinamentos_mes)
    vencidos = TreinamentoSeguranca.objects.filter(validade__lt=hoje).count()

    return render(
        request,
        'treinamentos/index.html',
        {
            'treinamentos_mes': treinamentos_mes.count(),
            'participantes_mes': total_participantes_mes,
            'vencidos': vencidos,
            'por_empresa': treinamentos_mes.values('empresa').annotate(total=Count('id')).order_by('-total')[:6],
        },
    )


def criar(request):
    if request.method == 'POST':
        form = TreinamentoForm(request.POST, request.FILES)
        if form.is_valid():
            treinamento = form.save()
            sync_participants(treinamento)
            messages.success(request, 'Treinamento cadastrado com sucesso.')
            return redirect('treinamentos:detalhe', pk=treinamento.pk)
    else:
        form = TreinamentoForm(initial={'data': timezone.localdate(), 'area': 'Pintura'})

    return render(
        request,
        'treinamentos/form.html',
        {'form': form, 'titulo': 'Novo treinamento', 'acao': 'Cadastrar treinamento'},
    )


def painel(request):
    busca = request.GET.get('busca', '').strip()
    empresa = request.GET.get('empresa', '').strip()
    categoria = request.GET.get('categoria', '')
    mes = request.GET.get('mes', '')

    treinamentos = TreinamentoSeguranca.objects.all()

    if busca:
        treinamentos = treinamentos.filter(
            Q(titulo__icontains=busca)
            | Q(instrutor__icontains=busca)
            | Q(area__icontains=busca)
            | Q(observacoes__icontains=busca)
            | Q(participantes__nome__icontains=busca)
        ).distinct()

    if empresa:
        treinamentos = treinamentos.filter(empresa__icontains=empresa)

    if categoria:
        treinamentos = treinamentos.filter(categoria=categoria)

    if mes:
        try:
            ano, numero_mes = mes.split('-')
            treinamentos = treinamentos.filter(data__year=ano, data__month=numero_mes)
        except ValueError:
            messages.error(request, 'Filtro de mes invalido.')

    return render(
        request,
        'treinamentos/painel.html',
        {
            'treinamentos': treinamentos,
            'busca': busca,
            'empresa': empresa,
            'categoria_atual': categoria,
            'mes': mes,
            'categoria_choices': TreinamentoSeguranca.Categoria.choices,
        },
    )


def detalhe(request, pk):
    treinamento = get_object_or_404(TreinamentoSeguranca, pk=pk)
    por_empresa = treinamento.participantes.values('empresa').annotate(total=Count('id')).order_by('-total')
    por_area = treinamento.participantes.values('area').annotate(total=Count('id')).order_by('-total')
    por_turno = treinamento.participantes.values('turno').annotate(total=Count('id')).order_by('-total')

    return render(
        request,
        'treinamentos/detalhe.html',
        {
            'treinamento': treinamento,
            'por_empresa': por_empresa,
            'por_area': por_area,
            'por_turno': por_turno,
        },
    )


def editar(request, pk):
    treinamento = get_object_or_404(TreinamentoSeguranca, pk=pk)

    if request.method == 'POST':
        form = TreinamentoForm(request.POST, request.FILES, instance=treinamento)
        if form.is_valid():
            treinamento = form.save()
            sync_participants(treinamento)
            messages.success(request, 'Treinamento atualizado com sucesso.')
            return redirect('treinamentos:detalhe', pk=treinamento.pk)
    else:
        form = TreinamentoForm(instance=treinamento)

    return render(
        request,
        'treinamentos/form.html',
        {'form': form, 'titulo': 'Editar treinamento', 'acao': 'Salvar treinamento'},
    )


def exportar_excel(request):
    treinamentos = TreinamentoSeguranca.objects.prefetch_related('participantes').all()
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Treinamentos'

    sheet.merge_cells('A1:J1')
    sheet['A1'] = 'Relatorio de Treinamentos de Seguranca da Pintura'
    sheet['A1'].font = Font(bold=True, size=16, color='FFFFFF')
    sheet['A1'].fill = PatternFill('solid', fgColor='17212B')
    sheet['A1'].alignment = Alignment(horizontal='center')

    headers = [
        'ID',
        'Data',
        'Titulo',
        'Categoria',
        'Empresa',
        'Area',
        'Instrutor',
        'Carga horaria',
        'Validade',
        'Participantes',
    ]
    sheet.append(headers)

    header_fill = PatternFill('solid', fgColor='E8F3EF')
    for cell in sheet[2]:
        cell.font = Font(bold=True, color='17212B')
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')

    for treinamento in treinamentos:
        sheet.append(
            [
                treinamento.id,
                treinamento.data.strftime('%d/%m/%Y'),
                treinamento.titulo,
                treinamento.get_categoria_display(),
                treinamento.empresa,
                treinamento.area,
                treinamento.instrutor,
                treinamento.carga_horaria,
                treinamento.validade.strftime('%d/%m/%Y') if treinamento.validade else '',
                treinamento.total_participantes,
            ]
        )

    participantes_sheet = workbook.create_sheet('Participantes')
    participantes_sheet.append(['Treinamento', 'Data', 'Nome', 'Matricula', 'Empresa', 'Turno', 'Area'])
    for treinamento in treinamentos:
        for participante in treinamento.participantes.all():
            participantes_sheet.append(
                [
                    treinamento.titulo,
                    treinamento.data.strftime('%d/%m/%Y'),
                    participante.nome,
                    participante.matricula,
                    participante.empresa,
                    participante.turno,
                    participante.area,
                ]
            )

    for active_sheet in workbook.worksheets:
        for row in active_sheet.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = Alignment(vertical='top', wrap_text=True)
        for index, width in enumerate([10, 14, 36, 20, 24, 20, 24, 16, 16, 16], start=1):
            active_sheet.column_dimensions[get_column_letter(index)].width = width

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    filename = f"relatorio_treinamentos_seguranca_{timezone.localdate().strftime('%Y_%m_%d')}.xlsx"
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
