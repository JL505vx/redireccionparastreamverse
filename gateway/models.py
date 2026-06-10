from django.db import models

from django.db import models

class SolicitudAcceso(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.nombre} - {self.estado}'
