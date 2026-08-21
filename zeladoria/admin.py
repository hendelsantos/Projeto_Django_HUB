from django.contrib import admin

from .models import ChamadoZeladoria


@admin.register(ChamadoZeladoria)
class ChamadoZeladoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'solicitante', 'local', 'status', 'ticket_oficial', 'criado_em')
    list_filter = ('status', 'criado_em')
    search_fields = ('solicitante', 'local', 'descricao', 'ticket_oficial')

# Register your models here.
