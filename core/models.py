
# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone

# Duración maxima de la reserva: 2 horas
MAX_RESERVATION_DURATION_HOURS = 2


# Modelo para la sala de estudio
class Sala(models.Model):
    """
    Modelo para la gestión de Salas de Estudio. [cite: 17]
    Permite al administrador agregar, editar y eliminar salas. [cite: 18]
    """
    nombre = models.CharField(max_length=100, unique=True) 
    capacidad_maxima = models.IntegerField() 
    disponible = models.BooleanField(default=True)
    habilitada = models.BooleanField(default=True) 

#aqui uso meta para definir el nombre en singular y plural del modelo
    class Meta:
        verbose_name = "Sala de Estudio"
        verbose_name_plural = "Salas de Estudio"

    def __str__(self):
        return self.nombre

#funcion para actualizar la disponibilidad de la sala
    def actualizar_disponibilidad(self):
        """
        Verifica si hay alguna reserva activa (que no ha expirado) para esta sala
        y actualiza su estado de disponibilidad. [cite: 14, 15]
        """
        # Una reserva activa es aquella cuya hora_termino es mayor al momento actual
        reservas_activas = Reserva.objects.filter(
            sala_reservada=self,
            hora_termino__gt=timezone.now()
        ).exists()

#Si hay reservas activas la sala no está disponible.
        self.disponible = not reservas_activas
        self.save()


#modelo para la reserva de sala de estudio
class Reserva(models.Model):
    sala_reservada = models.ForeignKey(Sala, on_delete=models.CASCADE)
    nombre_persona = models.CharField(max_length=100)
    apellido_persona = models.CharField(max_length=100)
    rut_persona = models.CharField(max_length=12)
    hora_inicio = models.DateTimeField(default=timezone.now)
    hora_termino = models.DateTimeField()

    class Meta:
        verbose_name = "Reserva de Sala"
        verbose_name_plural = "Reservas de Sala"
        # Garantiza que las reservas se ordenen por la hora de inicio
        ordering = ['hora_inicio'] 

    def clean(self):
     
 
        #Validar que la duración de la reserva no exceda el máximo de 2 horas. 
        duracion = self.hora_termino - self.hora_inicio
        max_duracion = timedelta(hours=MAX_RESERVATION_DURATION_HOURS)
        
        if duracion > max_duracion:
            raise ValidationError("La reserva no puede durar más de 2 horas (máximo 120 minutos).")
        
        #Validar que no haya solapamiento de reservas en la misma sala.
        # Busca otras reservas para esta sala donde el fin de la existente sea posterior 
        # a mi inicio Y el inicio de la existente sea anterior a mi fin.
        solapamientos = Reserva.objects.filter(
            sala_reservada=self.sala_reservada,
            hora_termino__gt=self.hora_inicio, 
            hora_inicio__lt=self.hora_termino  
        ).exclude(pk=self.pk) #Excluirse a sí mismo en caso de edición

        if solapamientos.exists():
            raise ValidationError("La sala ya está reservada en el período solicitado. Debe esperar hasta que venza el plazo anterior.")


    def save(self, *args, **kwargs):
        # Asignar horas si es un objeto nuevo
        if not self.id: 
            if not self.hora_inicio:
                self.hora_inicio = timezone.now()
            self.hora_termino = self.hora_inicio + timedelta(hours=MAX_RESERVATION_DURATION_HOURS)

        # Validar AHORA (las horas ya existen)
        self.full_clean()
        
        # Guardar en BD
        super().save(*args, **kwargs)
        
        # Actualizar sala
        self.sala_reservada.actualizar_disponibilidad()
        
    def __str__(self):
        return f"Reserva de {self.sala_reservada.nombre} para {self.nombre_persona} {self.apellido_persona}"