from django.contrib import admin

from .models import ChamadoZeladoria


@admin.register(ChamadoZeladoria)
class ChamadoZeladoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'solicitante', 'local', 'status', 'ticket_oficial', 'criado_em')
    list_filter = ('status', 'criado_em')
    list_editable = ('status', 'ticket_oficial')
    readonly_fields = ('criado_em', 'atualizado_em')
    search_fields = ('titulo', 'solicitante', 'local', 'descricao', 'ticket_oficial')

# Register your models here.
