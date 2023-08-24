from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from django.core.paginator import Paginator
from apps.rendas_gastos.utils import check_authentication
from apps.investimentos.models import Acoes, Fiis, Bdrs, Criptos, RendaFixa, HistoricoCompra
from apps.investimentos.forms import AcoesForm, FiisForm, BdrsForm, CriptosForm, RendaFixaForm
from apps.investimentos.forms import OpcoesAcoes, OpcoesBdrs, OpcoesCriptos, OpcoesFiis, OpcoesRendaFixa

def investimentos(request):
    if not check_authentication(request):
        return redirect('login')
    else:
        #context_renda_gasto = rendas_gastos_view(request)
        return #render(request, 'index.html', context_renda_gasto)

def acoes(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form(request, AcoesForm, Acoes, 'Ação registrada com sucesso!')
    acoes_cadastradas = Acoes.objects.filter(created_by=request.user)
    total_acoes, acoes_cadastradas = filter_selections(request, acoes_cadastradas)
    acoes_cadastradas = acoes_cadastradas.order_by('-data')
    paginator = Paginator(acoes_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'investimentos/acoes.html', {'form': form, 'acoes_cadastradas': acoes_cadastradas,
                    'total_acoes': total_acoes, 'opcoes_acoes': OpcoesAcoes.choices, 'page_obj': page_obj})
    
def fiis(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form(request, FiisForm, Fiis, 'Fundo imobiliário registrado com sucesso!')
    fiis_cadastrados = Fiis.objects.filter(created_by=request.user)
    total_fiis, fiis_cadastrados = filter_selections(request, fiis_cadastrados)
    fiis_cadastrados = fiis_cadastrados.order_by('-data')
    paginator = Paginator(fiis_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'investimentos/fiis.html', {'form': form, 'fiis_cadastrados': fiis_cadastrados,
                    'total_fiis': total_fiis, 'opcoes_fiis': OpcoesFiis.choices, 'page_obj': page_obj})
    
def bdrs(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form(request, BdrsForm, Bdrs, 'BDR registrado com sucesso!')
    bdrs_cadastrados = Bdrs.objects.filter(created_by=request.user)
    total_bdrs, bdrs_cadastrados = filter_selections(request, bdrs_cadastrados)
    bdrs_cadastrados = bdrs_cadastrados.order_by('-data')
    paginator = Paginator(bdrs_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'investimentos/bdrs.html', {'form': form, 'bdrs_cadastrados': bdrs_cadastrados,
                    'total_bdrs': total_bdrs, 'opcoes_bdrs': OpcoesBdrs.choices, 'page_obj': page_obj})
    
def criptos(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form(request, CriptosForm, Criptos, 'Cripto moeda registrada com sucesso!')
    criptos_cadastradas = Criptos.objects.filter(created_by=request.user)
    total_criptos, criptos_cadastradas = filter_selections(request, criptos_cadastradas)
    criptos_cadastradas = criptos_cadastradas.order_by('-data')
    paginator = Paginator(criptos_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'investimentos/criptos.html', {'form': form, 'criptos_cadastradas': criptos_cadastradas,
                    'total_criptos': total_criptos, 'opcoes_criptos': OpcoesCriptos.choices, 'page_obj': page_obj})
    
def rendasfixa(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form(request, RendaFixaForm, RendaFixa, 'Renda fixa registrada com sucesso!')
    rendasfixa_cadastradas = RendaFixa.objects.filter(created_by=request.user)
    total_rendasfixa, rendasfixa_cadastradas = filter_selections(request, rendasfixa_cadastradas)
    rendasfixa_cadastradas = rendasfixa_cadastradas.order_by('-data')
    paginator = Paginator(rendasfixa_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'investimentos/rendasfixa.html', {'form': form, 'rendasfixa_cadastradas': rendasfixa_cadastradas,
                    'total_rendasfixa': total_rendasfixa, 'opcoes_rendasfixa': OpcoesRendaFixa.choices, 'page_obj': page_obj})

def process_form(request, form_class, created_class, success_message):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            ticker = form.cleaned_data['ticker']
            valor = form.cleaned_data['valor']
            quantidade = form.cleaned_data['quantidade']
            dividendo = form.cleaned_data['dividendo']
            data = form.cleaned_data['data']
            categoria = form.cleaned_data['categoria']
            preco_medio = valor if valor > 0 else 0
            valor_total = valor * quantidade
            if created_class.objects.filter(ticker=ticker, created_by=request.user).exists():
                messages.warning(request, f'{ticker} já está cadastrado.')
            else:
                novo = created_class.objects.create(nome=nome, ticker=ticker, valor=valor_total, quantidade=quantidade,
                                                    dividendo=dividendo, preco_medio=preco_medio, data=data,
                                                    categoria=categoria, created_by=request.user)
                novo.save(user=request.user)
                historico_compra = HistoricoCompra.objects.create(ticker=ticker, valor=valor_total, quantidade=quantidade,
                                                    data=data, created_by=request.user)
                historico_compra.save()
                messages.success(request, success_message)
    else:
        form = form_class()
    return form

def filter_selections(request, name_cadastrado_categoria):
    selected_month = request.GET.get('selected_month')
    selected_category = request.GET.get('selected_category')
    filters ={'created_by': request.user}
    if selected_month:
        selected_month_date = datetime.strptime(selected_month, '%Y-%m')
        filters['data__year'] = selected_month_date.year
        filters['data__month'] = selected_month_date.month
    if selected_category:
        filters['categoria'] = selected_category
    name_cadastrado_categoria = name_cadastrado_categoria.filter(**filters)
    total = name_cadastrado_categoria.aggregate(total=Sum('valor'))['total']
    return total, name_cadastrado_categoria

def investimentos_view(request):
    #today = datetime.today()
    #rendas_do_mes = Rendas.objects.filter(created_by=request.user, data__year=today.year, data__month=today.month)
    #renda_mes = sum(renda.valor for renda in rendas_do_mes)
    #gastos_do_mes = Gastos.objects.filter(created_by=request.user, data__year=today.year, data__month=today.month)
    #gasto_mes = sum(gasto.valor for gasto in gastos_do_mes)
    #saldo = renda_mes - gasto_mes
    #context = {
    #    'renda_mes': renda_mes,
    #    'gasto_total': gasto_mes,
    #    'saldo': saldo, 
    #}
    return #context

def delete_acao(request, acao_id):
    acao = get_object_or_404(Acoes, pk=acao_id)
    acao.delete()
    messages.success(request, 'Ação deletada com sucesso!')
    return redirect('acoes')

def delete_fii(request, fii_id):
    fii = get_object_or_404(Fiis, pk=fii_id)
    fii.delete()
    messages.success(request, 'Fundo imobiliário deletado com sucesso!')
    return redirect('fiis')

def delete_bdr(request, bdr_id):
    bdr = get_object_or_404(Fiis, pk=bdr_id)
    bdr.delete()
    messages.success(request, 'BDR deletado com sucesso!')
    return redirect('bdrs')

def delete_cripto(request, cripto_id):
    cripto = get_object_or_404(Fiis, pk=cripto_id)
    cripto.delete()
    messages.success(request, 'Cripto moeda deletada com sucesso!')
    return redirect('criptos')

def delete_rendafixa(request, rendafixa_id):
    rendafixa = get_object_or_404(Fiis, pk=rendafixa_id)
    rendafixa.delete()
    messages.success(request, 'Renda fixa deletada com sucesso!')
    return redirect('rendasfixa')