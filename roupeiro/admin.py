from django.contrib import admin

from .models import Armario


@admin.register(Armario)
class ArmarioAdmin(admin.ModelAdmin):
    list_display = (
        'numero',
        'status',
        'usuario',
        'turno',
        'tamanho_camisa',
        'tamanho_camisa_numero',
        'tamanho_calca',
        'tamanho_calca_numero',
        'tamanho_macacao',
        'tamanho_macacao_numero',
    )
    list_filter = ('status', 'turno', 'tamanho_camisa', 'tamanho_calca', 'tamanho_macacao')
    search_fields = ('usuario', 'observacoes')
    ordering = ('numero',)

# Register your models here.
