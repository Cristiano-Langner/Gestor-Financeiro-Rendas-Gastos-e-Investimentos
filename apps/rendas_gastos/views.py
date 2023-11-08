from apps.rendas_gastos.forms import GastosForm, RendasForm, OpcoesRendas, OpcoesGastos, MetodoPagamento
from django.shortcuts import render, redirect, get_object_or_404
from apps.investimentos.views import investimentos_total_view 
from apps.rendas_gastos.utils import check_authentication
from apps.rendas_gastos.models import Rendas, Gastos
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.contrib import messages
from django.db.models import Sum
from django.urls import reverse

#Index responsável pela página inicial.
def index(request):
    if not check_authentication(request):
        return redirect('login')
    else:
        context_investimentos = investimentos_total_view(request)
        context_renda_gasto = rendas_gastos_view_total(request)
        context = {
            'context_renda_gasto': context_renda_gasto,
            'context_investimentos': context_investimentos
        }
        return render(request, 'index.html', context)

#Rendas responsável pela página de rendas.
def rendas(request):
    if not check_authentication(request):
        return redirect('login')
    else:
        form = process_form(request, RendasForm, Rendas, 'Renda registrada com sucesso!')
    rendas_cadastradas = Rendas.objects.filter(created_by=request.user)
    context_total = rendas_gastos_view_total(request)
    today = datetime.today()
    rendas_cadastradas_mes = Rendas.objects.filter(created_by=request.user, data__year=today.year, data__month=today.month)
    start_date = today - timedelta(days=365)
    rendas_cadastradas_12meses = Rendas.objects.filter(created_by=request.user, data__range=(start_date, today))
    categorias_renda = OpcoesRendas.choices
    grafico_mes = graph(categorias_renda, rendas_cadastradas_mes)
    porcentagem_mes = porcentagem(grafico_mes)
    grafico = graph(categorias_renda, rendas_cadastradas)
    porcentagem_total = porcentagem(grafico)
    grafico_12meses = graph(categorias_renda, rendas_cadastradas_12meses)
    porcentagem_12meses = porcentagem(grafico_12meses)
    porcentagem_categorias = ordenador_porcentagem(porcentagem_total, porcentagem_12meses, porcentagem_mes)
    total_rendas, rendas_cadastradas = filter_selections(request, rendas_cadastradas)
    rendas_cadastradas = rendas_cadastradas.order_by('-data')
    paginator = Paginator(rendas_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context_view = rendas_gastos_view(request)
    tipo = "renda"
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
        'context_total': context_total,
        'porcentagem_categorias': porcentagem_categorias,
        'tipo': tipo
    }
    return render(request, 'rendas_gastos/rendas.html', context)

#Gastos responsável pela página de gastos.
def gastos(request):
    if not check_authentication(request):
        return redirect('login')
    else:
        form = process_form(request, GastosForm, Gastos, 'Gasto registrado com sucesso!')
    gastos_cadastrados = Gastos.objects.filter(created_by=request.user)
    context_total = rendas_gastos_view_total(request)
    today = datetime.today()
    gastos_cadastrados_mes = Gastos.objects.filter(created_by=request.user, data__year=today.year, data__month=today.month)
    start_date = today - timedelta(days=365)
    gastos_cadastrados_12meses = Gastos.objects.filter(created_by=request.user, data__range=(start_date, today))
    categorias = OpcoesGastos.choices
    grafico_mes = graph(categorias, gastos_cadastrados_mes)
    porcentagem_mes = porcentagem(grafico_mes)
    grafico = graph(categorias, gastos_cadastrados)
    porcentagem_total = porcentagem(grafico)
    grafico_12meses = graph(categorias, gastos_cadastrados_12meses)
    porcentagem_12meses = porcentagem(grafico_12meses)
    porcentagem_categorias = ordenador_porcentagem(porcentagem_total, porcentagem_12meses, porcentagem_mes)
    total_gastos, gastos_cadastrados = filter_selections(request, gastos_cadastrados)
    gastos_cadastrados = gastos_cadastrados.order_by('-data')
    paginator = Paginator(gastos_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context_view = rendas_gastos_view(request)
    tipo = "gasto"
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
        'context_total': context_total,
        'porcentagem_categorias': porcentagem_categorias,
        'tipo': tipo
    }
    return render(request, 'rendas_gastos/gastos.html', context)

#Função para verificar a válidade dos dados a serem cadastrados e efetuar o salvamento.
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

#Função para filtrar os dados de acordo com o solicitado na página.
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

#Função para calcular os valores de renda, gasto e saldo no mês corrente.
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

#Função para calcular os valores de renda, gasto e saldo de todo o período cadastrado.
def rendas_gastos_view_total(request):
    rendas_usuario = Rendas.objects.filter(created_by=request.user)
    renda_total = round(sum(float(renda.valor) for renda in rendas_usuario), 2)
    gastos_usuario = Gastos.objects.filter(created_by=request.user)
    gasto_total = round(sum(float(gasto.valor) for gasto in gastos_usuario), 2)
    saldo_total = round((renda_total - gasto_total), 2)
    context_total = {
        'Rendas': renda_total,
        'Gastos': gasto_total,
        'Saldo': saldo_total, 
    }
    return context_total

#Função para gerar os dados para os gráficos, que também são usadas nas porcentagens.
def graph(categorias_ref, name_cadastrado):
    totais_dict = {categoria[1]: 0.0 for categoria in categorias_ref}
    for categoria in categorias_ref:
        total_categoria = name_cadastrado.filter(categoria=categoria[0]).aggregate(total=Sum('valor'))['total']
        total_categoria_formatted = round(float(total_categoria), 2) if total_categoria else 0.0
        totais_dict[categoria[1]] = total_categoria_formatted
    totais_dict_ordenado = {k: v for k, v in sorted(totais_dict.items(), key=lambda item: item[1], reverse=True)}
    return totais_dict_ordenado

#Função para calcular as porcentagens sobre as categorias em relação ao total analisado.
def porcentagem(dicionario):
    total = sum(dicionario.values())
    categoria_porcentagem = {}
    for categoria, valor in dicionario.items():
        if total > 0:
            percentage = (valor / total) * 100
            percentage = round(percentage, 2)
        else:
            percentage = 0.00
        categoria_porcentagem[categoria] = percentage
    return categoria_porcentagem

#Função para apenas ordenar as categorias e facilitar a exibição na página.
def ordenador_porcentagem(porcentagem_total, porcentagem_12meses, porcentagem_mes):
    categorias_ordenadas = sorted(porcentagem_total, key=lambda x: porcentagem_total[x], reverse=True)
    porcentagem_categorias = []
    for categoria in categorias_ordenadas:
        categoria_dict = {
            'categoria': categoria,
            'porcentagem_total': porcentagem_total[categoria],
            'porcentagem_12meses': porcentagem_12meses.get(categoria, 0),
            'porcentagem_mes': porcentagem_mes.get(categoria, 0),
        }
        porcentagem_categorias.append(categoria_dict)
    return porcentagem_categorias

#Função para limpar o filtro.
def limpar_filtros(pagina):
    return HttpResponseRedirect(reverse(pagina))

#Função para deletar uma renda.
def delete_renda(request, renda_id):
    renda = get_object_or_404(Rendas, pk=renda_id)
    renda.delete()
    messages.success(request, 'Renda deletada com sucesso!')
    return redirect('rendas')

#Função para deletar um gasto.
def delete_gasto(request, gasto_id):
    gasto = get_object_or_404(Gastos, pk=gasto_id)
    gasto.delete()
    messages.success(request, 'Gasto deletado com sucesso!')
    return redirect('gastos')