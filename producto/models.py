
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re



def letras_validator(value):
    if not re.match("^[A-Za-zÁÉÍÓÚáéíóú ]+$", value):
        raise ValidationError('Este campo solo debe contener letras.')

class Producto(models.Model):
    class Categoria(models.TextChoices):
        ACCESORIOS='ACCESORIOS',("Accesorios")
        RESPUESTOS='RESPUESTOS',("Repuestos")
        CONSUMIBLES='CONSUMIBLES',("Consumibles")
    categoria=models.CharField(max_length=11,choices=Categoria.choices,verbose_name="Categoria")
    nombre = models.CharField(max_length=45, verbose_name=_("Nombre"), validators=[letras_validator])
    descripcion = models.CharField(max_length=60, verbose_name=_("Descripcion"), validators=[letras_validator])
    precio = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Precio"))
    stock = models.PositiveIntegerField(verbose_name=_("Stock"))
    
    class Estado(models.TextChoices):
        ACTIVO = '1', _("Activo")
        INACTIVO = '0', _("Inactivo")
        CONDICIONADO = '2', _("Condicionado")

    estado = models.CharField(max_length=2, choices=Estado.choices, default=Estado.ACTIVO, verbose_name=_("Estado"))

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}" 
    class Meta:
        # Establece la restricción de que la combinación de nombre y descripción debe ser única
        unique_together = ('nombre', 'descripcion')
    def precio_colombiano(self):
        formatted_price = "{:,.2f}".format(self.precio).replace(',', '#').replace('.', ',').replace('#', '.')
        return f"${formatted_price}"

  
