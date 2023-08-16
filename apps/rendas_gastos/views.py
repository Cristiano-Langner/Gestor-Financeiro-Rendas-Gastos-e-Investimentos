from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Count
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
    selected_payment = request.GET.get('selected_payment')
    rendas_cadastradas = Rendas.objects.filter(created_by=request.user)
    
    categorias_renda = OpcoesRendas.choices
    totais_renda = []
    for categoria in categorias_renda:
        total_categoria = rendas_cadastradas.filter(categoria_renda=categoria[0]).aggregate(total=Sum('valor'))['total']
        totais_renda.append({
        'categoria_renda': categoria[1],
        'total': total_categoria if total_categoria else 0
        })
    total_categoria = rendas_cadastradas.values('categoria_renda').annotate(contagem=Count('categoria_renda'))
    grafico_renda = [totais_renda, list(total_categoria)]
    
    if selected_month:
        selected_month_date = datetime.strptime(selected_month, '%Y-%m')
        rendas_cadastradas = rendas_cadastradas.filter(data__year=selected_month_date.year, data__month=selected_month_date.month, created_by=request.user)
        total_rendas = rendas_cadastradas.filter(data__year=selected_month_date.year, data__month=selected_month_date.month).aggregate(total=Sum('valor'))['total']
    else:
        total_rendas = rendas_cadastradas.aggregate(total=Sum('valor'))['total']
    if selected_category:
        rendas_cadastradas = rendas_cadastradas.filter(categoria_renda=selected_category)
    if selected_payment:
        rendas_cadastradas = rendas_cadastradas.filter(metodo_pagamento=selected_payment)
        
    rendas_cadastradas = rendas_cadastradas.order_by('-data')
    paginator = Paginator(rendas_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'rendas_gastos/rendas.html', {'form': form, 'rendas_cadastradas': rendas_cadastradas,
                    'total_rendas': total_rendas, 'opcoes_rendas': OpcoesRendas.choices, 'grafico_renda': grafico_renda,
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
    selected_payment = request.GET.get('selected_payment')
    gastos_cadastrados = Gastos.objects.filter(created_by=request.user)
    
    categorias_gasto = OpcoesGastos.choices
    totais_gasto = []
    for categoria in categorias_gasto:
        total_categoria_gasto = gastos_cadastrados.filter(categoria_gasto=categoria[0]).aggregate(total=Sum('valor'))['total']
        totais_gasto.append({
        'categoria_gasto': categoria[1],
        'total': total_categoria_gasto if total_categoria_gasto else 0
        })
    total_categoria_gasto = gastos_cadastrados.values('categoria_gasto').annotate(contagem=Count('categoria_gasto'))
    grafico_gasto = [totais_gasto, list(total_categoria_gasto)]
    
    
    if selected_month:
        selected_month_date = datetime.strptime(selected_month, '%Y-%m')
        gastos_cadastrados = gastos_cadastrados.filter(data__year=selected_month_date.year, data__month=selected_month_date.month, created_by=request.user)
        total_gastos = gastos_cadastrados.filter(data__year=selected_month_date.year, data__month=selected_month_date.month).aggregate(total=Sum('valor'))['total']
    else:
        total_gastos = gastos_cadastrados.aggregate(total=Sum('valor'))['total']
    if selected_category:
        gastos_cadastrados = gastos_cadastrados.filter(categoria_gasto=selected_category)
    if selected_payment:
        gastos_cadastrados = gastos_cadastrados.filter(metodo_pagamento=selected_payment)
        
    gastos_cadastrados = gastos_cadastrados.order_by('-data')
    paginator = Paginator(gastos_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'rendas_gastos/gastos.html', {'form': form, 'gastos_cadastrados': gastos_cadastrados,
                    'total_gastos': total_gastos, 'opcoes_gastos': OpcoesGastos.choices, 'grafico_gasto': grafico_gasto,
                    'opcoes_pagamentos': MetodoPagamento.choices, 'page_obj': page_obj})
    
def delete_renda(request, renda_id):
    renda = get_object_or_404(Rendas, pk=renda_id)
    renda.delete()
    messages.success(request, 'Renda deletada com sucesso!')
    return redirect('rendas')

def delete_gasto(request, gasto_id):
    gasto = get_object_or_404(Gastos, pk=gasto_id)
    gasto.delete()
    messages.success(request, 'Gasto deletado com sucesso!')
    return redirect('gastos')