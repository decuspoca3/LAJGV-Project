from django.urls import path
from . import views
from cliente.views import cliente_listar, cliente_crear, cliente_modificar,cliente_eliminar 

urlpatterns = [
    path('cliente/', cliente_listar, name="cliente"),
    path('cliente/crear/', cliente_crear, name="cliente-crear"),
    path('cliente/modificar/<int:pk>/',cliente_modificar, name="cliente-modificar"),
    path('cliente/eliminar/<int:pk>/', cliente_eliminar, name="cliente-eliminar"),
]

