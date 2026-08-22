from django.urls import path

from . import views

app_name = 'tarefas'

urlpatterns = [
    path('', views.index, name='index'),
    path('nova/', views.criar, name='criar'),
    path('kanban/', views.kanban, name='kanban'),
    path('painel/', views.painel, name='painel'),
    path('exportar/', views.exportar_excel, name='exportar_excel'),
    path('<int:pk>/', views.detalhe, name='detalhe'),
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/concluir/', views.concluir, name='concluir'),
    path('<int:pk>/status/', views.alterar_status, name='alterar_status'),
]
