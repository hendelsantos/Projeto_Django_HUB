from django.db import models
from django.conf import settings


class AccessLog(models.Model):
    method = models.CharField('metodo', max_length=10)
    path = models.CharField('rota acessada', max_length=500)
    status_code = models.PositiveSmallIntegerField('codigo de resposta')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='usuario',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    ip_address = models.GenericIPAddressField('endereco IP', blank=True, null=True)
    user_agent = models.TextField('navegador/dispositivo', blank=True)
    referer = models.CharField('origem', max_length=500, blank=True)
    created_at = models.DateTimeField('data do acesso', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'acesso'
        verbose_name_plural = 'metricas de acesso'

    def __str__(self):
        return f'{self.method} {self.path} - {self.status_code}'

# Create your models here.
