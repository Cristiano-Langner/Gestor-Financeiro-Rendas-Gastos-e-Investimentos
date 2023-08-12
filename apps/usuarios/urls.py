from django.urls import path
from apps.usuarios.views import login, cadastro, logout, config

urlpatterns = [
    path('login', login, name='login'),
    path('cadastro', cadastro, name='cadastro'),
    path('logout', logout, name='logout'),
    path('config', config, name='config'),
] 