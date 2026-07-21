from django.contrib import admin

from .models import Articulo


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion')
    list_filter = ('fecha_publicacion', 'autor')
    search_fields = ('titulo', 'resumen')
