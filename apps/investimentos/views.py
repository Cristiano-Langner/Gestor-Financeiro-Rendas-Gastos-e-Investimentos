from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.investimentos.models import Acoes, Fiis, Bdrs, Criptos

def investimentos(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    return render(request, 'investimentos/investimentos.html')