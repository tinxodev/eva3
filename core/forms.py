# core/forms.py
from django import forms
import re  # <--- 1. Importa la librería de Expresiones Regulares
from django.core.exceptions import ValidationError # <--- 2. Importa el error de validación

class ReservaForm(forms.Form):
    
    #Formulario simple que ahora pide Nombre, Apellido y RUT.
    nombre_persona = forms.CharField(max_length=100, label="Nombre")
    apellido_persona = forms.CharField(max_length=100, label="Apellido")
    rut_persona = forms.CharField(max_length=12, label="Rut de la Persona que Reserva")

    def clean_rut_persona(self):
        # este método de validación de RUT queda exactamente igual
        rut = self.cleaned_data.get('rut_persona')
        #aqui en el pattern se define el formato del rut
        pattern = r'^(\d{1,2}\.\d{3}\.\d{3}-[\dkK]|\d{7,8}-[\dkK])$'
        # Usa re.match para validar el formato
        if not re.match(pattern, rut):
            raise ValidationError(
                "El formato del RUT no es válido. Debe ser '12.345.678-9' o '12345678-9'."
            )
        return rut