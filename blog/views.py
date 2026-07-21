from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView

from .forms import ArticuloForm
from .models import Articulo


class HomeView(TemplateView):
    """Vista de inicio del sitio."""

    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ultimos_articulos'] = Articulo.objects.all()[:3]
        return context


class AboutView(TemplateView):
    """Vista "Acerca de mí" con información del dueño de la página."""

    template_name = 'blog/about.html'


class ArticuloListView(ListView):
    """Listado de páginas del blog (route pages/), con buscador por título."""

    model = Articulo
    template_name = 'blog/articulo_list.html'
    context_object_name = 'articulos'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(titulo__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class ArticuloDetailView(DetailView):
    """Detalle de una página del blog."""

    model = Articulo
    template_name = 'blog/articulo_detail.html'
    context_object_name = 'articulo'


class ArticuloCreateView(LoginRequiredMixin, CreateView):
    """Creación de una nueva página. Requiere estar logueado (mixin)."""

    model = Articulo
    form_class = ArticuloForm
    template_name = 'blog/articulo_form.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, 'La página se creó correctamente.')
        return super().form_valid(form)


class ArticuloUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edición de una página existente. Solo el autor puede editarla."""

    model = Articulo
    form_class = ArticuloForm
    template_name = 'blog/articulo_form.html'
    login_url = 'accounts:login'

    def test_func(self):
        return self.get_object().autor == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'La página se actualizó correctamente.')
        return super().form_valid(form)


@login_required(login_url='accounts:login')
def articulo_delete(request, pk):
    """Borrado de una página. Vista basada en función con decorador @login_required."""

    articulo = get_object_or_404(Articulo, pk=pk)

    if articulo.autor != request.user:
        messages.error(request, 'No tenés permiso para borrar esta página.')
        return redirect('blog:articulo_detail', pk=pk)

    if request.method == 'POST':
        articulo.delete()
        messages.success(request, 'La página se borró correctamente.')
        return redirect('blog:articulo_list')

    return render(request, 'blog/articulo_confirm_delete.html', {'articulo': articulo})
