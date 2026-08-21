from django.db import models
from django.utils import timezone


class ChamadoTI(models.Model):
    class Categoria(models.TextChoices):
        CONTA = 'conta', 'Abertura ou acesso de conta'
        EQUIPAMENTO = 'equipamento', 'Equipamento'
        SISTEMA = 'sistema', 'Sistema'
        REDE = 'rede', 'Rede'
        EMAIL = 'email', 'E-mail'
        OUTROS = 'outros', 'Outros'

    class Prioridade(models.TextChoices):
        BAIXA = 'baixa', 'Baixa'
        MEDIA = 'media', 'Media'
        ALTA = 'alta', 'Alta'
        URGENTE = 'urgente', 'Urgente'

    class Status(models.TextChoices):
        NOVO = 'novo', 'Novo'
        EM_ANALISE = 'em_analise', 'Em analise'
        EM_ANDAMENTO = 'em_andamento', 'Em andamento'
        AGUARDANDO_TERCEIROS = 'aguardando_terceiros', 'Aguardando terceiros'
        CONCLUIDO = 'concluido', 'Concluido'
        CANCELADO = 'cancelado', 'Cancelado'

    titulo = models.CharField('titulo do chamado', max_length=140)
    solicitante = models.CharField('nome do solicitante', max_length=120)
    setor = models.CharField('setor ou area', max_length=120, blank=True)
    categoria = models.CharField(max_length=24, choices=Categoria.choices, default=Categoria.OUTROS)
    prioridade = models.CharField(max_length=16, choices=Prioridade.choices, default=Prioridade.MEDIA)
    descricao = models.TextField('descricao do membro')
    status = models.CharField(max_length=28, choices=Status.choices, default=Status.NOVO)
    ticket_oficial = models.CharField('ticket oficial', max_length=80, blank=True)
    solucao = models.TextField('solucao ou follow-up', blank=True)
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    concluido_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'chamado de TI'
        verbose_name_plural = 'chamados de TI'

    def __str__(self):
        return f'{self.titulo} - {self.solicitante}'

    def save(self, *args, **kwargs):
        if self.status == self.Status.CONCLUIDO and self.concluido_em is None:
            self.concluido_em = timezone.now()
        if self.status != self.Status.CONCLUIDO:
            self.concluido_em = None
        super().save(*args, **kwargs)

    @property
    def mes_referencia(self):
        return self.criado_em.strftime('%m/%Y')

# Create your models here.
