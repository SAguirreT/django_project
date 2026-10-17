from django.urls import path

from .api_generic_views import ProductoListCreateAPIView, ProductoRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', ProductoListCreateAPIView.as_view(), name='api-producto-list-create'),
    path('<int:pk>/', ProductoRetrieveUpdateDestroyAPIView.as_view(), name='api-producto-detail'),
]
