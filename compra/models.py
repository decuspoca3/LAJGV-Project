from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from decimal import Decimal
import locale
from django.db.models import Sum
from proveedor.models import Proveedor
from usuarios.models import Usuario
from django.core.exceptions import ValidationError

def validate_positive(value):
        if value < 1:
            raise ValidationError("La cantidad debe ser un número positivo.")

class Compra(models.Model):
    nombre= models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False)
    Proveedor= models.ForeignKey(Proveedor,verbose_name="Proveedor",related_name="Proveedor", on_delete=models.CASCADE)
    Empleado= models.ForeignKey(Usuario,verbose_name="Empleado", on_delete=models.CASCADE)

    class Estado(models.TextChoices):
        ACTIVO='1',_("Activo")
        INACTIVO='0',_("Inactivo")
    estado=models.CharField(max_length=1,choices=Estado.choices,default=Estado.ACTIVO,verbose_name="Estado")
    fecha_creacion = models.DateField(auto_now=True, verbose_name="Fecha de Creación")
    def __str__(self):
        return f"{self.Proveedor}"



class Detallecompra(models.Model):

    cantidad=models.IntegerField( verbose_name="cantidad", validators=[validate_positive])
    grupo=models.ForeignKey(Compra,verbose_name="Grupo", on_delete=models.CASCADE)
    producto = models.ForeignKey("producto.Producto", on_delete=models.CASCADE, verbose_name="Producto")
    Precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    valortotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="valor total", null=True, blank=True)

    
    class Estado(models.TextChoices):
        ACTIVO='1',_("Activo")
        INACTIVO='0',_("Inactivo")
    estado=models.CharField(max_length=1,choices=Estado.choices,default=Estado.ACTIVO,verbose_name="Estado")
    

    def precio_colombiano(self):
        formatted_price = "{:,.2f}".format(self.Precio).replace(',', '#').replace('.', ',').replace('#', '.')
        return f"${formatted_price}"  
    
    def save(self, *args, **kwargs):
    # Asegurarse de que self.cantidad sea un Decimal
        cantidad_decimal = Decimal(self.cantidad) if self.cantidad else Decimal('0')
    
    # Asegurarse de que self.Precio sea un Decimal
        precio_decimal = self.Precio if isinstance(self.Precio, Decimal) else Decimal(str(self.Precio))
    
    # Calcula el valor total multiplicando la cantidad por el precio del producto
        self.valortotal = cantidad_decimal * precio_decimal
        super().save(*args, **kwargs)
    
    def calcular_total_valores():
       total = Integrantes.objects.aggregate(Sum('valortotal'))['valortotal__sum']
       return total or Decimal(0.0)

    @property
    def valortotal_colombiano(self):
        locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")
        formatted_valortotal = locale.currency(self.valortotal, grouping=True, symbol=False)
        return formatted_valortotal 
