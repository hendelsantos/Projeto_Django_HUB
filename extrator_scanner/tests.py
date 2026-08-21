from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from openpyxl import load_workbook
from pypdf import PdfWriter


class ExtratorScannerTests(TestCase):
    def test_index_page_loads(self):
        response = self.client.get(reverse('extrator_scanner:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gerar Excel a partir de PDF')

    def test_pdf_upload_returns_excel(self):
        pdf = BytesIO()
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        writer.write(pdf)
        pdf.seek(0)

        uploaded_file = SimpleUploadedFile(
            'scanner.pdf',
            pdf.read(),
            content_type='application/pdf',
        )

        response = self.client.post(
            reverse('extrator_scanner:index'),
            {'scanner_file': uploaded_file},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

        workbook = load_workbook(BytesIO(response.content))
        sheet = workbook.active
        self.assertEqual(sheet['A1'].value, 'arquivo')
        self.assertEqual(sheet['D2'].value, 'Sem texto extraivel nesta pagina')

# Create your tests here.
