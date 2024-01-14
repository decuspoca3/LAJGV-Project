from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re
from django.core.validators import RegexValidator

def letras_validator(value):
    if not re.match("^[A-Za-zÁÉÍÓÚáéíóú ]+$", value):
        raise ValidationError('Este campo solo debe contener letras.')
    
def numeros_validator(value):
    if not re.match("^[0-9]+$", value):
        raise ValidationError('Este campo solo debe contener números.')

def unique_documento_validator(value):
    if Proveedor.objects.filter(documento=value).exists():
           raise ValidationError('Este documento ya está registrado.') 

    
class Proveedor(models.Model):
    nombre = models.CharField(max_length=45, verbose_name=_("Nombres"), validators=[letras_validator])
    apellido = models.CharField(max_length=45, verbose_name=_("Apellidos"), validators=[letras_validator])

    class TipoDocumento(models.TextChoices):
        CEDULA = 'CC', _("Cédula de Ciudadania")
        NIT='NIT',_("NIT")
        CEDULA_EXTRANJERIA='CE',_("Cédula de Extranjería")

    tipo_documento = models.CharField(max_length=20, choices=TipoDocumento.choices, verbose_name="Tipo de Documento")
    documento = models.CharField(max_length=20, verbose_name="Documento",validators=[numeros_validator, unique_documento_validator])
    telefono_contacto = models.CharField(max_length=10, verbose_name="Teléfono de contacto",validators=[numeros_validator])

    class Estado(models.TextChoices):
        ACTIVO = '1', _("Activo")
        INACTIVO = '0', _("Inactivo")
    estado = models.CharField(max_length=1, choices=Estado.choices, default=Estado.ACTIVO, verbose_name="Estado")
    def __str__(self):
        return "%s %s %s" % (self.nombre, self.apellido , self.documento )

    class Meta:
        verbose_name_plural = "Usuarios"

