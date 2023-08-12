from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    return render(request, 'index.html')

def rendas(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    return render(request, 'rendas_gastos/rendas.html')

def gastos(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    return render(request, 'rendas_gastos/gastos.html')