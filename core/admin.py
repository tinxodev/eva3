# core/admin.py

from django.contrib import admin
from .models import Sala, Reserva
from datetime import timedelta
from django.utils import timezone # Importar timezone y timedelta

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    """
    Configuración para la gestión de Salas en la interfaz de administración.
    """
    # Muestra estos campos en la lista
    list_display = ('nombre', 'capacidad_maxima', 'disponible', 'habilitada')
    
    # Permite filtrar por estos campos
    list_filter = ('disponible', 'habilitada')
    
    # Permite buscar por nombre
    search_fields = ('nombre',)
    
    # Permite editar 'habilitada' directamente en la lista (muy útil)
    list_editable = ('habilitada',)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    """
    Configuración para la gestión de Reservas en la interfaz de administración.
    """
    list_display = ('sala_reservada', 'rut_persona', 'hora_inicio', 'hora_termino')
    list_filter = ('sala_reservada',)
    search_fields = ('rut_persona', 'sala_reservada__nombre')
    
    def save_model(self, request, obj, form, change):
        """
        Sobrescribe el método de guardado del admin para fijar las horas
        automáticamente al crear una reserva desde aquí.
        """
        # Verifica si es un objeto NUEVO (no una edición)
        if not obj.pk: 
            # Asigna la hora de inicio (aunque tiene default, para asegurar)
            obj.hora_inicio = timezone.now()
            # Asigna la hora de término (2 horas después)
            obj.hora_termino = obj.hora_inicio + timedelta(hours=2)
        
        # Llama al guardado original (esto llamará a models.py clean() y save())
        super().save_model(request, obj, form, change)
        
        # Actualiza la disponibilidad de la sala
        obj.sala_reservada.actualizar_disponibilidad()

    def get_readonly_fields(self, request, obj=None):
        """
        Hace que los campos de hora sean de solo lectura.
        """
        if obj: # Si el objeto ya existe (editando), no se puede cambiar
            return ('hora_inicio', 'hora_termino', 'sala_reservada', 'rut_persona')
        else: # Si es un objeto nuevo (creando), solo 'hora_inicio'
            return ('hora_inicio',)