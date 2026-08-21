from django.urls import path

from . import views

app_name = 'hub'

urlpatterns = [
    path('', views.home, name='home'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/exportar/', views.exportar_relatorio_geral, name='exportar_relatorio_geral'),
]
