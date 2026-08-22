from django.db import models
from django.utils import timezone


class TreinamentoSeguranca(models.Model):
    class Categoria(models.TextChoices):
        SEGURANCA = 'seguranca', 'Seguranca'
        PINTURA = 'pintura', 'Pintura'
        QUALIDADE = 'qualidade', 'Qualidade'
        MEIO_AMBIENTE = 'meio_ambiente', 'Meio ambiente'
        OUTROS = 'outros', 'Outros'

    class Status(models.TextChoices):
        AGENDADO = 'agendado', 'Agendado'
        REALIZADO = 'realizado', 'Realizado'
        CANCELADO = 'cancelado', 'Cancelado'

    titulo = models.CharField('titulo do treinamento', max_length=160)
    categoria = models.CharField(max_length=24, choices=Categoria.choices, default=Categoria.SEGURANCA)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AGENDADO)
    data = models.DateField('data do treinamento')
    hora_inicio = models.TimeField('hora de inicio', blank=True, null=True)
    hora_fim = models.TimeField('hora de termino', blank=True, null=True)
    empresa = models.CharField('empresa', max_length=140)
    area = models.CharField('area', max_length=120, default='Pintura')
    instrutor = models.CharField('instrutor', max_length=120, blank=True)
    carga_horaria = models.CharField('carga horaria', max_length=40, blank=True)
    validade = models.DateField('validade', blank=True, null=True)
    documento = models.FileField('documento escaneado', upload_to='treinamentos/', blank=True)
    texto_participantes = models.TextField('texto dos participantes', blank=True)
    observacoes = models.TextField('observacoes', blank=True)
    total_participantes = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data', '-criado_em']
        verbose_name = 'treinamento de seguranca'
        verbose_name_plural = 'treinamentos de seguranca'

    def __str__(self):
        return f'{self.titulo} - {self.data:%d/%m/%Y}'

    def save(self, *args, **kwargs):
        if self.total_participantes and self.status == self.Status.AGENDADO:
            self.status = self.Status.REALIZADO
        super().save(*args, **kwargs)

    @property
    def mes_referencia(self):
        return self.data.strftime('%m/%Y')

    @property
    def esta_vencido(self):
        return self.validade and self.validade < timezone.localdate()

    @property
    def horario(self):
        if self.hora_inicio and self.hora_fim:
            return f'{self.hora_inicio:%H:%M} - {self.hora_fim:%H:%M}'
        if self.hora_inicio:
            return f'{self.hora_inicio:%H:%M}'
        return 'Sem horario'


class ParticipanteTreinamento(models.Model):
    treinamento = models.ForeignKey(
        TreinamentoSeguranca,
        on_delete=models.CASCADE,
        related_name='participantes',
    )
    nome = models.CharField('nome', max_length=160)
    matricula = models.CharField('matricula', max_length=60, blank=True)
    empresa = models.CharField('empresa', max_length=140, blank=True)
    turno = models.CharField('turno', max_length=80, blank=True)
    area = models.CharField('area', max_length=120, blank=True)
    criado_em = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['nome']
        verbose_name = 'participante de treinamento'
        verbose_name_plural = 'participantes de treinamento'

    def __str__(self):
        return self.nome
