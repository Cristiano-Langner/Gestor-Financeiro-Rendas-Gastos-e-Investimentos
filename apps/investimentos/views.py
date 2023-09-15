from apps.investimentos.models import Acoes, Fiis, Bdrs, Criptos, RendasFixa, HistoricoCompra, UltimaVerificacao
from apps.investimentos.forms import OpcoesAcoes, OpcoesBdrs, OpcoesCriptos, OpcoesFiis, OpcoesRendaFixa
from apps.investimentos.forms import AcoesForm, FiisForm, BdrsForm, CriptosForm, RendaFixaForm
from django.shortcuts import render, redirect, get_object_or_404
from apps.rendas_gastos.utils import check_authentication
from django.core.paginator import Paginator
from pandas_datareader import data as pdr
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime
import pandas as pd
import yfinance

#Responsável pela página das ações.
def acoes(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form_invest(request, AcoesForm, Acoes, 'Ação registrada com sucesso!')
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

#Responsável pela página dos fundos imobiliários.
def fiis(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form_invest(request, FiisForm, Fiis, 'Fundo imobiliário registrado com sucesso!')
    context_view, fiis_cadastrados, invest_ticker_dict = investimento_view(request, Fiis)
    total_fiis, fiis_cadastrados = filter_selections(request, fiis_cadastrados)
    tabela_tickers = tabela(fiis_cadastrados)
    categorias = OpcoesFiis.choices
    grafico = graph(categorias, fiis_cadastrados)
    paginator = Paginator(fiis_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print("Tabela: ")
    print(tabela_tickers)
    context = {
        'form': form,
        'fiis_cadastrados': fiis_cadastrados,
        'total_fiis': total_fiis,
        'opcoes_fiis': OpcoesFiis.choices,
        'page_obj': page_obj,
        'context_view': context_view,
        'grafico': grafico,
        'invest_ticker_dict': invest_ticker_dict,
        'tabela_tickers': tabela_tickers
    }
    return render(request, 'investimentos/fiis.html', context)

#Responsável pela página das BDRs.
def bdrs(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form_invest(request, BdrsForm, Bdrs, 'BDR registrado com sucesso!')
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

#Responsável pela página das cripto moedas.
def criptos(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form_invest(request, CriptosForm, Criptos, 'Cripto moeda registrada com sucesso!')
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

#Responsável pela página de renda fixa.
def rendasfixa(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form_invest(request, RendaFixaForm, RendasFixa, 'Renda fixa registrada com sucesso!')
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

#Função que faz a verificação da válidade dos dados, alguns tratamentos de dados e salvamentos das informações.
def process_form_invest(request, form_class, created_class, success_message):
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

#Função para filtrar os dados de acordo com o solicitado na página.
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

#Função calcula os valores que foram investidos, recebidos e somados de cada ativo financeiro.
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

#Função calcula os valores que foram investidos, recebidos e somados do ativo financeiro em análise.
def investimento_view(request, classe):
    investido_user = classe.objects.filter(created_by=request.user)
    investido = sum(invest.valor for invest in investido_user)
    dividendo = sum(invest.dividendo for invest in investido_user)
    total = investido + dividendo
    invest_ticker = []
    for ticker in investido_user:
        invest_ticker.append((ticker.ticker, float(ticker.valor)))
    invest_ticker_ordenado = sorted(invest_ticker, key=lambda x: x[1], reverse=True)
    invest_ticker_dict = {ticker: valor for ticker, valor in invest_ticker_ordenado}
    context = {
        'investido': investido,
        'dividendo': dividendo,
        'total': total,
    }
    return context, investido_user, invest_ticker_dict

#Função responsável pela organização e paginação dos elementos na página.
def paginacao(request, invest_cadastrados):
    invest_cadastrados = invest_cadastrados.order_by('-data')
    paginator = Paginator(invest_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj, invest_cadastrados

#Função para gerar os dados para os gráficos, que também são usadas nas porcentagens.
def graph(categorias_ref, name_cadastrado):
    totais_dict = {categoria[1]: 0.0 for categoria in categorias_ref}
    for categoria in categorias_ref:
        total_categoria = name_cadastrado.filter(categoria=categoria[0]).aggregate(total=Sum('valor'))['total']
        total_categoria_formatted = round(float(total_categoria), 2) if total_categoria else 0.0
        totais_dict[categoria[1]] = total_categoria_formatted
    totais_dict_ordenado = {k: v for k, v in sorted(totais_dict.items(), key=lambda item: item[1], reverse=True)}
    return totais_dict_ordenado

def tabela(invest_cadastrados):
    ultima_verificacao = obter_ultima_verificacao()
    data_hora_atual = datetime.today()
    if not invest_cadastrados:
        pass
    elif ultima_verificacao is None or ultima_verificacao != data_hora_atual.date():
        print("Ultima verificação:", ultima_verificacao)
        print("Data atual: ", data_hora_atual)
        ticker = [str(item).split('=')[1][:-1] for item in invest_cadastrados]
        tickers = [ticker + ".SA" for ticker in ticker]
        cotacoes = obter_cotacao_atual(tickers=tickers)
        salvar_ultima_verificacao(data_hora_atual)
    else:
        cotacoes = {}
    print("Antes das quantidade:")
    print(cotacoes)
    return cotacoes

def obter_cotacao_atual(tickers):
    cotacoes = {}
    for ticker in tickers:
        valor = yfinance.Ticker(ticker)
        cotacoes[ticker] = valor.info["regularMarketPreviousClose"]
        cotacoes = {chave.replace(".SA", ""): valor for chave, valor in cotacoes.items()}
    return cotacoes

def obter_cotacao(tickers):
    data_atual = datetime.today().strftime("%Y-%m-%d")
    yfinance.pdr_override()
    #Para pegar todos de uma vez, passar uma lista com os tickers, precisa ser lista.
    cotacao = pdr.get_data_yahoo(tickers, "2023-09-01", data_atual)["Adj Close"]
    print("tentantiva ultiomo valor")
    valor = yfinance.Ticker(tickers)
    informacoes_tempo_real = valor.info
    if "last_price" in informacoes_tempo_real:
        valor_atual = informacoes_tempo_real["last_price"]
        print(f'Valor atual de {tickers}: {valor_atual}')
    else:
        print(f'As informações em tempo real para {tickers} não estão disponíveis gratuitamente.')
    return cotacao

def obter_ultima_verificacao():
    try:
        ultima_verificacao = UltimaVerificacao.objects.latest('id')
        return ultima_verificacao.data
    except UltimaVerificacao.DoesNotExist:
        return None

def salvar_ultima_verificacao(data_atual):
    UltimaVerificacao.objects.create(data=data_atual)

#Função para deletar uma ação.
def delete_acao(request, acao_id):
    acao = get_object_or_404(Acoes, pk=acao_id)
    acao.delete()
    messages.success(request, 'Ação deletada com sucesso!')
    return redirect('acoes')

#Função para deletar um fundo imobiliário.
def delete_fii(request, fii_id):
    fii = get_object_or_404(Fiis, pk=fii_id)
    fii.delete()
    messages.success(request, 'Fundo imobiliário deletado com sucesso!')
    return redirect('fiis')

#Função para deletar um BDR.
def delete_bdr(request, bdr_id):
    bdr = get_object_or_404(Fiis, pk=bdr_id)
    bdr.delete()
    messages.success(request, 'BDR deletado com sucesso!')
    return redirect('bdrs')

#Função para deletar uma cripto moeda.
def delete_cripto(request, cripto_id):
    cripto = get_object_or_404(Fiis, pk=cripto_id)
    cripto.delete()
    messages.success(request, 'Cripto moeda deletada com sucesso!')
    return redirect('criptos')

#Função para deletar uma renda fixa.
def delete_rendafixa(request, rendafixa_id):
    rendafixa = get_object_or_404(Fiis, pk=rendafixa_id)
    rendafixa.delete()
    messages.success(request, 'Renda fixa deletada com sucesso!')
    return redirect('rendasfixa')