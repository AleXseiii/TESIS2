from django.db import models
from doctors.models import Kinesiologist
from users.models import Patient
from django.core.exceptions import ValidationError

# Create your models here.
class Availability(models.Model):
    DAYS = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    kinesiologist = models.ForeignKey(Kinesiologist, on_delete=models.CASCADE, related_name="availability")
    day = models.IntegerField(choices=DAYS)
    start_time = models.TimeField()   
    end_time = models.TimeField()     

    def __str__(self):
        return f"{self.kinesiologist} - {self.get_day_display()} {self.start_time} - {self.end_time}"
    
class Appointment(models.Model):
    kinesiologist = models.ForeignKey(Kinesiologist, on_delete=models.CASCADE, related_name="appointments")
    patient_name = models.ForeignKey(Patient, related_name="appointments", on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.patient_name} - {self.date} {self.start_time}"
    
    def clean(self):
        # 1. Verificar que esté dentro del horario del kinesiólogo
        from datetime import datetime

        day_of_week = self.date.weekday()

        availability = Availability.objects.filter(
            kinesiologist=self.kinesiologist,
            day=day_of_week,
            start_time__lte=self.start_time,
            end_time__gte=self.end_time
        )

        if not availability.exists():
            raise ValidationError("la cita está fuera del horario disponible del kinesiólogo.")

        # 2. Verificar solapamiento con otras citas
        overlapping = Appointment.objects.filter(
            kinesiologist=self.kinesiologist,
            date=self.date,
            start_time__lt=self.end_time,   # empieza antes que termine otra
            end_time__gt=self.start_time    # termina después que empieza otra
        ).exclude(id=self.id)

        if overlapping.exists():
            raise ValidationError("Este horario ya está ocupado.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)