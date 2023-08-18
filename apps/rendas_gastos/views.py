from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from apps.rendas_gastos.forms import GastosForm, RendasForm, OpcoesRendas, OpcoesGastos, MetodoPagamento
from apps.rendas_gastos.models import Rendas, Gastos
from apps.rendas_gastos.utils import check_authentication

def index(request):
    if not check_authentication(request):
        return redirect('login')
    return render(request, 'index.html')

def process_form(request, form_class, created_class, reditect_name, success_message):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            novo = created_class.objects.create(**form.cleaned_data, created_by=request.user)
            novo.save(user=request.user)
            messages.success(request, success_message)
            return redirect(reditect_name)
    else:
        form = form_class()
    return form

def graph(categorias_ref, name_cadastrado_categoria):
    totais = []
    for categoria in categorias_ref:
        total_categoria = name_cadastrado_categoria.filter(categoria=categoria[0]).aggregate(total=Sum('valor'))['total']
        totais.append({
        'categoria': categoria[1],
        'total': total_categoria if total_categoria else 0
        })
    total_categoria = name_cadastrado_categoria.values('categoria').annotate(contagem=Count('categoria'))
    grafico = [totais, list(total_categoria)]
    return grafico

def filter_selections(request, name_cadastrado_categoria):
    selected_month = request.GET.get('selected_month')
    selected_category = request.GET.get('selected_category')
    selected_payment = request.GET.get('selected_payment')
    filters ={'created_by': request.user}
    
    if selected_month:
        selected_month_date = datetime.strptime(selected_month, '%Y-%m')
        filters['data__year'] = selected_month_date.year
        filters['data__month'] = selected_month_date.month
    if selected_category:
        filters['categoria'] = selected_category
    if selected_payment:
        filters['metodo_pagamento'] = selected_payment
        
    name_cadastrado_categoria = name_cadastrado_categoria.filter(**filters)
    total = name_cadastrado_categoria.aggregate(total=Sum('valor'))['total']
    return total, name_cadastrado_categoria

def rendas(request):
    if not check_authentication(request):
        return redirect('login')
    else:
        form = process_form(request, RendasForm, Rendas, 'rendas', 'Renda registrada com sucesso!')
    
    rendas_cadastradas = Rendas.objects.filter(created_by=request.user)
    categorias_renda = OpcoesRendas.choices
    
    grafico_renda = graph(categorias_renda, rendas_cadastradas)
    
    total_rendas, rendas_cadastradas = filter_selections(request, rendas_cadastradas)
        
    rendas_cadastradas = rendas_cadastradas.order_by('-data')
    paginator = Paginator(rendas_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'rendas_gastos/rendas.html', {'form': form, 'rendas_cadastradas': rendas_cadastradas,
                    'total_rendas': total_rendas, 'opcoes_rendas': OpcoesRendas.choices, 'grafico_renda': grafico_renda,
                    'opcoes_pagamentos': MetodoPagamento.choices, 'page_obj': page_obj})

def gastos(request):
    if not check_authentication(request):
        return redirect('login')
    else:
        form = process_form(request, GastosForm, Gastos, 'gastos', 'Gasto registrado com sucesso!')
    
    gastos_cadastrados = Gastos.objects.filter(created_by=request.user)
    categorias = OpcoesGastos.choices
    
    grafico_gasto = graph(categorias, gastos_cadastrados)
    
    total_gastos, gastos_cadastrados = filter_selections(request, gastos_cadastrados)
    
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