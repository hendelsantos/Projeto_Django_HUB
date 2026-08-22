from django.contrib import admin

from .models import Tarefa


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'responsavel', 'area', 'prioridade', 'status', 'prazo', 'criado_em']
    list_filter = ['status', 'prioridade', 'area', 'origem', 'prazo']
    search_fields = ['titulo', 'descricao', 'responsavel', 'area', 'origem', 'follow_up']
    readonly_fields = ['criado_em', 'atualizado_em', 'concluido_em']
