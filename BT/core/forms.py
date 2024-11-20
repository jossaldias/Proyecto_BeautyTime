import re
from .models import User, Producto, Order, Item, Reserva, Servicio, Categoria
from django.conf import settings
from django import forms  
from django.forms import TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Fieldset, Layout, Submit, ButtonHolder, HTML
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from core.constants import REGIONES, COMUNAS

User = get_user_model()

# Validador personalizado para el número de teléfono
def validar_telefono(value):
    if not re.match(r'^9\d{8}$', value):
        raise ValidationError("El número de teléfono debe comenzar con 9 y tener 9 dígitos.")
class CustomUserCreationForm(UserCreationForm):
    region = forms.ChoiceField(choices=REGIONES)
    comuna = forms.ChoiceField(choices=COMUNAS)
    telefono = forms.CharField(
        max_length=9,
        validators=[validar_telefono],
        widget=forms.TextInput(attrs={'type': 'tel'}),
        label="Teléfono"
    )
    direccion = forms.CharField(max_length=60 )    

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','region','comuna','direccion','telefono','password1','password2']

class editarUsuarioForm(forms.ModelForm):
    region = forms.ChoiceField(choices=REGIONES)
    comuna = forms.ChoiceField(choices=COMUNAS)
    tipo_user = forms.ChoiceField(choices=[('Cliente', 'Cliente'), ('Administrador', 'Administrador')])
    fecha_nac = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    password = forms.CharField(required=False, widget=forms.PasswordInput, label="Cambiar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'picture', 'email', 'region', 'comuna', 'direccion', 'telefono', 'fecha_nac', 'tipo_user', 'password']
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Primer Nombre',
            'last_name': 'Apellido',
            'picture': 'Avatar',
            'email': 'E-mail',
            'region': 'Región',
            'comuna': 'Comuna',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'fecha_nac': 'Fecha de Nacimiento',
            'tipo_user': 'Tipo de Usuario',
            'password': 'Cambiar Contraseña',
        }

        widgets = {
            'fecha_nac': forms.DateInput(format='%Y/%m/%d', attrs={'type': 'date'}),
        }


        def clean_password(self):
            password = self.cleaned_data.get('password')
            if password:
                return password  # Retornar la nueva contraseña si se ingresó
            return None  # No cambiar la contraseña si el campo está vacío

        # Método para cambiar la contraseña solo si se proporcionó una nueva
        def save(self, commit=True):
            # Guardamos el usuario sin la contraseña
            user = super(editarUsuarioForm, self).save(commit=False)

            # Si hay una nueva contraseña y no está vacía
            password = self.cleaned_data.get('password')
            if password and password.strip():  # Validamos que la contraseña no esté vacía ni sea None
                user.set_password(password)  # Establecemos la nueva contraseña
            else:
                # Aquí no cambiamos la contraseña existente
                user.password = User.objects.get(pk=user.pk).password  # Recuperamos la contraseña actual de la base de datos

            if commit:
                user.save()
            return user

class editarPerfilForm(forms.ModelForm):
        region = forms.ChoiceField(choices=REGIONES, widget=forms.Select())
        comuna = forms.ChoiceField(choices=COMUNAS, widget=forms.Select())
        telefono = forms.CharField(max_length=9, widget=forms.TextInput(attrs={'type': 'tel'}), validators=[validar_telefono], required=True)
        fecha_nac = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
        password = forms.CharField(required=False, widget=forms.PasswordInput, label="Cambiar Contraseña")


        class Meta:
            model = User
            fields = ['username', 'first_name', 'last_name', 'picture', 'email', 'region', 'comuna', 'direccion', 'telefono', 'fecha_nac', 'password']
            labels = {
                'username': 'Nombre de Usuario',
                'first_name': 'Primer Nombre',
                'last_name': 'Apellido',
                'picture': 'Avatar',
                'email': 'E-mail',
                'region': 'Región',
                'comuna': 'Comuna',
                'direccion': 'Dirección',
                'telefono': 'Teléfono',
                'fecha_nac': 'Fecha de Nacimiento',
                'password': 'Cambiar Contraseña',
            }
            widgets = {
                'username': forms.TextInput(attrs={'type': 'text', 'id': 'username_editar'}),
                'first_name': forms.TextInput(attrs={'id': 'nombre_editar'}),
                'last_name': forms.TextInput(attrs={'id': 'apellido_editar'}),
                'email': forms.TextInput(attrs={'id': 'email_editar'}),
                'direccion': forms.TextInput(attrs={'id': 'direccion_editar'}),
                'region': forms.TextInput(attrs={'id': 'region_editar'}),
                'comuna': forms.TextInput(attrs={'id': 'comuna_editar'}),
                'telefono': forms.TextInput(attrs={'id': 'telefono_editar'}),
                'fecha_nac': forms.DateInput(format=('%Y/%m/%d'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
            }
        # Método para validar el campo de contraseña
        def clean_password(self):
            password = self.cleaned_data.get('password')
            if password:
                return password  # Retornar la nueva contraseña si se ingresó
            return None  # No cambiar la contraseña si el campo está vacío

        # Método para cambiar la contraseña solo si se proporcionó una nueva
        def save(self, commit=True):
            # Guardamos el usuario sin la contraseña
            user = super(editarPerfilForm, self).save(commit=False)

            # Si hay una nueva contraseña y no está vacía
            password = self.cleaned_data.get('password')
            if password and password.strip():  # Validamos que la contraseña no esté vacía ni sea None
                user.set_password(password)  # Establecemos la nueva contraseña
            else:
                # Aquí no cambiamos la contraseña existente
                user.password = User.objects.get(pk=user.pk).password  # Recuperamos la contraseña actual de la base de datos

            if commit:
                user.save()
            return user


class agregarProductoForm(forms.ModelForm):
     # Cargar dinámicamente categorías desde la base de datos
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Categoría',
        required=True
    )

    TIPO = [
        ('producto', 'Producto'),
        ('servicio', 'Servicio'),
    ]

    nombre = forms.CharField(max_length=45, label='Nombre')
    tipo = forms.ChoiceField(choices=TIPO, label='Tipo')
    costo = forms.IntegerField(initial=0, required=True, label='Costo')
    picture = forms.ImageField(required=False, label='Imagen')
    cantidad = forms.IntegerField(initial=0, required=True, label='Cantidad')

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if Producto.objects.filter(nombre=nombre).exists():
            raise ValidationError('El producto o servicio ya existe, revisa el inventario e intenta otra vez.')
        return nombre

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'tipo', 'costo', 'picture', 'cantidad']
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'tipo': 'Tipo',
            'costo': 'Costo',
            'picture': 'Imagen',
            'cantidad':'Cantidad'
        }


