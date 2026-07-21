from django.conf import settings
from django.db import models


class Perfil(models.Model):
    """Datos extendidos de un usuario: avatar, biografía y demás."""

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',
    )
    avatar = models.ImageField(upload_to='avatares/', blank=True, null=True)
    biografia = models.TextField(max_length=500, blank=True)
    link = models.URLField(blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'
