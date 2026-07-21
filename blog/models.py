from django.conf import settings
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Articulo(models.Model):
    """Modelo principal del blog: una nota/artículo sobre gestión hídrica."""

    titulo = models.CharField(max_length=150)
    resumen = models.CharField(
        max_length=250,
        help_text='Bajada breve que se muestra en el listado.',
    )
    contenido = RichTextField()
    imagen = models.ImageField(upload_to='articulos/', blank=True, null=True)
    fecha_publicacion = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articulos',
    )

    class Meta:
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('blog:articulo_detail', kwargs={'pk': self.pk})
