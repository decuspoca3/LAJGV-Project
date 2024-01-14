import os
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from proveedor.models import Proveedor
from proveedor.forms import ProveedorForm, ProveedorUpdateForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


@login_required()
def proveedor_crear(request):
    titulo = "Proveedor"
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Proveedor creado exitosamente.')
                return redirect('compras-crear')
            except IntegrityError as e:
                messages.error(request, 'Error al crear el Proveedor: {}'.format(str(e)))

    else:
        form = ProveedorForm()

    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "proveedor/proveedor/crear.html", context)


@login_required()
def proveedor_listar(request):
    titulo="Proveedor"
    proveedors = Proveedor.objects.all()
    context={
        "titulo":titulo,
        "proveedors":proveedors
    }
    return render(request,"proveedor/proveedor/listar.html", context)

@login_required()
def proveedor_modificar(request,pk):
    titulo="Proveedor"
    proveedor = Proveedor.objects.get(id=pk)

    if request.method=='POST':
        form= ProveedorUpdateForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
        messages.success(request, 'Proveedor modificado exitosamente.')

        return redirect('proveedor')
    else:
        form= ProveedorUpdateForm(instance=proveedor)
    context={
        "titulo":titulo,
        "form":form
    }
    return render(request,"proveedor/proveedor/modificar.html", context)

@login_required()
def proveedor_eliminar(request,pk):
    proveedor = Proveedor.objects.filter(id=pk)
    proveedor.update(
        estado="0"
    )
    return redirect('proveedor')

