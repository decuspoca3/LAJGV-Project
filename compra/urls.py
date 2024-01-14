from django.urls import path

#from compra.views import usuario_listar, usuario_crear, usuario_modificar, usuario_eliminar
from compra.views import  compra_listar,  compra_crear,  compra_modificar,  compra_eliminar
from compra.views import detallecompra_eliminar,  compra_final




urlpatterns = [

    


    path('compra/', compra_listar, name="compras" ),

    path('compra/crear/', compra_crear, name="compras-crear" ),
    path('compra/gestionar/<int:pk>/', compra_crear, name="compras-crear" ),

    path('compra/modificar/<int:pk>/', compra_modificar, name="compras-modificar" ),
    path('compra/eliminar/<int:pk>/', compra_eliminar, name="compras-eliminar" ),

    path('compra/detallecompra/eliminar/<int:pk>/', detallecompra_eliminar, name="detallecompra-eliminar" ),
    path('compra/final/<int:pk>/', compra_final, name="compras-final" ),

]
