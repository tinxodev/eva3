
from django.contrib import admin
from .models import Sala, Reserva
from datetime import timedelta
from django.utils import timezone 

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    
    #Configuración para la gestión de Salas en la interfaz de administración.
    
    list_display = ('nombre', 'capacidad_maxima', 'disponible', 'habilitada')
    list_filter = ('disponible', 'habilitada')
    search_fields = ('nombre',)
    list_editable = ('habilitada',)

# aqui la reserva la hago para que sea editable
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    

    def get_readonly_fields(self, request, obj=None):
        
        if obj: 
            
            return ('hora_inicio', 'sala_reservada', 'rut_persona')
        else: 
            return ('hora_inicio',)