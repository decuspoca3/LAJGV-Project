from django.shortcuts import redirect, render
from usuarios.models import Usuario
from producto.models import Producto
from venta.models import Venta
from compra.models import Compra
from proveedor.models import Proveedor
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from cliente.models import Cliente 
from django.shortcuts import render

@login_required
def principal(request):
    titulo="Bienvenido al Sistema"
    usuarios= Usuario.objects.all().count()
    producto=Producto.objects.all().count()
    ventas=Venta.objects.all().count()
    compras=Compra.objects.all().count()
    proveedors= Proveedor.objects.all().count()
    clientes = Cliente.objects.all().count()

    context={
        
        "usuarios":usuarios,
        "producto":producto,
        "ventas":ventas,
        "compras":compras,
        "proveedors": proveedors,
        "clientes":  clientes,
        "titulo":titulo,
        
    }
    return render(request, "index.html",context)
@login_required
def logout_user(request):
    logout(request)
    return redirect('inicio')

@login_required
def mostrar_pdf_ayuda(request):
    titulo="Ayuda"
    context = {
        "titulo":titulo,
    }
    return render(request, 'ayuda/ayuda/ayuda.html',context)
