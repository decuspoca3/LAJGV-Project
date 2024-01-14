from django.core.files.uploadedfile import UploadedFile
from django.forms import ModelForm, widgets
from compra.models import Compra,Detallecompra
from usuarios.models import Usuario
from django import forms
from django.core.exceptions import ValidationError
from producto.models import Producto

class CompraForm(ModelForm):

    class Meta:
        model = Compra
        fields = "__all__"
        exclude=["estado","Empleado"]
    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)



class CompraUpdateForm(ModelForm):
    
    class Meta:
        model = Compra
        fields = "__all__"
        exclude=["fecha_creacion","estado"]
        
class DetallecompraForm(ModelForm):

    precio_str = forms.CharField(label="Precio Unitario", max_length=20)

    class Meta:
        model = Detallecompra
        fields = "__all__"
        exclude=["estado","grupo","valortotal","Precio"]
        
    def clean_precio_str(self):
        precio_str = self.cleaned_data['precio_str']

        try:
            precio_decimal = round(float(precio_str.replace(",", "").replace(".", "").replace(" ", "")), 2)
            if precio_decimal < 0:
                raise ValidationError("El precio debe ser mayor o igual a cero.")
            return precio_decimal
        except (ValueError, TypeError):
            raise ValidationError("Asegúrese de ingresar un valor numérico válido.")
        
    def __init__(self, *args, **kwargs):
        super(DetallecompraForm, self).__init__(*args, **kwargs)
        self.fields["producto"].queryset = Producto.objects.filter(estado=Producto.Estado.ACTIVO)
