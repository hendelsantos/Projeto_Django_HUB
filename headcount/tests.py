from datetime import date
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from openpyxl import Workbook
from PIL import Image

from .models import BirthdayList, HeadcountImport, HeadcountMember
from .services import import_headcount, process_birthday_list


def make_headcount_file():
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(['Name', 'Shift', 'Work Group', 'Team'])
    sheet.append(['Maria Oliveira', '1 turno', 'Paint', 'A'])
    sheet.append(['Carlos Lima', '2 turno', 'Paint', 'B'])
    output = BytesIO()
    workbook.save(output)
    return SimpleUploadedFile(
        'headcount.xlsx',
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )


def make_image_file():
    image = Image.new('RGB', (10, 10), color='white')
    output = BytesIO()
    image.save(output, format='PNG')
    return SimpleUploadedFile('aniversariantes.png', output.getvalue(), content_type='image/png')


class HeadcountTests(TestCase):
    def test_import_headcount_and_process_birthdays(self):
        importacao = HeadcountImport.objects.create(
            mes=date(2026, 8, 1),
            arquivo=make_headcount_file(),
        )

        total = import_headcount(importacao)
        lista = BirthdayList.objects.create(
            mes=date(2026, 8, 1),
            imagem=make_image_file(),
            texto_extraido='Maria Oliveira\nPessoa Fora',
            headcount=importacao,
        )
        birthdays = process_birthday_list(lista)

        self.assertEqual(total, 2)
        self.assertEqual(birthdays, 2)
        self.assertTrue(HeadcountMember.objects.filter(nome='Maria Oliveira', turno='1 turno').exists())
        self.assertTrue(lista.nomes.filter(nome='Maria Oliveira', membro__isnull=False).exists())

    def test_index_loads(self):
        response = self.client.get(reverse('headcount:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Headcount e aniversariantes')

# Create your tests here.
