from django.core.files.uploadedfile import UploadedFile
from django.forms import ModelForm, widgets
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from usuarios.models import Usuario

class UsuarioCreationForm(UserCreationForm):
    
    TIPOS_USUARIO = [
        ('Administrador', 'Administrador'),  # Valor por defecto
        ('Empleado', 'Empleado'), 
        # ... Puedes añadir más opciones aquí
    ]
    nombre = forms.CharField(max_length=100, required=True,label="Nombres")
    apellido = forms.CharField(max_length=100, required=True,label="Apellidos")
    tipo_documento = forms.ChoiceField(choices= Usuario.TipoDocumento.choices, required=True,label="Tipo de documento")
    documento = forms.CharField(max_length=10, required=True)
    rh = forms.ChoiceField(choices= Usuario.RH.choices, required=True)
    telefono = forms.CharField(max_length=10, required=True)
    direccion =forms.CharField(max_length=100, required=True)
    TipoUsuario = forms.ChoiceField(choices=TIPOS_USUARIO, required=True,label="Tipo de usuario")

    class Meta:
        model = Usuario
        fields = ('TipoUsuario','nombre','apellido','tipo_documento','documento','rh','telefono','direccion', 'email', 'password1', 'password2' )
        exclude=["estado"]
        
        
    def clean(self):
        cleaned_data = super().clean()
        documento = cleaned_data.get('documento')
        telefono= cleaned_data.get('telefono')

        if documento and len(str(documento)) > 12:
            self.add_error('documento', "El documento no puede tener más de 12 dígitos")

        if telefono and len(str(telefono)) > 10:
            self.add_error('telefono_contacto', "El teléfono no puede tener más de 10 dígitos")
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(UsuarioCreationForm, self).__init__(*args, **kwargs)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password2')


    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Contraseña'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if not user.username:
            user.username = self.cleaned_data['documento']# Si el campo empleado_usuario no está presente, asigna el valor del campo documento
        user.is_superuser = 1
        if commit:
            user.save()
        return user




class UsuarioUpdateForm(ModelForm):
    
    class Meta:
        model = Usuario
        fields = ('nombre','apellido','telefono','direccion', 'email','estado' )
        exclude=["documento","rh"]
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance.estado == Usuario.Estado.ACTIVO:
                self.fields['estado'].widget = forms.HiddenInput()

               
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = self.cleaned_data['estado']  # Cambiar el estado del usuario activo/inactivo
        if commit:
            user.save()
        return user
    