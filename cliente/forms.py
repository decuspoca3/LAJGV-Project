from django.forms import ModelForm, widgets
from cliente.models import Cliente

class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        fields = "__all__"
        exclude = ["estado"]
        

class ClienteUpdateForm(ModelForm):

    class Meta:
        model = Cliente
        fields = "__all__"
        exclude = ["documento","estado"]


