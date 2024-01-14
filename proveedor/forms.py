from django.forms import ModelForm, widgets
from proveedor.models import Proveedor

class ProveedorForm(ModelForm):

    class Meta:
        model = Proveedor
        fields = "__all__"
        exclude = ["estado"]
        

class ProveedorUpdateForm(ModelForm):

    class Meta:
        model = Proveedor
        fields = "__all__"
        exclude = ["documento","estado"]


