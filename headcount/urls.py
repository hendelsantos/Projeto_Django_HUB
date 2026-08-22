from django.urls import path

from . import views

app_name = 'headcount'

urlpatterns = [
    path('', views.index, name='index'),
    path('importar/', views.importar, name='importar'),
    path('painel/', views.painel, name='painel'),
    path('<int:pk>/', views.detalhe, name='detalhe'),
    path('<int:pk>/exportar/', views.exportar_excel, name='exportar_excel'),
]
