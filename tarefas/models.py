from django.db import models
from django.utils import timezone


class Tarefa(models.Model):
    class Prioridade(models.TextChoices):
        BAIXA = 'baixa', 'Baixa'
        MEDIA = 'media', 'Media'
        ALTA = 'alta', 'Alta'
        URGENTE = 'urgente', 'Urgente'

    class Status(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        EM_ANDAMENTO = 'em_andamento', 'Em andamento'
        CONCLUIDA = 'concluida', 'Concluida'
        CANCELADA = 'cancelada', 'Cancelada'

    titulo = models.CharField('titulo', max_length=160)
    descricao = models.TextField('descricao', blank=True)
    responsavel = models.CharField('responsavel', max_length=120, blank=True)
    area = models.CharField('area', max_length=120, blank=True)
    origem = models.CharField('app ou origem', max_length=120, blank=True)
    prioridade = models.CharField(max_length=16, choices=Prioridade.choices, default=Prioridade.MEDIA)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    prazo = models.DateField('prazo', blank=True, null=True)
    follow_up = models.TextField('follow-up', blank=True)
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    concluido_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['status', 'prazo', '-criado_em']
        verbose_name = 'tarefa de follow-up'
        verbose_name_plural = 'tarefas de follow-up'

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if self.status == self.Status.CONCLUIDA and self.concluido_em is None:
            self.concluido_em = timezone.now()
        if self.status != self.Status.CONCLUIDA:
            self.concluido_em = None
        super().save(*args, **kwargs)

    @property
    def mes_referencia(self):
        return self.criado_em.strftime('%m/%Y')

    @property
    def esta_aberta(self):
        return self.status not in [self.Status.CONCLUIDA, self.Status.CANCELADA]

    @property
    def esta_vencida(self):
        return self.esta_aberta and self.prazo and self.prazo < timezone.localdate()

    @property
    def vence_hoje(self):
        return self.esta_aberta and self.prazo == timezone.localdate()
