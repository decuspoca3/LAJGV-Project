
from django.shortcuts import render, redirect, get_object_or_404
from usuarios.models import Usuario
from usuarios.forms import UsuarioCreationForm,UsuarioUpdateForm
from django.contrib import messages
from django.urls import reverse, resolve
from django.urls import reverse
from . import urls
from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordResetForm 



@login_required()
def usuario_crear(request):
    titulo = "Usuario"

    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            try:
                # Crear una instancia del modelo Usuario pero no guardarlo aún
                nuevo_usuario = form.save(commit=False)

                # Establecer el valor del campo tipoUsuario del modelo Usuario
                nuevo_usuario.tipoUsuario = form.cleaned_data['TipoUsuario']

                # Guardar el nuevo usuario con el valor del campo tipoUsuario asignado
                nuevo_usuario.save()

                # Obtener el token para restablecimiento de contraseña
                user = nuevo_usuario
                token = default_token_generator.make_token(user)

                # Construir la URL de restablecimiento de contraseña
                protocol = 'http'  # Puedes cambiarlo a 'https' si tu sitio usa SSL
                domain = request.META['HTTP_HOST']
                reset_url = reverse('password_reset_confirm', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': token})

                # Construir el mensaje de correo
                email_content = f"Hola {user.username},\n\n"
                email_content += "Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace:\n\n"
                email_content += f"{protocol}://{domain}{reset_url}\n\n"
                email_content += "Si no solicitaste este restablecimiento de contraseña, ignora este correo.\n\n"
                email_content += "Gracias,\nEl equipo de TuNombreDeSitio"

                # Enviar el correo
                send_mail(
                    'Restablecimiento de contraseña',
                    email_content,
                    'noreply@example.com',
                    [user.email],
                    fail_silently=False,
                )

                messages.success(request, 'Usuario creado exitosamente. Se ha enviado un correo electrónico para restablecer la contraseña.')
                return redirect('usuarios')
            except IntegrityError as e:
                if 'UNIQUE constraint' in str(e):
                    messages.error(request, 'El nombre de usuario ya existe.')
                else:
                    messages.error(request, 'Error al crear el usuario: {}'.format(str(e)))
        else:
            messages.error(request, 'Error al crear el usuario')
    else:
        form = UsuarioCreationForm()

    context = {
        'titulo': titulo,
        'form': form,
    }

    return render(request, 'usuarios/usuarios/crear.html', context)

@login_required
def usuario_listar(request):
    titulo="Usuario"
    usuarios= Usuario.objects.all()
    context={
        "titulo":titulo,
        "usuarios":usuarios,
        "user": request.user
    }
    return render(request,"usuarios/usuarios/listar.html", context)

@login_required
def usuario_modificar(request,pk):
    titulo="Usuario"
    usuario= Usuario.objects.get(id=pk)
    
    if request.method== 'POST':
        form= UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'El formulario se ha enviado correctamente.')
            return redirect('usuarios')
    else:
        form= UsuarioUpdateForm(instance=usuario)
    context={
        "titulo":titulo,
        "form":form
        }
    return render(request,"usuarios/usuarios/modificar.html", context)

@login_required()
def usuario_eliminar(request, pk):
    usuario = Usuario.objects.get(id=pk)
    # Cambiar el estado del usuario a "0" (inactivo)
    usuario.estado = "0"
    usuario.is_active = usuario.estado != "0"
    usuario.save()
    return redirect('usuarios')
   

@login_required
def inactivos_listar(request):
    titulo="Usuario"
    inactivos= Usuario.objects.filter(estado="0")
    context={
        "titulo":titulo,
        "inactivos":inactivos,
        "user": request.user
    }
    return render(request,"usuarios/usuarios/inactivos.html", context)