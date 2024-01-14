from django.shortcuts import render, redirect, get_object_or_404
from compra.models import Compra,Detallecompra
from compra.forms import CompraForm, CompraUpdateForm
from compra.forms import DetallecompraForm
from django.contrib import messages
from django.urls import reverse, resolve
from django.urls import reverse
from . import urls
from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal
import locale
from django.db import transaction
from django.db.models import F

@login_required()
def compra_listar(request):
    titulo="Compra"
    modulo="Usuarios"
    compras= Compra.objects.all()
    context={
        "titulo":titulo,
        "modulo":modulo,
        "compras":compras
    }
    return render(request,"compras/compras/listar.html", context)



@login_required()
def compra_crear(request, pk=0):
    titulo = "Compras"
    modulo = "Usuarios"
    compra = Compra.objects.filter(id=pk)
    detallecompras = Detallecompra.objects.filter(grupo_id=pk)
    total_valores = detallecompras.aggregate(Sum('valortotal'))['valortotal__sum'] or Decimal(0.0)
     
    locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")
    total_valores_colombiano = locale.currency(total_valores, grouping=True, symbol=False)
    
    if request.method == 'POST' and 'form-grupo' in request.POST:
        form_compra = CompraForm(request.POST)
        if form_compra.is_valid():
            compra_nuevo = form_compra.save(commit=False)

            compra_nuevo.Empleado = request.user


            compra_nuevo.save()

            return redirect('compras-crear',compra_nuevo.id)
        else:
            messages.danger(request, 'Error al crear el compra.')

    else:
        form_compra = CompraForm()

    if request.method == 'POST' and 'form-detallecompra' in request.POST:
        form_detallecompra = DetallecompraForm(request.POST)
        if form_detallecompra.is_valid():
            detallecompra_data = form_detallecompra.cleaned_data
            producto_id = detallecompra_data['producto'].id

            # Verificar si el producto ya existe en el grupo
            existing_detallecompra = Detallecompra.objects.filter(grupo_id=pk, producto_id=producto_id).first()

            if existing_detallecompra:
                # Si el producto ya existe, solo actualiza la cantidad
                existing_detallecompra.cantidad += detallecompra_data['cantidad']
                existing_detallecompra.save()
                messages.success(request, 'Se actualizó la cantidad del producto.')
            else:
                # Si el producto no existe, crea un nuevo registro
                precio_decimal = form_detallecompra.cleaned_data['precio_str']
                detallecompra = form_detallecompra.save(commit=False)
                detallecompra.grupo_id = pk
                detallecompra.Precio = precio_decimal
                detallecompra.save()

                messages.success(request, 'Detalle Compra se agregó correctamente.')

            return redirect('compras-crear', pk)
        else:
           messages.error(request, "Formulario inválido. Verifica los datos ingresados.")

    else:
        form_detallecompra = DetallecompraForm()

    context = {
        "form_detallecompra": form_detallecompra,
        "form_compra": form_compra,
        "titulo": titulo,
        "modulo": modulo,
        "compra": compra,
        "detallecompras": detallecompras,
        'total_valores': total_valores,
        'total_valores_colombiano': total_valores_colombiano,
    }
    return render(request, "compras/compras/crear.html", context)

@login_required() 
def compra_modificar(request,pk):
    titulo="compras"
    
    compra = Compra.objects.get(id=pk)
    
    if request.method== 'POST':
        form= compraUpdateForm(request.POST, instance=compra)
        if form.is_valid():
            form.save()
            return redirect('compras')
    else:
        form= CompraUpdateForm(instance=compra)
    context={
        "titulo":titulo,
        "form":form
        }
    return render(request,"compras/compras/modificar.html", context)

@login_required()
def compra_eliminar(request, pk):
    compra = Compra.objects.filter(id=pk)
    detallecompras = Detallecompra.objects.filter(grupo_id=pk)

    if detallecompras:
        try:
            with transaction.atomic():
                for detallecompra in detallecompras:
                    producto = detallecompra.producto
                    producto.stock = F('stock') + detallecompra.cantidad
                    producto.save()
            compra.update(estado="0")  # Cambiar el estado del proyecto a "0"
            return redirect('compras')
        except Exception as e:
            messages.error(request, f'Error al actualizar el stock: {str(e)}')
    else:
        messages.error(request, 'No puedes finalizar la Compra sin un detalle compra. Agrega al menos uno antes de finalizarlo.')

    return redirect('compras')


@login_required()
def detallecompra_eliminar(request,pk):
    detallecompra = get_object_or_404(Detallecompra, id=pk)
    id_proy= detallecompra.grupo.id
    detallecompra.delete()
    return redirect('compras-crear',id_proy)


@login_required()
def compra_final(request,pk):
    titulo="Compra"
    modulo="Usuarios"
    compra = Compra.objects.filter(id=pk)
    compras= Compra.objects.filter(id=pk)
    detallecompras = Detallecompra.objects.filter(grupo_id=pk)
    total_valores = detallecompras.aggregate(Sum('valortotal'))['valortotal__sum'] or Decimal(0.0)
 
    locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")
    total_valores_colombiano = locale.currency(total_valores, grouping=True, symbol=False)
    context={
        "titulo":titulo,
        "modulo":modulo,
        "compras":compras,      
        "compra": compra,
        "detallecompras": detallecompras,
        'total_valores': total_valores,
        'total_valores_colombiano': total_valores_colombiano,

    }
    return render(request,"compras/compras/listar_Compra.html", context)