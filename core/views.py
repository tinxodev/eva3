# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages 
from datetime import timedelta
from .models import Sala, Reserva
from .forms import ReservaForm 

def sala_list(request):
    """Muestra la página principal con todas las salas y su estado."""
    salas = Sala.objects.filter(habilitada=True)

    for sala in salas:
        sala.actualizar_disponibilidad()
        
    context = {
        'salas': salas,
    }
    # (Usa 'sala_list.html' si tus templates están directos en /templates/)
    return render(request, 'sala_list.html', context)

def sala_detail(request, pk):
    """Muestra el detalle de una sala específica."""
    sala = get_object_or_404(Sala, pk=pk)
    
    reserva_activa = Reserva.objects.filter(
        sala_reservada=sala,
        hora_termino__gt=timezone.now()
    ).first()

    context = {
        'sala': sala,
        'reserva_activa': reserva_activa,
    }
    # (Usa 'sala_detail.html' si tus templates están directos en /templates/)
    return render(request, 'sala_detail.html', context)

# ---
# --- LA FUNCIÓN CRÍTICA ES ESTA ---
# ---
# core/views.py

# --- Asegúrate de tener estas importaciones ---
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages 
from datetime import timedelta
from .models import Sala, Reserva
from .forms import ReservaForm 
# ---------------------------------------------

# ... (tus otras vistas, sala_list, sala_detail) ...

def reserva_create(request, sala_pk):
    """
    Maneja la creación de una nueva reserva (con nombre y apellido).
    """
    sala = get_object_or_404(Sala, pk=sala_pk)

    if not sala.disponible:
        messages.error(request, f"La sala {sala.nombre} ya está reservada.")
        return redirect('sala_list')

    if request.method == 'POST':
        form = ReservaForm(request.POST) 
        
        if form.is_valid():
            try:
                # 3. Obtenemos TODOS los datos validados
                rut_validado = form.cleaned_data['rut_persona']
                nombre_validado = form.cleaned_data['nombre_persona']
                apellido_validado = form.cleaned_data['apellido_persona']
                
                # 4. CREAMOS el objeto Reserva manualmente
                reserva = Reserva(
                    sala_reservada=sala,
                    rut_persona=rut_validado,
                    nombre_persona=nombre_validado,  # <--- AÑADIDO
                    apellido_persona=apellido_validado # <--- AÑADIDO
                )
                
                # 5. GUARDAMOS:
                reserva.save() 
                
                messages.success(request, f"Reserva de {sala.nombre} creada con éxito.")
                return redirect('sala_list') 
            
            except ValidationError as e:
                error_msg = list(e.message_dict.values())[0][0] if isinstance(e.message_dict, dict) else str(e)
                messages.error(request, f"Error en la reserva: {error_msg}")
        else:
            messages.error(request, "Error en los datos del formulario (revisa el RUT, nombre o apellido).")
    else:
        form = ReservaForm() # Formulario vacío

    context = {
        'form': form,
        'sala': sala
    }
    
    return render(request, 'reserva_form.html', context)