from django.contrib import admin

from .models import ParticipanteTreinamento, TreinamentoSeguranca


class ParticipanteInline(admin.TabularInline):
    model = ParticipanteTreinamento
    extra = 0


@admin.register(TreinamentoSeguranca)
class TreinamentoSegurancaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data', 'hora_inicio', 'empresa', 'area', 'instrutor', 'status', 'total_participantes', 'validade']
    list_filter = ['status', 'categoria', 'empresa', 'area', 'data', 'validade']
    search_fields = ['titulo', 'empresa', 'area', 'instrutor', 'participantes__nome']
    readonly_fields = ['total_participantes', 'criado_em', 'atualizado_em']
    inlines = [ParticipanteInline]


@admin.register(ParticipanteTreinamento)
class ParticipanteTreinamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'treinamento', 'empresa', 'turno', 'area']
    list_filter = ['empresa', 'turno', 'area']
    search_fields = ['nome', 'matricula', 'empresa', 'treinamento__titulo']
