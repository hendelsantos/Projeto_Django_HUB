from django.db import models
from django.utils import timezone


class Armario(models.Model):
    class Status(models.TextChoices):
        LIVRE = 'livre', 'Livre'
        OCUPADO = 'ocupado', 'Ocupado'
        MANUTENCAO = 'manutencao', 'Manutencao'
        INATIVO = 'inativo', 'Inativo'

    class Turno(models.TextChoices):
        PRIMEIRO = 'primeiro', '1 turno'
        SEGUNDO = 'segundo', '2 turno'
        TERCEIRO = 'terceiro', '3 turno'
        ADMINISTRATIVO = 'administrativo', 'Administrativo'
        OUTRO = 'outro', 'Outro'

    class TamanhoRoupa(models.TextChoices):
        PP = 'pp', 'PP'
        P = 'p', 'P'
        M = 'm', 'M'
        G = 'g', 'G'
        GG = 'gg', 'GG'
        XG = 'xg', 'XG'
        XGG = 'xgg', 'XGG'
        ESPECIAL = 'especial', 'Especial'

    numero = models.PositiveIntegerField('numero do armario', unique=True)
    usuario = models.CharField('nome do usuario', max_length=140, blank=True)
    turno = models.CharField(max_length=24, choices=Turno.choices, blank=True)
    tamanho_camisa = models.CharField('tamanho da camisa', max_length=16, choices=TamanhoRoupa.choices, blank=True)
    tamanho_camisa_numero = models.PositiveIntegerField('tamanho numerico da camisa', blank=True, null=True)
    tamanho_calca = models.CharField('tamanho da calca', max_length=16, choices=TamanhoRoupa.choices, blank=True)
    tamanho_calca_numero = models.PositiveIntegerField('tamanho numerico da calca', blank=True, null=True)
    tamanho_macacao = models.CharField('tamanho do macacao', max_length=16, choices=TamanhoRoupa.choices, blank=True)
    tamanho_macacao_numero = models.PositiveIntegerField('tamanho numerico do macacao', blank=True, null=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.LIVRE)
    observacoes = models.TextField('observacoes', blank=True)
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['numero']
        verbose_name = 'armario'
        verbose_name_plural = 'armarios'

    def __str__(self):
        return f'Armario {self.numero}'

    def save(self, *args, **kwargs):
        if self.usuario and self.status == self.Status.LIVRE:
            self.status = self.Status.OCUPADO
        if not self.usuario and self.status == self.Status.OCUPADO:
            self.status = self.Status.LIVRE
        super().save(*args, **kwargs)

    @property
    def mes_referencia(self):
        return self.criado_em.strftime('%m/%Y')

# Create your models here.
