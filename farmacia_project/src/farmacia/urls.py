from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('zonas/', views.zona_list, name='zona_list'),
    path('zonas/nueva/', views.zona_create, name='zona_create'),
    path('farmacias/', views.farmacia_list, name='farmacia_list'),
    path('farmacias/nueva/', views.farmacia_create, name='farmacia_create'),
    path('evaluaciones/', views.evaluacion_list, name='evaluacion_list'),
    path('evaluaciones/nueva/', views.evaluacion_create, name='evaluacion_create'),
    path('evaluaciones/<int:evaluacion_id>/', views.evaluacion_detail, name='evaluacion_detail'),
    path('comparacion/', views.comparacion, name='comparacion'),
]
