from django.urls import path
from usuarios.views import usuario_listar, usuario_crear, usuario_modificar, usuario_eliminar ,inactivos_listar

urlpatterns = [
    path('usuario/', usuario_listar, name="usuarios" ),
    path('usuario/inactivos', inactivos_listar, name="inactivos" ),
    path('usuario/crear/', usuario_crear, name="usuarios-crear" ),
    path('usuario/modificar/<int:pk>/', usuario_modificar, name="usuarios-modificar" ),
    path('usuario/eliminar/<int:pk>/', usuario_eliminar, name="usuarios-eliminar" ),
    

]
