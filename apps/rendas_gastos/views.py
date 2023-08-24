from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from django.core.paginator import Paginator
from apps.rendas_gastos.forms import GastosForm, RendasForm, OpcoesRendas, OpcoesGastos, MetodoPagamento
from apps.rendas_gastos.models import Rendas, Gastos
from apps.rendas_gastos.utils import check_authentication

def index(request):
    if not check_authentication(request):
        return redirect('login')
    else:
        context_renda_gasto = rendas_gastos_view(request)
        return render(request, 'index.html', context_renda_gasto)

def rendas(request):
    if not check_authentication(request):
        return redirect('login')
    else:
        form = process_form(request, RendasForm, Rendas, 'Renda registrada com sucesso!')
    rendas_cadastradas = Rendas.objects.filter(created_by=request.user)
    total_rendas, rendas_cadastradas = filter_selections(request, rendas_cadastradas)
    rendas_cadastradas = rendas_cadastradas.order_by('-data')
    paginator = Paginator(rendas_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'rendas_gastos/rendas.html', {'form': form, 'rendas_cadastradas': rendas_cadastradas,
                    'total_rendas': total_rendas, 'opcoes_rendas': OpcoesRendas.choices, 
                    'opcoes_pagamentos': MetodoPagamento.choices, 'page_obj': page_obj})

def gastos(request):
    if not check_authentication(request):
        return redirect('login')
    else:
        form = process_form(request, GastosForm, Gastos, 'gastos', 'Gasto registrado com sucesso!')
    gastos_cadastrados = Gastos.objects.filter(created_by=request.user)
    total_gastos, gastos_cadastrados = filter_selections(request, gastos_cadastrados)
    gastos_cadastrados = gastos_cadastrados.order_by('-data')
    paginator = Paginator(gastos_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'rendas_gastos/gastos.html', {'form': form, 'gastos_cadastrados': gastos_cadastrados,
                    'total_gastos': total_gastos, 'opcoes_gastos': OpcoesGastos.choices,
                    'opcoes_pagamentos': MetodoPagamento.choices, 'page_obj': page_obj})

def process_form(request, form_class, created_class, success_message):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            novo = created_class.objects.create(**form.cleaned_data, created_by=request.user)
            novo.save(user=request.user)
            messages.success(request, success_message)
    else:
        form = form_class()
    return form

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
    
def rendas_gastos_view(request):
    today = datetime.today()
    rendas_do_mes = Rendas.objects.filter(created_by=request.user, data__year=today.year, data__month=today.month)
    renda_mes = sum(renda.valor for renda in rendas_do_mes)
    gastos_do_mes = Gastos.objects.filter(created_by=request.user, data__year=today.year, data__month=today.month)
    gasto_mes = sum(gasto.valor for gasto in gastos_do_mes)
    saldo = renda_mes - gasto_mes
    context = {
        'renda_mes': renda_mes,
        'gasto_total': gasto_mes,
        'saldo': saldo, 
    }
    return context

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