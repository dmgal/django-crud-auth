# Para crear un fomulario personalizado
#from django.forms import ModelForm

# Para crear un fomulario personalizado y usar widgets
from django import forms
# Modelos en los que se basará el formulario
from .models import Task

# Clase con la que extendemos el form básico de django y que daremos forma con nuestro modelo

# Formato sin Widgets
#class TaskForm(ModelForm):

# Formato con Widgets
class TaskForm(forms.ModelForm):
    class Meta:
        # Modelo que usaremos
        model = Task
        # Creamos una lista con los campos que queremos usar en el formulario
        fields = ['title', 'description', 'important']
        # Con este diccionario describimos propiedades sobre los campos expuestos en "fields"
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escribe un título.'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Escribe una descripción.'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check form-check-input'}),
        }
