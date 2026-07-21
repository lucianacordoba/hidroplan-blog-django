from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('pages/', views.ArticuloListView.as_view(), name='articulo_list'),
    path('pages/crear/', views.ArticuloCreateView.as_view(), name='articulo_create'),
    path('pages/<int:pk>/', views.ArticuloDetailView.as_view(), name='articulo_detail'),
    path('pages/<int:pk>/editar/', views.ArticuloUpdateView.as_view(), name='articulo_update'),
    path('pages/<int:pk>/borrar/', views.articulo_delete, name='articulo_delete'),
]
