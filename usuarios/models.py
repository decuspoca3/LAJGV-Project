from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
import re
def letras_validator(value):
    if not re.match("^[A-Za-zÁÉÍÓÚáéíóú ]+$", value):
        raise ValidationError('Este campo solo debe contener letras.')
    
def numeros_validator(value):
    if not re.match("^[0-9]+$", value):
        raise ValidationError('Este campo solo debe contener números.')
def unique_documento_validator(value):
    if Usuario.objects.filter(documento=value).exists():
           raise ValidationError('Este documento ya está registrado.')   

class Usuario(AbstractUser):
    groups = models.ManyToManyField(Group, blank=True, related_name="usuarios")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='usuarios')
    nombre = models.CharField(max_length=45,verbose_name="Nombres", validators=[letras_validator])
    apellido = models.CharField(max_length=45,verbose_name="Apellidos", validators=[letras_validator]) 
    class TipoDocumento(models.TextChoices):
        CEDULA = 'CC', _("Cédula de Ciudadania")
        NIT='NIT',_("NIT")
        CEDULA_EXTRANJERIA='CE',_("Cédula de Extranjería")
    tipo_documento =models.CharField(max_length=20,choices=TipoDocumento.choices,verbose_name="Tipo de Documento")
    documento = models.CharField(max_length=10,verbose_name="Documento",validators=[numeros_validator, unique_documento_validator])
    class RH(models.TextChoices):
        OP='OP',_("O+")
        ON='ON',_("O-")
        AP='AP',_("A+")
        AN='AN',_("A-")
        BP='BP',_("B+")
        BN='BN',_("B-")
        ABP='ABP',_("AB+")
        ABN='ABN',_("AB-")
        
    rh= models.CharField(max_length=3,choices=RH.choices,verbose_name="Factor RH")
    class TipoUsuario(models.TextChoices):
        ADMINISTRADOR='A',_("Administrador")
        EMPLEADO = 'E', _("Empleado")
    tipoUsuario=models.CharField(max_length=2,choices=TipoUsuario.choices,verbose_name="tipoUsuario", default="Administrador")
    
    telefono=models.CharField(max_length=10,verbose_name="Teléfono",validators=[numeros_validator])
    direccion=models.CharField(max_length=45,verbose_name="Dirección", default="cra3 #4-5")
    class Estado(models.TextChoices):
        ACTIVO='1',_("Activo")
        INACTIVO='0',_("Inactivo")
    estado=models.CharField(max_length=1,choices=Estado.choices,default=Estado.ACTIVO,verbose_name="Estado")
   

                
    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.username}"
    
    class Meta:
        verbose_name_plural = "Usuarios"


