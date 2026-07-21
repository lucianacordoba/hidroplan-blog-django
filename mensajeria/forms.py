from django import forms

from .models import Mensaje


class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(
                attrs={'rows': 2, 'placeholder': 'Escribí tu mensaje...'}
            ),
        }
