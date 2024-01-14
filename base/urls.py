
from django.contrib import admin
from django.urls import path, include
from base.views import principal, logout_user ,mostrar_pdf_ayuda
# para las iamgenes
from django.conf import settings
from django.conf.urls.static import static
# para la gestion de login y contraseña
from django.contrib.auth import views as auth_views
urlpatterns = [
    #gestion de login y contraseña
    path('',auth_views.LoginView.as_view(),name='inicio'),
    path('reiniciar/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('reiniciar/enviar',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reiniciar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reiniciar/completo',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('logout/',logout_user,name="logout"),
    
    path('admin/', admin.site.urls),
    path('inicio/', principal, name="index" ),
    path('usuarios/', include('usuarios.urls') ),
    path('producto/', include('producto.urls')),
    path('venta/', include('venta.urls')),
    path('compra/', include('compra.urls')),
    path('proveedor/', include('proveedor.urls')),
   path('cliente/', include('cliente.urls')),
   path('ayuda/',mostrar_pdf_ayuda, name='ayuda'),


    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
