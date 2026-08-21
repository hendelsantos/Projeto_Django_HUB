from django.urls import path

from . import views

app_name = 'roupeiro'

urlpatterns = [
    path('', views.index, name='index'),
    path('novo/', views.criar, name='criar'),
    path('mapa/', views.mapa, name='mapa'),
    path('painel/', views.painel, name='painel'),
    path('exportar/', views.exportar_excel, name='exportar_excel'),
    path('<int:pk>/', views.detalhe, name='detalhe'),
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/liberar/', views.liberar, name='liberar'),
]
