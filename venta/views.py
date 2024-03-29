from django.shortcuts import render, redirect, get_object_or_404
from venta.models import Venta,Detalleventa
from venta.forms import VentaForm, VentaUpdateForm
from venta.forms import DetalleventaForm
from django.contrib import messages
from django.urls import reverse, resolve
from django.urls import reverse
from . import urls
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal
import locale
from django.db import transaction
from django.db.models import F

@login_required()
def venta_listar(request):
    titulo="Venta"
    modulo="Usuarios"
    ventas= Venta.objects.all()
    context={
        "titulo":titulo,
        "modulo":modulo,
        "ventas":ventas
    }
    return render(request,"ventas/ventas/listar.html", context)



@login_required()
def venta_crear(request, pk=0):
    titulo = "Ventas"
    modulo = "Usuarios"
    venta= Venta.objects.filter(id=pk)
    detalleventas = Detalleventa.objects.filter(grupo_id=pk)
    total_valores = detalleventas.aggregate(Sum('valortotal'))['valortotal__sum'] or Decimal(0.0)
     
    locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")
    total_valores_colombiano = locale.currency(total_valores, grouping=True, symbol=False)
    
    # para el form de creación del grupo
    if request.method == 'POST' and 'form-grupo' in request.POST:
        form_venta = VentaForm(request.POST)
        if form_venta.is_valid():
            venta_nuevo = form_venta.save(commit=False)

            # Asignar el usuario autenticado (Empleado) al campo Empleado del proyecto
            venta_nuevo.Empleado = request.user

            # Guardar el proyecto en la base de datos
            venta_nuevo.save()

            return redirect('ventas-crear', venta_nuevo.id)
        else:
            messages.danger(request, 'Error al crear el grupo.')

    else:
        form_venta = VentaForm()

    # para el form de agregar aprendiz al grupo
    if request.method == 'POST' and 'form-detalleventa' in request.POST:
        form_detalleventa = DetalleventaForm(request.POST)
        if form_detalleventa.is_valid():
            detalleventa_data = form_detalleventa.cleaned_data
            producto_id = detalleventa_data['producto'].id

            # Verificar si el producto ya existe en el grupo
            existing_detalleventa = Detalleventa.objects.filter(grupo_id=pk, producto_id=producto_id).first()

            if existing_detalleventa:
                # Si el producto ya existe, solo actualiza la cantidad
                existing_detalleventa.cantidad += detalleventa_data['cantidad']
                existing_detalleventa.save()
                messages.success(request, 'Se actualizó la cantidad del producto.')
            else:
                # Si el producto no existe, crea un nuevo registro
                detalleventa = form_detalleventa.save(commit=False)
                detalleventa.grupo_id = pk
                detalleventa.save()
                messages.success(request, 'Detalle venta  se agregó correctamente.')

            return redirect('ventas-crear', pk)
        else:
            messages.error(request, "Formulario inválido. Verifica los datos ingresados.")
    else:
        form_detalleventa = DetalleventaForm()

    context = {
        "form_detalleventa": form_detalleventa,
        "form_venta": form_venta,
        "titulo": titulo,
        "modulo": modulo,
        "venta": venta,
        "detalleventas": detalleventas,
        'total_valores': total_valores,
        'total_valores_colombiano': total_valores_colombiano,
    }
    return render(request, "ventas/ventas/crear.html", context)

@login_required()
def venta_modificar(request,pk):
    titulo="Ventas"
    
    venta= Venta.objects.get(id=pk)
    
    if request.method== 'POST':
        form= VentaUpdateForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('ventas')
    else:
        form= VentaUpdateForm(instance=venta)
    context={
        "titulo":titulo,
        "form":form
        }
    return render(request,"ventas/ventas/modificar.html", context)




@login_required()  
def venta_eliminar(request, pk):
    venta = Venta.objects.filter(id=pk)
    detalleventas = Detalleventa.objects.filter(grupo_id=pk)
    productos_sin_stock_suficiente = []

    if detalleventas:
        try:
            with transaction.atomic():
                for detalleventa in detalleventas:
                    producto = detalleventa.producto
                    nueva_cantidad_stock = producto.stock - detalleventa.cantidad
                    if nueva_cantidad_stock >= 0:
                        producto.stock = nueva_cantidad_stock
                        producto.save()
                    else:
                        productos_sin_stock_suficiente.append((producto, nueva_cantidad_stock))

                if productos_sin_stock_suficiente:
                    for producto, cantidad_faltante in productos_sin_stock_suficiente:
                        error_message = f'Cantidad insuficiente de stock para {producto.nombre}. Stock disponible: {producto.stock}'
                        messages.error(request, error_message)
                    return redirect('ventas')

            venta.update(estado="0")  # Cambiar el estado de la venta a "0"
            return redirect('ventas')
        except Exception as e:
            messages.error(request, f'Error al actualizar el stock: {str(e)}')
    else:
        messages.error(request, 'No puedes finalizar la venta sin un detalle venta. Agrega al menos uno antes de finalizarla.')

    return redirect('ventas')

@login_required()
def detalleventa_eliminar(request,pk):
    detalleventa  = get_object_or_404(Detalleventa, id=pk)
    id_proy=detalleventa.grupo.id
    detalleventa.delete()
    return redirect('ventas-crear',id_proy)


@login_required()
def venta_final(request,pk):
    titulo="Venta"
    modulo="Usuarios"
    venta= Venta.objects.filter(id=pk)
    ventas= Venta.objects.filter(id=pk)
    detalleventas  = Detalleventa.objects.filter(grupo_id=pk)
    total_valores = detalleventas.aggregate(Sum('valortotal'))['valortotal__sum'] or Decimal(0.0)
 
    locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")
    total_valores_colombiano = locale.currency(total_valores, grouping=True, symbol=False)
    context={
        "titulo":titulo,
        "modulo":modulo,
        "ventas":ventas,
        "venta":venta,
        "detalleventas": detalleventas,
        'total_valores': total_valores,
        'total_valores_colombiano': total_valores_colombiano,

    }
    return render(request,"ventas/ventas/listar_Venta.html", context)