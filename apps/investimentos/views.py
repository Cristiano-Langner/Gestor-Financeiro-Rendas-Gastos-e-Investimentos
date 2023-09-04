from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from django.core.paginator import Paginator
from apps.rendas_gastos.utils import check_authentication
from apps.investimentos.models import Acoes, Fiis, Bdrs, Criptos, RendasFixa, HistoricoCompra
from apps.investimentos.forms import AcoesForm, FiisForm, BdrsForm, CriptosForm, RendaFixaForm
from apps.investimentos.forms import OpcoesAcoes, OpcoesBdrs, OpcoesCriptos, OpcoesFiis, OpcoesRendaFixa

def acoes(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form(request, AcoesForm, Acoes, 'Ação registrada com sucesso!')
    context_view, acoes_cadastradas = investimento_view(request, Acoes)
    grafico = graph(acoes_cadastradas)
    total_acoes, acoes_cadastradas = filter_selections(request, acoes_cadastradas)
    acoes_cadastradas = acoes_cadastradas.order_by('-data')
    paginator = Paginator(acoes_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'acoes_cadastradas': acoes_cadastradas,
        'total_acoes': total_acoes,
        'opcoes_acoes': OpcoesAcoes.choices,
        'page_obj': page_obj,
        'context_view': context_view,
        'grafico': grafico
    }
    return render(request, 'investimentos/acoes.html', context)
    
def fiis(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form(request, FiisForm, Fiis, 'Fundo imobiliário registrado com sucesso!')
    context_view, fiis_cadastrados = investimento_view(request, Fiis)
    total_fiis, fiis_cadastrados = filter_selections(request, fiis_cadastrados)
    paginator = Paginator(fiis_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'fiis_cadastrados': fiis_cadastrados,
        'total_fiis': total_fiis,
        'opcoes_fiis': OpcoesFiis.choices,
        'page_obj': page_obj,
        'context_view': context_view
    }
    return render(request, 'investimentos/fiis.html', context)
    
def bdrs(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form(request, BdrsForm, Bdrs, 'BDR registrado com sucesso!')
    context_view, bdrs_cadastrados = investimento_view(request, Bdrs)
    total_bdrs, bdrs_cadastrados = filter_selections(request, bdrs_cadastrados)
    paginator = Paginator(bdrs_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'bdrs_cadastrados': bdrs_cadastrados,
        'total_bdrs': total_bdrs,
        'opcoes_bdrs': OpcoesBdrs.choices,
        'page_obj': page_obj,
        'context_view': context_view
    }
    return render(request, 'investimentos/bdrs.html', context)
    
def criptos(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form(request, CriptosForm, Criptos, 'Cripto moeda registrada com sucesso!')
    context_view, criptos_cadastradas = investimento_view(request, Criptos)
    total_criptos, criptos_cadastradas = filter_selections(request, criptos_cadastradas)
    paginator = Paginator(criptos_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'criptos_cadastradas': criptos_cadastradas,
        'total_criptos': total_criptos,
        'opcoes_criptos': OpcoesCriptos.choices,
        'page_obj': page_obj,
        'context_view': context_view
    }
    return render(request, 'investimentos/criptos.html', context)
    
def rendasfixa(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form(request, RendaFixaForm, RendasFixa, 'Renda fixa registrada com sucesso!')
    context_view, rendasfixa_cadastradas = investimento_view(request, RendasFixa)
    total_rendasfixa, rendasfixa_cadastradas = filter_selections(request, rendasfixa_cadastradas)
    paginator = Paginator(rendasfixa_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'rendasfixa_cadastradas': rendasfixa_cadastradas,
        'total_rendasfixa': total_rendasfixa,
        'opcoes_rendasfixa': OpcoesRendaFixa.choices,
        'page_obj': page_obj,
        'context_view': context_view
    }
    return render(request, 'investimentos/rendasfixa.html', context)

def process_form(request, form_class, created_class, success_message):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            valor = form.cleaned_data['valor']
            quantidade = form.cleaned_data['quantidade']
            data = form.cleaned_data['data']
            categoria = form.cleaned_data['categoria']
            preco_medio = valor if valor > 0 else 0
            valor_total = valor * quantidade
            if created_class.objects.filter(ticker=ticker, created_by=request.user).exists():
                messages.warning(request, f'{ticker} já está cadastrado.')
            else:
                novo = created_class.objects.create(ticker=ticker, valor=valor_total, quantidade=quantidade,
                                                    preco_medio=preco_medio, data=data,
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

def investimentos_total_view(request):
    investido_acoes_user = Acoes.objects.filter(created_by=request.user)
    investido_acoes = sum(acao.valor for acao in investido_acoes_user)
    dividendo_acoes = sum(acao.dividendo for acao in investido_acoes_user)
    total_acoes = investido_acoes + dividendo_acoes
    investido_fiis_user = Fiis.objects.filter(created_by=request.user)
    investido_fiis = sum(fii.valor for fii in investido_fiis_user)
    dividendo_fiis = sum(fii.dividendo for fii in investido_acoes_user)
    total_fiis = investido_fiis + dividendo_fiis
    investido_bdrs_user = Bdrs.objects.filter(created_by=request.user)
    investido_bdrs = sum(bdr.valor for bdr in investido_bdrs_user)
    dividendo_bdrs = sum(bdr.dividendo for bdr in investido_bdrs_user)
    total_bdrs = investido_bdrs = dividendo_bdrs
    investido_criptos_user = Criptos.objects.filter(created_by=request.user)
    investido_criptos = sum(cripto.valor for cripto in investido_criptos_user)
    dividendo_criptos = sum(cripto.dividendo for cripto in investido_criptos_user)
    total_criptos = investido_criptos + dividendo_criptos
    investido_rendasfixa_user = RendasFixa.objects.filter(created_by=request.user)
    investido_rendasfixa = sum(rendafixa.valor for rendafixa in investido_rendasfixa_user)
    dividendo_rendasfixa = sum(rendafixa.dividendo for rendafixa in investido_rendasfixa_user)
    total_rendasfixa = investido_rendasfixa + dividendo_rendasfixa
    context = {
        'investido_acoes': investido_acoes,
        'dividendo_acoes': dividendo_acoes,
        'total_acoes': total_acoes,
        'investido_fiis': investido_fiis,
        'dividendo_fiis': dividendo_fiis,
        'total_fiis': total_fiis,
        'investido_bdrs': investido_bdrs,
        'dividendo_bdrs': dividendo_bdrs,
        'total_bdrs': total_bdrs,
        'investido_criptos': investido_criptos,
        'dividendo_criptos': dividendo_criptos,
        'total_criptos': total_criptos,
        'investido_rendasfixa': investido_rendasfixa,
        'dividendo_rendasfixa': dividendo_rendasfixa,
        'total_rendasfixa': total_rendasfixa,
    }
    return context

def investimento_view(request, classe):
    investido_user = classe.objects.filter(created_by=request.user)
    investido = sum(invest.valor for invest in investido_user)
    dividendo = sum(invest.dividendo for invest in investido_user)
    total = investido + dividendo
    context = {
        'investido': investido,
        'dividendo': dividendo,
        'total': total,
    }
    return context, investido_user

def graph(name_cadastrado):
    return 

def paginacao(request, invest_cadastrados):
    invest_cadastrados = invest_cadastrados.order_by('-data')
    paginator = Paginator(invest_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj, invest_cadastrados

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