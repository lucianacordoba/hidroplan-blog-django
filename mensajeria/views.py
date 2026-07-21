from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MensajeForm
from .models import Mensaje

User = get_user_model()


@login_required(login_url='accounts:login')
def bandeja_view(request):
    """Bandeja de entrada: lista de contactos con los que hay mensajes."""

    mensajes = Mensaje.objects.filter(
        Q(emisor=request.user) | Q(receptor=request.user)
    )

    contactos = {}
    for mensaje in mensajes:
        otro = mensaje.receptor if mensaje.emisor == request.user else mensaje.emisor
        if otro.id not in contactos or mensaje.fecha_envio > contactos[otro.id]['fecha']:
            contactos[otro.id] = {'usuario': otro, 'ultimo': mensaje, 'fecha': mensaje.fecha_envio}

    lista_contactos = sorted(contactos.values(), key=lambda c: c['fecha'], reverse=True)

    otros_usuarios = User.objects.exclude(id=request.user.id).exclude(id__in=contactos.keys())

    return render(
        request,
        'mensajeria/bandeja.html',
        {'contactos': lista_contactos, 'otros_usuarios': otros_usuarios},
    )


@login_required(login_url='accounts:login')
def conversacion_view(request, user_id):
    """Conversación entre el usuario logueado y otro usuario."""

    otro_usuario = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = request.user
            mensaje.receptor = otro_usuario
            mensaje.save()
            return redirect('mensajeria:conversacion', user_id=otro_usuario.id)
    else:
        form = MensajeForm()

    mensajes = Mensaje.objects.filter(
        (Q(emisor=request.user) & Q(receptor=otro_usuario))
        | (Q(emisor=otro_usuario) & Q(receptor=request.user))
    )
    mensajes.filter(receptor=request.user, leido=False).update(leido=True)

    return render(
        request,
        'mensajeria/conversacion.html',
        {'otro_usuario': otro_usuario, 'mensajes': mensajes, 'form': form},
    )
