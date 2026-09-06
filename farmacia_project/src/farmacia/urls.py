from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('categorias/', views.entidad_list, {'entidad': 'categoria'}, name='categoria_list'),
    path('categorias/nuevo/', views.entidad_create, {'entidad': 'categoria'}, name='categoria_create'),
    path('productos/', views.entidad_list, {'entidad': 'producto'}, name='producto_list'),
    path('productos/nuevo/', views.entidad_create, {'entidad': 'producto'}, name='producto_create'),
    path('productos/<int:pk>/editar/', views.entidad_update, {'entidad': 'producto'}, name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.entidad_delete, {'entidad': 'producto'}, name='producto_delete'),
    path('proveedores/', views.entidad_list, {'entidad': 'proveedor'}, name='proveedor_list'),
    path('clientes/', views.entidad_list, {'entidad': 'cliente'}, name='cliente_list'),
    path('ventas/', views.entidad_list, {'entidad': 'venta'}, name='venta_list'),
    path('<str:entidad>/', views.entidad_list, name='entidad_list'),
    path('<str:entidad>/nuevo/', views.entidad_create, name='entidad_create'),
    path('<str:entidad>/<int:pk>/editar/', views.entidad_update, name='entidad_update'),
    path('<str:entidad>/<int:pk>/eliminar/', views.entidad_delete, name='entidad_delete'),
]
