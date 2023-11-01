from apps.usuarios.views import login, cadastro, logout, config
from django.urls import path

urlpatterns = [
    path('cadastro', cadastro, name='cadastro'),
    path('logout', logout, name='logout'),
    path('config', config, name='config'),
    path('login', login, name='login'),
]