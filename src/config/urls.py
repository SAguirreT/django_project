from django.urls import path
from . import views  # El punto significa "importa views de esta misma carpeta"

urlpatterns = [
    # Cuando entren a la ruta principal, ejecuta la vista 'inicio_farmacia'
    path('', views.inicio_farmacia, name='inicio'),
]