from django.db import models
from django.utils import timezone


class HeadcountImport(models.Model):
    mes = models.DateField('mes de referencia')
    arquivo = models.FileField('arquivo headcount', upload_to='headcount/%Y/%m/')
    total_membros = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-mes', '-criado_em']
        verbose_name = 'importacao de headcount'
        verbose_name_plural = 'importacoes de headcount'

    def __str__(self):
        return f'Headcount {self.mes.strftime("%m/%Y")}'


class HeadcountMember(models.Model):
    importacao = models.ForeignKey(HeadcountImport, related_name='membros', on_delete=models.CASCADE)
    nome = models.CharField(max_length=180)
    nome_normalizado = models.CharField(max_length=180, db_index=True)
    turno = models.CharField(max_length=80, blank=True)
    work_group = models.CharField('work group', max_length=140, blank=True)
    team = models.CharField('team', max_length=140, blank=True)
    area = models.CharField(max_length=180, blank=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'membro do headcount'
        verbose_name_plural = 'membros do headcount'

    def __str__(self):
        return self.nome


class BirthdayList(models.Model):
    mes = models.DateField('mes dos aniversariantes')
    imagem = models.ImageField('foto/lista de aniversariantes', upload_to='aniversariantes/%Y/%m/')
    texto_extraido = models.TextField('texto extraido ou digitado da imagem', blank=True)
    headcount = models.ForeignKey(HeadcountImport, related_name='listas_aniversariantes', on_delete=models.CASCADE)
    criado_em = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-mes', '-criado_em']
        verbose_name = 'lista de aniversariantes'
        verbose_name_plural = 'listas de aniversariantes'

    def __str__(self):
        return f'Aniversariantes {self.mes.strftime("%m/%Y")}'


class BirthdayName(models.Model):
    lista = models.ForeignKey(BirthdayList, related_name='nomes', on_delete=models.CASCADE)
    nome = models.CharField(max_length=180)
    nome_normalizado = models.CharField(max_length=180, db_index=True)
    membro = models.ForeignKey(HeadcountMember, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['nome']
        verbose_name = 'aniversariante'
        verbose_name_plural = 'aniversariantes'

    def __str__(self):
        return self.nome

# Create your models here.
