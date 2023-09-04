from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from apps.rendas_gastos.forms import GastosForm, RendasForm, OpcoesRendas, OpcoesGastos, MetodoPagamento
from apps.rendas_gastos.models import Rendas, Gastos
from apps.investimentos.views import investimentos_total_view
from apps.rendas_gastos.utils import check_authentication

def index(request):
    if not check_authentication(request):
        return redirect('login')
    else:
        context_investimentos = investimentos_total_view(request)
        context_renda_gasto = rendas_gastos_view_total(request)
        rendas_cadastradas = Rendas.objects.filter(created_by=request.user)
        categorias_renda = OpcoesRendas.choices
        grafico_renda = graph(categorias_renda, rendas_cadastradas)
        gastos_cadastrados = Gastos.objects.filter(created_by=request.user)
        categorias_gasto = OpcoesGastos.choices
        grafico_gasto = graph(categorias_gasto, gastos_cadastrados)
        context = {
            'context_renda_gasto': context_renda_gasto,
            'context_investimentos': context_investimentos,
            'grafico_renda': grafico_renda,
            'grafico_gasto': grafico_gasto
        }
        return render(request, 'index.html', context)

def rendas(request):
    if not check_authentication(request):
        return redirect('login')
    else:
        form = process_form(request, RendasForm, Rendas, 'Renda registrada com sucesso!')
    rendas_cadastradas = Rendas.objects.filter(created_by=request.user)
    context_total = rendas_gastos_view_total(request)
    today = datetime.today()
    rendas_cadastradas_mes = Rendas.objects.filter(created_by=request.user, data__year=today.year, data__month=today.month)
    categorias_renda = OpcoesRendas.choices
    grafico_mes = graph(categorias_renda, rendas_cadastradas_mes)
    grafico = graph(categorias_renda, rendas_cadastradas)
    total_rendas, rendas_cadastradas = filter_selections(request, rendas_cadastradas)
    rendas_cadastradas = rendas_cadastradas.order_by('-data')
    paginator = Paginator(rendas_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context_view = rendas_gastos_view(request)
    context = {
        'form': form,
        'rendas_cadastradas': rendas_cadastradas,
        'total_rendas': total_rendas,
        'opcoes_rendas': OpcoesRendas.choices,
        'grafico_mes': grafico_mes,
        'grafico': grafico,
        'opcoes_pagamentos': MetodoPagamento.choices,
        'page_obj': page_obj,
        'context_view': context_view,
        'context_total': context_total
    }
    return render(request, 'rendas_gastos/rendas.html', context)

def gastos(request):
    if not check_authentication(request):
        return redirect('login')
    else:
        form = process_form(request, GastosForm, Gastos, 'Gasto registrado com sucesso!')
    gastos_cadastrados = Gastos.objects.filter(created_by=request.user)
    context_total = rendas_gastos_view_total(request)
    today = datetime.today()
    gastos_cadastrados_mes = Gastos.objects.filter(created_by=request.user, data__year=today.year, data__month=today.month)
    categorias = OpcoesGastos.choices
    grafico_mes = graph(categorias, gastos_cadastrados_mes)
    grafico = graph(categorias, gastos_cadastrados)
    total_gastos, gastos_cadastrados = filter_selections(request, gastos_cadastrados)
    gastos_cadastrados = gastos_cadastrados.order_by('-data')
    paginator = Paginator(gastos_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context_view = rendas_gastos_view(request)
    context = {
        'form': form,
        'gastos_cadastrados': gastos_cadastrados,
        'total_gastos': total_gastos,
        'opcoes_gastos': OpcoesGastos.choices,
        'grafico_mes': grafico_mes,
        'grafico': grafico,
        'opcoes_pagamentos': MetodoPagamento.choices,
        'page_obj': page_obj,
        'context_view': context_view,
        'context_total': context_total
    }
    return render(request, 'rendas_gastos/gastos.html', context)

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
    context_view = {
        'renda_mes': renda_mes,
        'gasto_mes': gasto_mes,
        'saldo': saldo, 
    }
    return context_view

def rendas_gastos_view_total(request):
    rendas_usuario = Rendas.objects.filter(created_by=request.user)
    renda_total = sum(renda.valor for renda in rendas_usuario)
    gastos_usuario = Gastos.objects.filter(created_by=request.user)
    gasto_total = sum(gasto.valor for gasto in gastos_usuario)
    saldo_total = renda_total - gasto_total
    context_total = {
        'renda_total': renda_total,
        'gasto_total': gasto_total,
        'saldo_total': saldo_total, 
    }
    return context_total

def graph(categorias_ref, name_cadastrado):
    totais_dict = {categoria[1]: 0.0 for categoria in categorias_ref}
    for categoria in categorias_ref:
        total_categoria = name_cadastrado.filter(categoria=categoria[0]).aggregate(total=Sum('valor'))['total']
        total_categoria_formatted = round(float(total_categoria), 2) if total_categoria else 0.0
        totais_dict[categoria[1]] = total_categoria_formatted
    totais_dict_ordenado = {k: v for k, v in sorted(totais_dict.items(), key=lambda item: item[1], reverse=True)}
    return totais_dict_ordenado

def limpar_filtros(request, pagina):
    return HttpResponseRedirect(reverse(pagina))

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