class editarProductoForm(forms.ModelForm):
    costo = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'number'}),required=True, label='Costo')
    descuento = forms.DecimalField(widget=forms.NumberInput(attrs={'type': 'number'}), max_digits=4, decimal_places=2, required=True, label='Descuento')

    class Meta:
        model = Producto
        fields = ['costo', 'descuento'] 
        labels = {
            'costo': 'Costo',
            'descuento': 'Descuento',
        }
        widgets = {
            'costo': forms.NumberInput(attrs={'id': 'costo_editar'}),
            'descuento': forms.NumberInput(attrs={'id': 'descuento_editar'}),
        }

# FORMULARIO PARA AGENDAR CITAS
class ReservaCitaForm(forms.ModelForm):
    # Mantener todos los campos necesarios
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    hora = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    
    # Usar ModelChoiceField para cargar dinámicamente los servicios desde la base de datos
    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.all(),  # Cargar servicios desde la base de datos
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Nuevo campo para número de contacto
    contacto = forms.CharField(
        label="Número de contacto",
        max_length=9,
        required=True,
        help_text="Ingresa tu número de contacto sin el prefijo (+56)",
        widget=forms.TextInput(attrs={'placeholder': '9XXXXXXXX', 'class': 'form-control'})
    )

    class Meta:
        model = Reserva
        fields = ['nombre', 'email', 'servicio', 'fecha', 'hora', 'contacto']

    def clean_contacto(self):
        contacto = self.cleaned_data['contacto']
        # Validar que el número siga el formato chileno sin el prefijo +56
        if not re.match(r'^\d{9}$', contacto):
            raise forms.ValidationError("El número debe tener 9 dígitos.")
        return f'+56 {contacto}'


class CartAddProductoForm(forms.Form):
  cantidad = forms.IntegerField(
    label="Cantidad",
  )
  override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class OrderCreateForm(forms.ModelForm):
    region = forms.ChoiceField(choices=REGIONES)
    comuna = forms.ChoiceField(choices=COMUNAS)
    class Meta:
        model = Order
        fields = [
        
        "email",
        "direccion",
        "telefono",
        "observaciones",
        "region",
        "comuna",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "."
        self.helper.layout = Layout(
        Fieldset(
            Div(
            Field("nombre", css_class="form-control", wrapper_class="col"),
            css_class="row",
            ),
            Div(
            Field("email", css_class="form-control", wrapper_class="col"),
            css_class="row",
            ),
            Div(
            Field("region", css_class="form-control", wrapper_class="col"),
            css_class="row",
            ),
            Div(
            Field("comuna", css_class="form-control", wrapper_class="col"),
            css_class="row",
            ),
            Div(
            Field("direccion", css_class="form-control", wrapper_class="col"),
            css_class="row",
            ),
            Div(
            Field("telefono", css_class="form-control", wrapper_class="col"),
            css_class="row",
            ),
            Div(
            Field("observaciones", css_class="form-control", wrapper_class="col"),
            css_class="row",
            ),
            css_class="border-bottom mb-3",
        ),
        ButtonHolder(
                Submit(
                    "submit",
                    "Siguiente",
                    css_class="btn btn-success btn-lg btn-block"
                ),
                HTML('<a href="/clear/" class="btn btn-danger btn-lg btn-block">Cancelar compra</a>'),
                css_class="button-holder")
        )

        PRODUCTO_CANTIDAD_CHOICES = [
        (i, str(i)) for i in range(1, settings.PROVIDER_ITEM_MAX_CANTIDAD + 1)
        ]
