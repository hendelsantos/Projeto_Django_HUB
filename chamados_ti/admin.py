from django.contrib import admin

from .models import ChamadoTI


@admin.register(ChamadoTI)
class ChamadoTIAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'titulo',
        'solicitante',
        'categoria',
        'prioridade',
        'status',
        'ticket_oficial',
        'criado_em',
    )
    list_filter = ('status', 'categoria', 'prioridade', 'criado_em')
    list_editable = ('prioridade', 'status', 'ticket_oficial')
    readonly_fields = ('criado_em', 'atualizado_em', 'concluido_em')
    search_fields = ('titulo', 'solicitante', 'setor', 'descricao', 'ticket_oficial')

# Register your models here.
