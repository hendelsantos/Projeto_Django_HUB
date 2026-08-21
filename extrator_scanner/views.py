from io import BytesIO
from pathlib import Path

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook
from pypdf import PdfReader


def index(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('scanner_file')

        if not uploaded_file:
            messages.error(request, 'Selecione um arquivo PDF para gerar o Excel.')
            return render(request, 'extrator_scanner/index.html')

        if Path(uploaded_file.name).suffix.lower() != '.pdf':
            messages.error(request, 'Por enquanto o extrator aceita apenas arquivos PDF.')
            return render(request, 'extrator_scanner/index.html')

        workbook = build_workbook_from_pdf(uploaded_file)
        output = BytesIO()
        workbook.save(output)
        output.seek(0)

        filename = f"{Path(uploaded_file.name).stem}_extraido.xlsx"
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    return render(request, 'extrator_scanner/index.html')


def build_workbook_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Dados extraidos'
    sheet.append(['arquivo', 'pagina', 'linha', 'texto'])

    rows_added = 0
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ''
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        if not lines:
            sheet.append([uploaded_file.name, page_number, '', 'Sem texto extraivel nesta pagina'])
            rows_added += 1
            continue

        for line_number, line in enumerate(lines, start=1):
            sheet.append([uploaded_file.name, page_number, line_number, line])
            rows_added += 1

    if rows_added == 0:
        sheet.append([uploaded_file.name, '', '', 'Nenhum texto extraivel encontrado no PDF'])

    for column_cells in sheet.columns:
        max_length = max(len(str(cell.value or '')) for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = min(max_length + 2, 80)

    return workbook

# Create your views here.
