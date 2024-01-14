import os
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from cliente.models import Cliente
from cliente.forms import ClienteForm, ClienteUpdateForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


@login_required()
def cliente_crear(request):
    titulo = "Cliente"
    if request.method == 'POST':
        form =ClienteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Cliente creado exitosamente.')
                return redirect('ventas-crear')
            except IntegrityError as e:
                messages.error(request, 'Error al crear el Cliente: {}'.format(str(e)))

    else:
        form = ClienteForm()

    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "cliente/cliente/crear.html", context)


@login_required()
def cliente_listar(request):
    titulo="Cliente"
    clientes = Cliente.objects.all()
    context={
        "titulo":titulo,
        "clientes":clientes
    }
    return render(request,"cliente/cliente/listar.html", context)

@login_required()
def cliente_modificar(request,pk):
    titulo="Cliente"
    cliente = Cliente.objects.get(id=pk)

    if request.method=='POST':
        form= ClienteUpdateForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
        messages.success(request, 'Cliente modificado exitosamente.')

        return redirect('cliente')
    else:
        form= ClienteUpdateForm(instance=cliente)
    context={
        "titulo":titulo,
        "form":form
    }
    return render(request,"cliente/cliente/modificar.html", context)

@login_required()
def cliente_eliminar(request,pk):
    cliente = Cliente.objects.filter(id=pk)
    cliente.update(
        estado="0"
    )
    return redirect('cliente')

