from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from apps.rendas_gastos.forms import GastosForm, RendasForm, OpcoesRendas, OpcoesGastos, MetodoPagamento
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
                valor = form['valor'].value()
                descricao = form['descricao'].value()
                data = form['data'].value()
                pagamento = form['metodo_pagamento'].value()
                categoria = form['categoria_renda'].value()
                nova_renda = Rendas.objects.create(
                    valor=valor,
                    descricao=descricao,
                    data=data,
                    metodo_pagamento=pagamento,
                    categoria_renda=categoria,
                )
                nova_renda.save(user=request.user)
                messages.success(request, 'Renda registrada com sucesso!')
                return redirect('rendas')
        else:
            form = RendasForm()
    selected_month = request.GET.get('selected_month')
    selected_category = request.GET.get('selected_category')
    selected_payment = request.GET.get('selected_category')
    if selected_month:
        selected_month_date = datetime.strptime(selected_month, '%Y-%m')
        rendas_cadastradas = Rendas.objects.filter(data__year=selected_month_date.year, data__month=selected_month_date.month)
        total_rendas = Rendas.objects.filter(data__year=selected_month_date.year, data__month=selected_month_date.month).aggregate(total=Sum('valor'))['total']
    else:
        rendas_cadastradas = Rendas.objects.all()
        total_rendas = Rendas.objects.aggregate(total=Sum('valor'))['total']
    if selected_category:
        categorias_cadastradas = Rendas.objects.filter(categoria_renda=selected_category)
    else:
        categorias_cadastradas = OpcoesRendas.values
    if selected_payment:
        pagamentos_cadastrados = Rendas.objects.filter(metodo_pagamento=selected_payment)
    else:
        pagamentos_cadastrados = MetodoPagamento.values
        
    paginator = Paginator(rendas_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'rendas_gastos/rendas.html', {'form': form, 'rendas_cadastradas': rendas_cadastradas,
                    'total_rendas': total_rendas, 'categorias_cadastradas': categorias_cadastradas,
                    'opcoes_rendas': OpcoesRendas.choices, 'pagamentos_cadastrados': pagamentos_cadastrados,
                    'opcoes_pagamentos': MetodoPagamento.choices, 'page_obj': page_obj})

def gastos(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        if request.method == 'POST':
            form = GastosForm(request.POST)
            if form.is_valid():
                valor = form['valor'].value()
                descricao = form['descricao'].value()
                data = form['data'].value()
                pagamento = form['metodo_pagamento'].value()
                categoria = form['categoria_gasto'].value()
                novo_gasto = Gastos.objects.create(
                    valor=valor,
                    descricao=descricao,
                    data=data,
                    metodo_pagamento=pagamento,
                    categoria_gasto=categoria,
                )
                novo_gasto.save(user=request.user)
                messages.success(request, 'Gasto registrado com sucesso!')
                return redirect('gastos')
        else:
            form = GastosForm()
    selected_month = request.GET.get('selected_month')
    selected_category = request.GET.get('selected_category')
    if selected_month:
        selected_month_date = datetime.strptime(selected_month, '%Y-%m')
        gastos_cadastrados = Gastos.objects.filter(data__year=selected_month_date.year, data__month=selected_month_date.month)
        total_gastos = Gastos.objects.filter(data__year=selected_month_date.year, data__month=selected_month_date.month).aggregate(total=Sum('valor'))['total']
    else:
        gastos_cadastrados = Gastos.objects.all()
        total_gastos = Gastos.objects.aggregate(total=Sum('valor'))['total']
    if selected_category:
        categorias_cadastradas = Gastos.objects.filter(categoria_gasto=selected_category)
    else:
        categorias_cadastradas = OpcoesGastos.values
        
    paginator = Paginator(gastos_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'rendas_gastos/gastos.html', {'form': form, 'gastos_cadastrados': gastos_cadastrados,
                    'total_gastos': total_gastos, 'categorias_cadastradas': categorias_cadastradas,
                    'opcoes_gastos': OpcoesGastos.choices, 'page_obj': page_obj})
    
def delete_renda(request, renda_id):
    renda = get_object_or_404(Rendas, pk=renda_id)
    renda.delete()
    messages.success(request, 'Renda deletada com sucesso!')
    return redirect('rendas')