from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.forms.fields import CharField
from django.forms.widgets import TextInput, Widget

class FormRegistro(UserCreationForm):
    
    class Meta:
        model = User
        #Campos a pedir usuario, first_name == telefono, 
        fields = ['username','email','first_name','password1','password2']
        labels = {'first_name':'Telefono'}

class FormSession(forms.Form):
    nombre = forms.CharField(
        label='Usuario',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Ingresa tu nombre de usuario',
                'name': 'usuario'
            }
        )    
    )
    clave = forms.CharField(
        label='Contraseña',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Ingresa tu contraseña',
                'name': 'clave'
            }
        )
    )