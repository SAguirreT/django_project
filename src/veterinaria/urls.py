from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # PROPIETARIOS
    path('propietarios/', views.listar_propietarios, name='listar_propietarios'),
    path('propietarios/nuevo/', views.crear_propietario, name='crear_propietario'),
    path('propietarios/editar/<int:id>/', views.actualizar_propietario, name='actualizar_propietario'),
    path('propietarios/eliminar/<int:id>/', views.eliminar_propietario, name='eliminar_propietario'),
]