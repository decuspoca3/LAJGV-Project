from django.urls import path
from . import views
from proveedor.views import proveedor_listar, proveedor_crear, proveedor_modificar,proveedor_eliminar 

urlpatterns = [
    path('proveedor/', proveedor_listar, name="proveedor"),
    path('proveedor/crear/', proveedor_crear, name="proveedor-crear"),
    path('proveedor/modificar/<int:pk>/',proveedor_modificar, name="proveedor-modificar"),
    path('proveedor/eliminar/<int:pk>/', proveedor_eliminar, name="proveedor-eliminar"),
]

