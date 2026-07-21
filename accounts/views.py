from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PerfilForm, SignupForm, UserUpdateForm


def signup_view(request):
    """Registro de usuarios: username, email y password."""

    if request.user.is_authenticated:
        return redirect('blog:home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, '¡Cuenta creada con éxito! Bienvenido/a.')
            return redirect('blog:home')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


@login_required(login_url='accounts:login')
def profile_view(request):
    """Muestra los datos del usuario logueado. Vista basada en función con decorador."""

    return render(request, 'accounts/profile.html', {'perfil': request.user.perfil})


@login_required(login_url='accounts:login')
def profile_edit_view(request):
    """Edición de los datos de usuario y del perfil extendido."""

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(
            request.POST, request.FILES, instance=request.user.perfil
        )
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Tu perfil se actualizó correctamente.')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        perfil_form = PerfilForm(instance=request.user.perfil)

    return render(
        request,
        'accounts/profile_edit.html',
        {'user_form': user_form, 'perfil_form': perfil_form},
    )
