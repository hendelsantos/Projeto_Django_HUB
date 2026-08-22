from django.urls import path

from . import views

app_name = 'hub'

urlpatterns = [
    path('', views.home, name='home'),
    path('buscar/', views.buscar, name='buscar'),
    path('photocloud/', views.photocloud, name='photocloud'),
    path('photocloud/qrcode/', views.photocloud_qrcode, name='photocloud_qrcode'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/exportar/', views.exportar_relatorio_geral, name='exportar_relatorio_geral'),
]
