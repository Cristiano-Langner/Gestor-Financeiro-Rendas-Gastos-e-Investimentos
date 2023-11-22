from apps.rendas_gastos.forms import GastosForm, RendasForm, OpcoesRendas, OpcoesGastos, MetodoPagamento 
from django.shortcuts import render, redirect, get_object_or_404
from apps.investimentos.views import investimentos_total_view
from django.contrib.auth.decorators import login_required
from apps.rendas_gastos.models import Rendas, Gastos
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.contrib import messages
from django.db.models import Sum
from django.urls import reverse

#Index responsável pela página inicial.
@login_required(login_url='login')
def index(request):
    context_investimentos = investimentos_total_view(request)
    context_renda_gasto = rendas_gastos_view_total(request)
    context = {
        'context_renda_gasto': context_renda_gasto,
        'context_investimentos': context_investimentos
    }
    return render(request, 'index.html', context)

#Responsável pela página de rendas.
@login_required(login_url='login')
def rendas(request):
    context = rendas_gastos(request, RendasForm, Rendas, 'Renda registrada com sucesso!', OpcoesRendas, "renda")
    return render(request, 'rendas_gastos/rendas.html', context)

#Responsável pela página de gastos.
@login_required(login_url='login')
def gastos(request):
    context = rendas_gastos(request, GastosForm, Gastos, 'Gasto registrado com sucesso!', OpcoesGastos, "gasto")
    return render(request, 'rendas_gastos/gastos.html', context)

