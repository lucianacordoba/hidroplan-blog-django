from django.conf import settings
from django.db import models


class Mensaje(models.Model):
    """Mensaje privado entre dos usuarios registrados."""

    emisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mensajes_enviados',
    )
    receptor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mensajes_recibidos',
    )
    contenido = models.TextField(max_length=1000)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        ordering = ['fecha_envio']

    def __str__(self):
        return f'{self.emisor} -> {self.receptor}: {self.contenido[:30]}'
