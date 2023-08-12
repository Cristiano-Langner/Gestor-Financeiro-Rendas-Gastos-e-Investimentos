from django.shortcuts import render, redirect
from django.contrib import messages
from apps.rendas_gastos.forms import GastosForm, RendasForm
from apps.rendas_gastos.models import Rendas

def index(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    return render(request, 'index.html')

def rendas(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        if request.method == 'POST':
            form = GastosForm(request.POST)
            if form.is_valid():
                print("Form is valid")
                valor = form['valor_renda'].value()
                descricao = form['descricao_renda'].value()
                data = form['data_renda'].value()
                pagamento = form['metodo_pagamento_renda'].value()
                categoria = form['categoria_renda'].value()
                nova_renda = Rendas.objects.create(
                    usuario=request.user,
                    valor=valor,
                    descricao=descricao,
                    data=data,
                    metodo_pagamento=pagamento,
                    categoria=categoria
                )
                nova_renda.save()
                messages.success(request, 'Renda registrada com sucesso!')
                return redirect('rendas')
        else:
            form = RendasForm()
    return render(request, 'rendas_gastos/rendas.html', {'form': form})

def gastos(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    return render(request, 'rendas_gastos/gastos.html')