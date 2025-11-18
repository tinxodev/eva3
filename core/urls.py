# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 1. Lista de Salas: Página principal (Mapea a views.sala_list)
    # Ruta: / 
    path('', views.sala_list, name='sala_list'),

    # 2. Detalle de Sala: Muestra la información específica de una sala
    # Ruta: /sala/1/, /sala/2/, etc.
    # El 'pk' (Primary Key) es el identificador de la sala.
    path('sala/<int:pk>/', views.sala_detail, name='sala_detail'),
    
    # 3. Creación de Reserva: Formulario para reservar una sala
    # Ruta: /sala/1/reservar/
    # El 'sala_pk' es el ID de la sala que se va a reservar.
    path('sala/<int:sala_pk>/reservar/', views.reserva_create, name='reserva_create'),
]