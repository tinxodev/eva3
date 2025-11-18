
from django.urls import path
from . import views

urlpatterns = [
    # Lista de Salas: Página principal (Mapea a views.sala_list)
    path('', views.sala_list, name='sala_list'),
    # Detalle de Sala: Muestra la información específica de una sala
    # El 'pk' (Primary Key) es el identificador de la sala.
    path('sala/<int:pk>/', views.sala_detail, name='sala_detail'),
    # Creación de Reserva: Formulario para reservar una sala
    # El 'sala_pk' es el ID de la sala que se va a reservar.
    path('sala/<int:sala_pk>/reservar/', views.reserva_create, name='reserva_create'),
]