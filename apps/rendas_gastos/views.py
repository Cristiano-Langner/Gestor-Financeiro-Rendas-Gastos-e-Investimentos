from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from apps.rendas_gastos.forms import GastosForm, RendasForm
from apps.rendas_gastos.models import Rendas, Gastos

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
            form = RendasForm(request.POST)
            if form.is_valid():
                valor = form['valor_renda'].value()
                descricao = form['descricao_renda'].value()
                data = form['data_renda'].value()
                pagamento = form['metodo_pagamento_renda'].value()
                categoria = form['categoria_renda'].value()
                nova_renda = Rendas.objects.create(
                    valor=valor,
                    descricao=descricao,
                    data=data,
                    metodo_pagamento=pagamento,
                    categoria=categoria,
                )
                nova_renda.save(user=request.user)
                messages.success(request, 'Renda registrada com sucesso!')
                return redirect('rendas')
        else:
            form = RendasForm()
    selected_month = request.GET.get('selected_month')
    if selected_month:
        selected_month_date = datetime.strptime(selected_month, '%Y-%m')
        rendas_cadastradas = Rendas.objects.filter(data__year=selected_month_date.year, data__month=selected_month_date.month)
        total_rendas = Rendas.objects.filter(data__year=selected_month_date.year, data__month=selected_month_date.month).aggregate(total=Sum('valor'))['total']
    else:
        rendas_cadastradas = Rendas.objects.all()
        total_rendas = Rendas.objects.aggregate(total=Sum('valor'))['total']
    return render(request, 'rendas_gastos/rendas.html', {'form': form, 'rendas_cadastradas': rendas_cadastradas, 'total_rendas': total_rendas})

def gastos(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        if request.method == 'POST':
            form = GastosForm(request.POST)
            if form.is_valid():
                valor = form['valor_renda'].value()
                descricao = form['descricao_renda'].value()
                data = form['data_renda'].value()
                pagamento = form['metodo_pagamento_renda'].value()
                categoria = form['categoria_renda'].value()
                novo_gasto = Gastos.objects.create(
                    valor=valor,
                    descricao=descricao,
                    data=data,
                    metodo_pagamento=pagamento,
                    categoria=categoria,
                )
                novo_gasto.save(user=request.user)
                messages.success(request, 'Gasto registrado com sucesso!')
                return redirect('gastos')
        else:
            form = GastosForm()
    return render(request, 'rendas_gastos/gastos.html', {'form': form})