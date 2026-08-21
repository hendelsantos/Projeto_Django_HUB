from django.db import models
from django.utils import timezone


class ChamadoZeladoria(models.Model):
    class Status(models.TextChoices):
        NOVO = 'novo', 'Novo'
        EM_ANALISE = 'em_analise', 'Em analise'
        TICKET_ABERTO = 'ticket_aberto', 'Ticket aberto'
        EM_ANDAMENTO = 'em_andamento', 'Em andamento'
        CONCLUIDO = 'concluido', 'Concluido'
        CANCELADO = 'cancelado', 'Cancelado'

    titulo = models.CharField('titulo do chamado', max_length=140, default='Chamado de zeladoria')
    solicitante = models.CharField('nome do solicitante', max_length=120)
    local = models.CharField('local', max_length=160)
    descricao = models.TextField('descricao da necessidade')
    foto = models.ImageField('foto', upload_to='zeladoria/%Y/%m/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOVO)
    ticket_oficial = models.CharField('ticket oficial', max_length=80, blank=True)
    observacoes = models.TextField('observacoes de follow-up', blank=True)
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'chamado de zeladoria'
        verbose_name_plural = 'chamados de zeladoria'

    def __str__(self):
        return f'{self.titulo} - {self.local}'

    @property
    def mes_referencia(self):
        return self.criado_em.strftime('%m/%Y')

# Create your models here.