#Executa as funções para rendas e gastos.
def rendas_gastos(request, form_process, class_process, message, opcoes_process, tipo):
    form = process_form(request, form_process, class_process, message)
    dados_cadastrados = class_process.objects.filter(created_by=request.user)
    context_total = rendas_gastos_view_total(request)
    today = datetime.today()
    dados_cadastrados_mes = class_process.objects.filter(created_by=request.user, data__year=today.year, data__month=today.month)
    start_date = today - timedelta(days=365)
    dados_cadastrados_12meses = class_process.objects.filter(created_by=request.user, data__range=(start_date, today))
    categorias = opcoes_process.choices
    formas_pagamento = MetodoPagamento.choices
    grafico_mes = graph(categorias, dados_cadastrados_mes)
    porcentagem_mes = porcentagem(grafico_mes)
    grafico = graph(categorias, dados_cadastrados)
    porcentagem_total = porcentagem(grafico)
    grafico_12meses = graph(categorias, dados_cadastrados_12meses)
    porcentagem_12meses = porcentagem(grafico_12meses)
    porcentagem_categorias = ordenador_porcentagem(porcentagem_total, porcentagem_12meses, porcentagem_mes)
    pagamentos_mes = pagamentos(formas_pagamento, dados_cadastrados_mes)
    procentagem_mes_pagamentos = porcentagem(pagamentos_mes)
    pagamentos_12meses = pagamentos(formas_pagamento, dados_cadastrados_12meses)
    porcentagem_12meses_pagamentos = porcentagem(pagamentos_12meses)
    pagamentos_total = pagamentos(formas_pagamento, dados_cadastrados)
    procentagem_total_pagamentos = porcentagem(pagamentos_total)
    porcentagem_categorias_pagamento = ordenador_porcentagem(procentagem_total_pagamentos, porcentagem_12meses_pagamentos, procentagem_mes_pagamentos)
    total, dados_cadastrados = filter_selections(request, dados_cadastrados)
    dados_cadastrados = dados_cadastrados.order_by('-data')
    paginator = Paginator(dados_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context_view = rendas_gastos_view(request)
    context = {
        'form': form,
        'total': total,
        'grafico_mes': grafico_mes,
        'grafico': grafico,
        'opcoes_pagamentos': MetodoPagamento.choices,
        'opcoes': categorias,
        'page_obj': page_obj,
        'context_view': context_view,
        'context_total': context_total,
        'porcentagem_categorias': porcentagem_categorias,
        'porcentagem_categorias_pagamento': porcentagem_categorias_pagamento,
        'tipo': tipo
    }
    return context

#Verifica a válidade dos dados a serem cadastrados e efetua o salvamento.
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

#Filtra os dados de acordo com o solicitado na página.
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

#Calcula os valores de renda, gasto e saldo no mês corrente.
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

#Calcula os valores de renda, gasto e saldo de todo o período cadastrado.
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

#Gera os dados para os gráficos, que também são usados nas porcentagens.
def graph(categorias_ref, name_cadastrado):
    totais_dict = {categoria[1]: 0.0 for categoria in categorias_ref}
    for categoria in categorias_ref:
        total_categoria = name_cadastrado.filter(categoria=categoria[0]).aggregate(total=Sum('valor'))['total']
        total_categoria_formatted = round(float(total_categoria), 2) if total_categoria else 0.0
        totais_dict[categoria[1]] = total_categoria_formatted
    totais_dict_ordenado = {k: v for k, v in sorted(totais_dict.items(), key=lambda item: item[1], reverse=True)}
    return totais_dict_ordenado

#Gera os dados das categorias de pagamentos usadas na tabela de porcentagens.
def pagamentos(pagamento_ref, name_cadastrado):
    totais_dict = {categoria[1]: 0.0 for categoria in pagamento_ref}
    for metodo_pagamento in pagamento_ref:
        total_pagamento = name_cadastrado.filter(metodo_pagamento=metodo_pagamento[0]).aggregate(total=Sum('valor'))['total']
        total_pagamento_formatted = round(float(total_pagamento), 2) if total_pagamento else 0.0
        totais_dict[metodo_pagamento[1]] = total_pagamento_formatted
    totais_dict_pagamento_ordenado  = {k: v for k, v in sorted(totais_dict.items(), key=lambda item: item[1], reverse=True)}
    return totais_dict_pagamento_ordenado 

#Calcula as porcentagens sobre as categorias em relação ao total analisado.
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

#Ordena as categorias e facilita a exibição na página.
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

#Limpar a seleção do filtro.
def limpar_filtros(pagina):
    return HttpResponseRedirect(reverse(pagina))

#Editar uma renda/gasto.
@login_required(login_url='login')
def editar_renda_gasto(request, tipo, obj_id):
    if tipo == 'renda':
        form_class = RendasForm
        obj = Rendas.objects.get(pk=obj_id)
        form_editar = RendasForm(
            instance=obj,
            initial={
                'valor': obj.valor,
                'data': obj.data.strftime('%Y-%m-%d') if obj.data else None,
                'metodo_pagamento': obj.metodo_pagamento,
                'categoria': obj.categoria,
                'descricao': obj.descricao,
            }
        )
    else:
        form_class = GastosForm
        obj = get_object_or_404(Gastos, id=obj_id, created_by=request.user)
        form_editar = GastosForm(
            instance=obj,
            initial={
                'valor': obj.valor,
                'data': obj.data.strftime('%Y-%m-%d') if obj.data else None,
                'metodo_pagamento': obj.metodo_pagamento,
                'categoria': obj.categoria,
                'descricao': obj.descricao,
            }
        )
    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            print("Usuário:", request.user)
            instance.created_by = request.user
            print("Criado por:", instance.created_by)
            instance.save(user=request.user)
            messages.success(request, "Atualizado com sucesso!")
            if tipo == 'renda': return redirect('rendas')
            else: return redirect('gastos')
        else:
            print("Formulario invalido")
    return render(request, 'rendas_gastos/editar.html', {'form_editar': form_editar, 'tipo': tipo, 'obj_id': obj_id})

#Deletar uma renda/gasto.
@login_required(login_url='login')
def delete_renda_gasto(request, tipo, obj_id):
    if tipo == 'renda': obj = get_object_or_404(Rendas, pk=obj_id)
    else: obj = get_object_or_404(Gastos, pk=obj_id)
    obj.delete()
    messages.success(request, 'Deletado com sucesso!')
    if tipo == 'renda': return redirect('rendas')
    else: return redirect('gastos')