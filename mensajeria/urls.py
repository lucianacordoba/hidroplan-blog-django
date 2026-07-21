from django.urls import path

from . import views

app_name = 'mensajeria'

urlpatterns = [
    path('', views.bandeja_view, name='bandeja'),
    path('<int:user_id>/', views.conversacion_view, name='conversacion'),
]
