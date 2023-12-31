from apps.investimentos.forms import AcoesForm, FiisForm, BdrsForm, CriptosForm, RendaFixaForm, DividendoForm, CVForm, CVRendaFixaForm
from apps.investimentos.models import Acoes, Fiis, Bdrs, Criptos, RendasFixa, HistoricoCompra, HistoricoDividendo
from apps.investimentos.forms import OpcoesAcoes, OpcoesBdrs, OpcoesCriptos, OpcoesFiis, OpcoesRendaFixa
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.functions import ExtractMonth, ExtractYear
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from collections import defaultdict
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
import yfinance as yf
import datetime

#Responsável pela página das ações.
@login_required(login_url='login')
def acoes(request):
    context = investimento_paginas_views(request, AcoesForm, Acoes, 'Ação registrada com sucesso!', OpcoesAcoes, False, False)
    return render(request, 'investimentos/acoes.html', context)

#Responsável pela página dos fundos imobiliários.
@login_required(login_url='login')
def fiis(request):
    context = investimento_paginas_views(request, FiisForm, Fiis, 'Fundo imobiliário registrado com sucesso!', OpcoesFiis, False, False)
    return render(request, 'investimentos/fiis.html', context)

#Responsável pela página das BDRs.
@login_required(login_url='login')
def bdrs(request):
    context = investimento_paginas_views(request, BdrsForm, Bdrs, 'BDR registrado com sucesso!', OpcoesBdrs, False, False)
    return render(request, 'investimentos/bdrs.html', context)

#Responsável pela página das cripto moedas.
@login_required(login_url='login')
def criptos(request):
    context = investimento_paginas_views(request, CriptosForm, Criptos, 'Cripto moeda registrada com sucesso!', OpcoesCriptos, False, True)
    return render(request, 'investimentos/criptos.html', context)

#Responsável pela página de renda fixa.
@login_required(login_url='login')
def rendafixa(request):
    context = investimento_paginas_views(request, RendaFixaForm, RendasFixa, 'Renda fixa registrada com sucesso!', OpcoesRendaFixa, True, False)
    return render(request, 'investimentos/rendafixa.html', context)

#Executa as funções para as páginas de investimentos.
def investimento_paginas_views(request, form_process, class_process, message, opcoes_process, veio_rendafixa, veio_cripto):
    #Função que faz a verificação da válidade dos dados, alguns tratamentos de dados e salvamentos das informações.
    def process_form_invest(request, form_class, created_class, success_message, origem, origem_cripto):
        if request.method == 'POST':
            form = form_class(request.POST)
            if form.is_valid() and not origem:
                if origem_cripto:
                    valor = float(form.cleaned_data['valor'])
                    quantidade = float(form.cleaned_data['quantidade'])
                else:
                    valor = form.cleaned_data['valor']
                    quantidade = form.cleaned_data['quantidade']
                preco_medio = valor if valor > 0 else 0
                valor_total = valor * quantidade
                ticker = form.cleaned_data['ticker']
                data = form.cleaned_data['data']
                categoria = form.cleaned_data['categoria']
                ja_cadastrado = created_class.objects.filter(ticker=ticker, created_by=request.user).first()
                if ja_cadastrado:
                    messages.warning(request, f'{ticker} já está cadastrado. Para registrar nova compra ou venda entre na página do {ticker}.')
                else:
                    novo = created_class.objects.create(ticker=ticker, valor=valor_total, quantidade=quantidade,
                                                        preco_medio=preco_medio, data=data,
                                                        categoria=categoria, created_by=request.user)
                    novo.save(user=request.user)
                    historico_compra = HistoricoCompra.objects.create(ticker=ticker, valor=valor_total, quantidade=quantidade,
                                                        data=data, created_by=request.user)
                    historico_compra.save()
                    messages.success(request, success_message)
            elif form.is_valid():
                ticker = form.cleaned_data['ticker']
                valor = form.cleaned_data['valor']
                data = form.cleaned_data['data']
                categoria = form.cleaned_data['categoria']
                ja_cadastrado = created_class.objects.filter(ticker=ticker, created_by=request.user).first()
                if ja_cadastrado:
                    messages.warning(request, f'{ticker} já está cadastrado. Para registrar nova compra ou venda entre na página do {ticker}.')
                else:
                    novo = created_class.objects.create(ticker=ticker, valor=valor, data=data,
                                                        categoria=categoria, created_by=request.user)
                    novo.save(user=request.user)
                    historico_compra = HistoricoCompra.objects.create(ticker=ticker, valor=valor, data=data, created_by=request.user)
                    historico_compra.save()
                    messages.success(request, success_message)
        else:
            form = form_class()
        return form
    
    #Função calcula os valores que foram investidos, recebidos e somados do ativo financeiro em análise.
    def investimento_view(request, classe, veio_rendafixa):
        investido_user = classe.objects.filter(created_by=request.user)
        investido = sum(invest.valor for invest in investido_user)
        dividendo = sum(invest.dividendo for invest in investido_user)
        if not veio_rendafixa: total_mercado =  sum(invest.valor_total_mercado for invest in investido_user) 
        else: total_mercado = 0
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
            'total_mercado': total_mercado,
        }
        return context, investido_user, invest_ticker_dict
    
    #Função para gerar os dados para os gráficos, que também são usadas nas porcentagens.
    def graph(categorias_ref, name_cadastrado):
        totais_dict = {categoria[1]: 0.0 for categoria in categorias_ref}
        for categoria in categorias_ref:
            total_categoria = name_cadastrado.filter(categoria=categoria[0]).aggregate(total=Sum('valor'))['total']
            total_categoria_formatted = round(float(total_categoria), 2) if total_categoria else 0.0
            totais_dict[categoria[1]] = total_categoria_formatted
        totais_dict_ordenado = {k: v for k, v in sorted(totais_dict.items(), key=lambda item: item[1], reverse=True)}
        return totais_dict_ordenado
    
    form = process_form_invest(request, form_process, class_process, message, veio_rendafixa, veio_cripto)
    context_view, dados_cadastrados, invest_ticker_dict = investimento_view(request, class_process, veio_rendafixa)
    categorias = opcoes_process.choices
    grafico = graph(categorias, dados_cadastrados)
    dados_cadastrados = dados_cadastrados.order_by('-valor')
    paginator = Paginator(dados_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    lista_tickers = set()
    for obj in dados_cadastrados:
        ticker = obj.ticker
        lista_tickers.add(ticker)
    dividendos_agrupados_por_mes = get_dividendos_agrupados(request.user, False, lista_tickers)
    context = {
        'form': form,
        'page_obj': page_obj,
        'context_view': context_view,
        'grafico': grafico,
        'invest_ticker_dict': invest_ticker_dict,
        'dividendos_agrupados_por_mes': dividendos_agrupados_por_mes
    }
    return context

#Responsável pela página de detalhes dos ativos.
@login_required(login_url='login')
def detalhes_ticker(request, tipo_investimento, ticker):
    #Calcula os dividendos do mês.
    def dividendos_por_mes(dividendos_cadastrados):
        totais_por_mes = defaultdict(float)
        for dividendo in dividendos_cadastrados:
            mes_ano = dividendo.data.strftime('%Y-%m')
            total_mes = float(dividendo.valor)
            totais_por_mes[mes_ano] += total_mes
        totais_dict_ordenado = {k: round(v, 2) for k, v in sorted(totais_por_mes.items(), key=lambda item: item[0])}
        return totais_dict_ordenado

    #Calcula as compras do mês.
    def compras_por_mes(compras_cadastradas):
        totais_por_mes = defaultdict(float)
        for valor in compras_cadastradas:
            mes_ano = valor.data.strftime('%Y-%m')
            total_mes = float(valor.valor)
            totais_por_mes[mes_ano] += total_mes
        totais_dict_ordenado = {k: round(v, 2) for k, v in sorted(totais_por_mes.items(), key=lambda item: item[0])}
        return totais_dict_ordenado
    
    if request.method == 'POST':
        cadastrar_dividendo(request, ticker, tipo_investimento)
        if tipo_investimento == 'rendasfixa':
            cadastrar_cv_rendafixa(request, ticker, tipo_investimento) 
        else:
            cadastrar_cv(request, ticker, tipo_investimento)                
    form = DividendoForm()
    if tipo_investimento == 'rendasfixa': form_cv = CVRendaFixaForm()
    else: form_cv = CVForm()
    dividendos_cadastrados = HistoricoDividendo.objects.filter(created_by=request.user, ticker=ticker)
    compras_cadastradas = HistoricoCompra.objects.filter(created_by=request.user, ticker=ticker)
    dividendos_cadastrados = dividendos_cadastrados.order_by('-data')
    somados_por_mes = dividendos_por_mes(dividendos_cadastrados)
    compras_cadastradas = compras_cadastradas.order_by('-data')
    somados_compras_por_mes = compras_por_mes(compras_cadastradas)
    paginator = Paginator(dividendos_cadastrados, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    paginator_cv = Paginator(compras_cadastradas, 6)
    page_number_cv = request.GET.get('page')
    page_obj_cv = paginator_cv.get_page(page_number_cv)
    total_div = dividendos_cadastrados.aggregate(total=Sum('valor'))['total']
    total_compra = compras_cadastradas.aggregate(total=Sum('valor'))['total']
    total_quantidade = compras_cadastradas.aggregate(total=Sum('quantidade'))['total']
    if total_compra < 0 or total_quantidade == 0: total_compra = 0
    context = {
        'tipo_investimento': tipo_investimento,
        'ticker': ticker,
        'form': form,
        'form_cv': form_cv,
        'somados_por_mes': somados_por_mes,
        'somados_compras_por_mes': somados_compras_por_mes,
        'page_obj': page_obj,
        'page_obj_cv': page_obj_cv,
        'total_div': total_div,
        'total_compra': total_compra
    }
    return render(request, 'investimentos/ticker.html', context)

#Cadastrar uma compra ou venda de ativos.
@login_required(login_url='login')
def cadastrar_cv(request, ticker, tipo_investimento):
    if request.method == 'POST':
        form_cv = CVForm(request.POST)
        if form_cv.is_valid():
            if tipo_investimento == 'criptos':
                valor = float(form_cv.cleaned_data['valor'])
                quantidade = float(form_cv.cleaned_data['quantidade'])
            else:
                valor = form_cv.cleaned_data['valor']
                quantidade = form_cv.cleaned_data['quantidade']
            data = form_cv.cleaned_data['data']
            valor_total = valor * quantidade
            if tipo_investimento == 'acoes': created_class = Acoes
            elif tipo_investimento == 'fiis': created_class = Fiis
            elif tipo_investimento == 'bdrs': created_class = Bdrs
            elif tipo_investimento == 'criptos': created_class = Criptos
            elif tipo_investimento == 'rendafixa': created_class = RendasFixa
            ja_cadastrado = created_class.objects.filter(ticker=ticker, created_by=request.user).first()
            if 'compra' in request.POST:
                if ja_cadastrado:
                    ja_cadastrado.valor += valor_total
                    if not tipo_investimento == 'rendafixa':
                        ja_cadastrado.quantidade += quantidade
                        ja_cadastrado.preco_medio = ((ja_cadastrado.valor)/ja_cadastrado.quantidade)
                    if data < ja_cadastrado.data: ja_cadastrado.data = data
                    ja_cadastrado.save(user=request.user)
                    historico_compra = HistoricoCompra.objects.create(ticker=ticker, valor=valor_total, quantidade=quantidade,
                                                        data=data, created_by=request.user)
                    historico_compra.save()
                    messages.success(request, f'Compra do {ticker} adicionada.')
                else:
                    messages.error(request, "Impossível registrar compra de um ativo não cadastrado! ")
            if 'venda' in request.POST:
                if ja_cadastrado:
                    liquidou = ja_cadastrado.quantidade - quantidade
                    if liquidou >= 0:
                        if liquidou != 0:
                            ja_cadastrado.valor -= valor_total
                            ja_cadastrado.quantidade -= quantidade
                            ja_cadastrado.preco_medio = ((ja_cadastrado.valor)/ja_cadastrado.quantidade)
                        else:
                            ja_cadastrado.valor = 0
                            ja_cadastrado.quantidade = 0
                            ja_cadastrado.preco_medio = 0
                        if data > ja_cadastrado.data: ja_cadastrado.data = data
                        ja_cadastrado.save(user=request.user)
                        quantidade = quantidade*-1
                        valor_total = valor_total*-1
                        historico_compra = HistoricoCompra.objects.create(ticker=ticker, valor=valor_total, quantidade=quantidade,
                                                            data=data, created_by=request.user)
                        historico_compra.save()
                        messages.success(request, f'Venda do {ticker} adicionada.')
                    else:
                        messages.error(request, "Quantidade de venda superior ao possuído! ")
                else:
                    messages.error(request, "Impossível registrar venda de um ativo não cadastrado! ")

#Cadastrar uma compra ou venda de renda fixa.
@login_required(login_url='login')
def cadastrar_cv_rendafixa(request, ticker, tipo_investimento):
    if request.method == 'POST':
        form_cv = CVRendaFixaForm(request.POST)
        if form_cv.is_valid():
            valor = form_cv.cleaned_data['valor']
            data = form_cv.cleaned_data['data']
            ja_cadastrado = RendasFixa.objects.filter(ticker=ticker, created_by=request.user).first()
            if 'compra' in request.POST:
                if ja_cadastrado:
                    ja_cadastrado.valor += valor
                    if data < ja_cadastrado.data: ja_cadastrado.data = data
                    ja_cadastrado.save(user=request.user)
                    historico_compra = HistoricoCompra.objects.create(ticker=ticker, valor=valor,
                                                        data=data, created_by=request.user)
                    historico_compra.save()
                    messages.success(request, f'Compra do {ticker} adicionada.')
                else:
                    messages.error(request, "Impossível registrar compra de um ativo não cadastrado! ")
            if 'venda' in request.POST:
                if ja_cadastrado:
                    liquidou = ja_cadastrado.valor - valor
                    if liquidou >= 0:
                        if liquidou != 0:
                            ja_cadastrado.valor -= valor
                        else:
                            ja_cadastrado.valor = 0
                        if data > ja_cadastrado.data: ja_cadastrado.data = data
                        ja_cadastrado.save(user=request.user)
                        valor = valor*-1
                        historico_compra = HistoricoCompra.objects.create(ticker=ticker, valor=valor,
                                                            data=data, created_by=request.user)
                        historico_compra.save()
                        messages.success(request, f'Venda do {ticker} adicionada.')
                    else:
                        messages.error(request, "Quantidade de venda superior ao possuído! ")
                else:
                    messages.error(request, "Impossível registrar venda de um ativo não cadastrado! ")

#Cadastro de dividendo dos ativos.
def cadastrar_dividendo(request, ticker, tipo_investimento):
    if request.method == 'POST':
        form = DividendoForm(request.POST)
        if form.is_valid() and 'dividendo' in request.POST:
            if tipo_investimento == 'criptos':
                valor = float(form.cleaned_data['valor'])
            else:
                valor = form.cleaned_data['valor']
            data = form.cleaned_data['data']
            novo_dividendo = HistoricoDividendo.objects.create(
                ticker=ticker,
                valor=valor,
                data=data,
                created_by=request.user,
            )
            novo_dividendo.save()
            messages.success(request, 'Dividendo registrado com sucesso!')
            if tipo_investimento == 'acoes':
                ativo_cadastrado = Acoes.objects.filter(ticker=ticker, created_by=request.user).first()
            elif tipo_investimento == 'fiis':
                ativo_cadastrado = Fiis.objects.filter(ticker=ticker, created_by=request.user).first()
            elif tipo_investimento == 'bdrs':
                ativo_cadastrado = Bdrs.objects.filter(ticker=ticker, created_by=request.user).first()
            elif tipo_investimento == 'rendafixa':
                ativo_cadastrado = RendasFixa.objects.filter(ticker=ticker, created_by=request.user).first()
            else:
                ativo_cadastrado = Criptos.objects.filter(ticker=ticker, created_by=request.user).first()
            ativo_cadastrado.dividendo = ativo_cadastrado.dividendo + valor
            ativo_cadastrado.save(user=request.user)
    else:
        form = DividendoForm()
    return form

#Função calcula os valores que foram investidos, recebidos e somados de cada ativo financeiro.
def investimentos_total_view(request):
    #Função para ajudar nos calculos de investimentos_total_view.
    def calcular_valores_investimentos(model_class, request_user, renda_fixa):
        investimentos = model_class.objects.filter(created_by=request_user)
        soma_investimentos = round(sum(float(investment.valor) for investment in investimentos), 2)
        soma_dividendos = round(sum(float(investment.dividendo) for investment in investimentos), 2)
        total_investido = round(soma_investimentos + soma_dividendos, 2)
        if renda_fixa:
            return soma_investimentos, soma_dividendos, total_investido
        else:
            investimentos_consolidado = round(sum(float(invest.valor_mercado) * float(invest.quantidade) for invest in investimentos), 2)
            return soma_investimentos, soma_dividendos, total_investido, investimentos_consolidado
    
    investido_rendasfixa, dividendo_rendasfixa, total_rendasfixa = calcular_valores_investimentos(RendasFixa, request.user, True)
    investido_acoes, dividendo_acoes, total_acoes, investido_acoes_consolidado = calcular_valores_investimentos(Acoes, request.user, False)
    investido_fiis, dividendo_fiis, total_fiis, investido_fiis_consolidado = calcular_valores_investimentos(Fiis, request.user, False)
    investido_bdrs, dividendo_bdrs, total_bdrs, investido_bdrs_consolidado = calcular_valores_investimentos(Bdrs, request.user, False)    
    investido_criptos_user = Criptos.objects.filter(created_by=request.user)
    dividendo_criptos = 0
    for ticker in investido_criptos_user:
        cotacao_consolidada = Criptos.objects.filter(ticker=ticker)
        if cotacao_consolidada:
            valor_reais = round(float(cotacao_consolidada.preco_medio) * float(cotacao_consolidada.dividendo), 2)
        else:
            valor_reais = round(float(ticker.preco_medio) * float(ticker.dividendo), 2)
        dividendo_criptos += valor_reais
    investido_criptos = round(sum(float(cripto.valor) for cripto in investido_criptos_user), 2)
    total_criptos = round(investido_criptos + dividendo_criptos, 2)
    investido_criptos_consolidado = round(sum(float(cripto.valor_mercado) * float(cripto.quantidade) for cripto in investido_criptos_user), 2)
    lucro_acao = round((investido_acoes_consolidado - investido_acoes) + dividendo_acoes, 2)
    lucro_fii = round((investido_fiis_consolidado - investido_fiis) + dividendo_fiis, 2)
    lucro_bdr = round((investido_bdrs_consolidado - investido_bdrs) + dividendo_bdrs, 2)
    lucro_cripto = round((investido_criptos_consolidado - investido_criptos) + dividendo_criptos, 2)
    total_lucro = round((dividendo_rendasfixa + lucro_acao + lucro_fii + lucro_bdr + lucro_cripto), 2)
    total_dividendos = round(dividendo_rendasfixa + dividendo_acoes + dividendo_fiis + dividendo_bdrs + dividendo_criptos, 2)
    total_comprado = round((investido_rendasfixa + investido_acoes + investido_fiis + investido_bdrs + investido_criptos), 2)
    total_consolidado = round((investido_rendasfixa + investido_acoes_consolidado + investido_fiis_consolidado + investido_bdrs_consolidado + investido_criptos_consolidado), 2)
    dividendos_agrupados_por_mes = get_dividendos_agrupados(request.user, True, None)
    context = {
        'investido_rendasfixa': investido_rendasfixa,
        'dividendo_rendasfixa': dividendo_rendasfixa,
        'total_rendasfixa': total_rendasfixa,
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
        'investido_acoes_consolidado': investido_acoes_consolidado,
        'investido_fiis_consolidado': investido_fiis_consolidado,
        'investido_bdrs_consolidado': investido_bdrs_consolidado,
        'investido_criptos_consolidado': investido_criptos_consolidado,
        'lucro_acao': lucro_acao,
        'lucro_fii': lucro_fii,
        'lucro_bdr': lucro_bdr,
        'lucro_cripto': lucro_cripto,
        'total_lucro': total_lucro,
        'total_dividendos': total_dividendos,
        'total_comprado': total_comprado,
        'total_consolidado': total_consolidado,
        'dividendos_agrupados_por_mes': dividendos_agrupados_por_mes
    }
    return context

# Função para obter o histórico de dividendos agrupado por mês e ticker
def get_dividendos_agrupados(request_user, index, lista):
    if index:
        tickers_unicos = set()
        dividendos_agrupados = (
        HistoricoDividendo.objects.filter(created_by=request_user)
        .annotate(mes=ExtractMonth('data'), ano=ExtractYear('data'))
        .values('ticker', 'ano', 'mes')
        .annotate(total_dividendos=Sum('valor'))
        .order_by('ano', 'mes', 'ticker')
        )
    else:
        tickers_unicos = lista
        dividendos_agrupados = (
            HistoricoDividendo.objects.filter(created_by=request_user, ticker__in=tickers_unicos)
            .annotate(mes=ExtractMonth('data'), ano=ExtractYear('data'))
            .values('ticker', 'ano', 'mes')
            .annotate(total_dividendos=Sum('valor'))
            .order_by('ano', 'mes', 'ticker')
        )
    dados_organizados = {}
    for div in dividendos_agrupados:
        mes, ano, ticker = div['mes'], div['ano'], div['ticker']
        total_dividendos = float(round(div['total_dividendos'], 2))
        chave_data = f"{ano}-{mes}"
        if index: tickers_unicos.add(ticker)
        if chave_data  not in dados_organizados:
            dados_organizados[chave_data] = {ticker: total_dividendos}
        else:
            if ticker not in dados_organizados[chave_data]:
                dados_organizados[chave_data][ticker] = total_dividendos
            else:
                dados_organizados[chave_data][ticker] += total_dividendos
    for chave_data in dados_organizados:
        for ticker in tickers_unicos:
            if ticker not in dados_organizados[chave_data]:
                dados_organizados[chave_data][ticker] = 0.00
        dados_organizados[chave_data] = dict(sorted(dados_organizados[chave_data].items(), key=lambda x: x[1]))
    return dados_organizados

#Executa todas as funções para pegar as cotações e consolidar a carteira.
@login_required(login_url='login')
def consolidar_carteira(request):
    #Obtem as cotações do yahoo finance.
    def obter_cotacao(request, cotacoes, dados, class_name, data_atual):
        for ticker in dados:
            ticker_temporario = ticker.replace(".SA", "")
            dados_salvos = class_name.objects.filter(ticker=ticker_temporario, created_by=request.user).first()
            if dados_salvos:
                data_inicial = dados_salvos.data
                try:
                    dados = yf.download(ticker)
                    cotacoes[ticker] = round(dados["Close"].iloc[-1], 2)
                except Exception as e:
                    print("Erro:", str(e))
        cotacoes = {chave.replace(".SA", ""): valor for chave, valor in cotacoes.items()}
        return cotacoes

    #Obtem as cotações de criptomoedas no yahoo finance.
    def obter_cotacao_cripto(request, cotacoes, dados, class_name, data_atual):
        cotacao_dolar = yf.download("BRL=X")
        cotacao_dolar = round(cotacao_dolar["Close"].iloc[-1], 2)
        for ticker in dados:
            ticker_temporario = ticker.replace("-USD", "")
            dados_salvos = class_name.objects.filter(ticker=ticker_temporario, created_by=request.user).first()
            if dados_salvos:
                data_inicial = dados_salvos.data
                try:
                    dados = yf.download(ticker)
                    cotacoes[ticker] = round((dados["Close"].iloc[-1] * cotacao_dolar), 8)
                except Exception as e:
                    print("Erro:", str(e))
        cotacoes = {chave.replace("-USD", ""): valor for chave, valor in cotacoes.items()}
        return cotacoes
    
    #Salva a consolidação.
    def salvar_consolidacao(request, dados, class_name):
        for ticker, cotacao in dados.items():
            investimento = class_name.objects.filter(ticker=ticker, created_by=request.user).first()
            if investimento:
                quantidade = investimento.quantidade
                investimento.valor_mercado = cotacao
                if isinstance(investimento, Criptos): investimento.valor_total_mercado = Decimal(cotacao) * quantidade
                else: investimento.valor_total_mercado = cotacao * quantidade
                investimento.save(user=request.user)

    if request.method == 'POST':
        data_atual = datetime.date.today()
        investido_acoes = Acoes.objects.filter(created_by=request.user)
        investido_fiis = Fiis.objects.filter(created_by=request.user)
        investido_bdrs = Bdrs.objects.filter(created_by=request.user)
        investido_criptos = Criptos.objects.filter(created_by=request.user)
        dados_acoes = {acao.ticker + '.SA': 0 for acao in investido_acoes}
        dados_fiis = {fii.ticker + '.SA': 0 for fii in investido_fiis}
        dados_bdrs = {bdr.ticker + '.SA': 0 for bdr in investido_bdrs}
        dados_criptos = {cripto.ticker + '-USD': 0 for cripto in investido_criptos}
        cotacoes = {}
        cotacoes_acoes = obter_cotacao(request, cotacoes, dados_acoes, Acoes, data_atual)
        cotacoes_fiis = obter_cotacao(request, cotacoes, dados_fiis, Fiis, data_atual)
        cotacoes_bdrs = obter_cotacao(request, cotacoes, dados_bdrs, Bdrs, data_atual)
        cotacoes_criptos = obter_cotacao_cripto(request, cotacoes, dados_criptos, Criptos, data_atual)
        salvar_consolidacao(request, cotacoes_acoes, Acoes)
        salvar_consolidacao(request, cotacoes_fiis, Fiis)
        salvar_consolidacao(request, cotacoes_bdrs, Bdrs)
        salvar_consolidacao(request, cotacoes_criptos, Criptos)
    return redirect('index')

#Deletar um investimento.
@login_required(login_url='login')
def delete_investimento(request, tipo_investimento, invest_id):
    if tipo_investimento == 'acoes':
        acao = get_object_or_404(Acoes, pk=invest_id)
        ticker = acao.ticker
        acao.delete()
        historico_delete = HistoricoCompra.objects.filter(ticker=ticker)
        historico_delete.delete()
        dividendos_delete = HistoricoDividendo.objects.filter(ticker=ticker)
        dividendos_delete.delete()
        messages.success(request, 'Ação deletada com sucesso!')
        return redirect('acoes')
    if tipo_investimento == 'fiis':
        fii = get_object_or_404(Fiis, pk=invest_id)
        ticker = fii.ticker
        fii.delete()
        historico_delete = HistoricoCompra.objects.filter(ticker=ticker)
        historico_delete.delete()
        dividendos_delete = HistoricoDividendo.objects.filter(ticker=ticker)
        dividendos_delete.delete()
        messages.success(request, 'Fundo imobiliário deletado com sucesso!')
        return redirect('fiis')
    if tipo_investimento == 'bdrs':
        bdr = get_object_or_404(Bdrs, pk=invest_id)
        ticker = bdr.ticker
        bdr.delete()
        historico_delete = HistoricoCompra.objects.filter(ticker=ticker)
        historico_delete.delete()
        dividendos_delete = HistoricoDividendo.objects.filter(ticker=ticker)
        dividendos_delete.delete()
        messages.success(request, 'BDR deletado com sucesso!')
        return redirect('bdrs')
    if tipo_investimento == 'criptos':
        cripto = get_object_or_404(Criptos, pk=invest_id)
        ticker = cripto.ticker
        cripto.delete()
        historico_delete = HistoricoCompra.objects.filter(ticker=ticker)
        historico_delete.delete()
        dividendos_delete = HistoricoDividendo.objects.filter(ticker=ticker)
        dividendos_delete.delete()
        messages.success(request, 'Cripto moeda deletada com sucesso!')
        return redirect('criptos')
    if tipo_investimento == 'rendasfixa':
        fixa = get_object_or_404(RendasFixa, pk=invest_id)
        ticker = fixa.ticker
        fixa.delete()
        historico_delete = HistoricoCompra.objects.filter(ticker=ticker)
        historico_delete.delete()
        dividendos_delete = HistoricoDividendo.objects.filter(ticker=ticker)
        dividendos_delete.delete()
        messages.success(request, 'Renda fixa deletada com sucesso!')
        return redirect('rendafixa')

#Deletar um dividendo.
@login_required(login_url='login')
def delete_div(request, tipo_investimento, ticker, div_id,):
    dividendo = get_object_or_404(HistoricoDividendo, pk=div_id)
    dividendo.delete()
    messages.success(request, 'Dividendo deletado com sucesso!')
    return redirect('detalhes_ticker', tipo_investimento, ticker)

#Deletar uma compra ou venda.
@login_required(login_url='login')
def delete_cv(request, tipo_investimento, ticker, cv_id,):
    cv = get_object_or_404(HistoricoCompra, pk=cv_id)
    if tipo_investimento == 'acoes': investimento = Acoes.objects.filter(ticker=ticker, created_by=request.user).first()
    elif tipo_investimento == 'fiis': investimento = Fiis.objects.filter(ticker=ticker, created_by=request.user).first()
    elif tipo_investimento == 'bdrs': investimento = Bdrs.objects.filter(ticker=ticker, created_by=request.user).first()
    elif tipo_investimento == 'criptos': investimento = Criptos.objects.filter(ticker=ticker, created_by=request.user).first()
    elif tipo_investimento == 'rendasfixa': investimento = RendasFixa.objects.filter(ticker=ticker, created_by=request.user).first()
    valor = cv.valor
    quantidade = cv.quantidade
    if valor < 0:
        valor = valor*-1
        quantidade = quantidade*-1
    if tipo_investimento == 'rendasfixa':
        if cv.valor > 0: investimento.valor -= valor
        else: investimento.valor += valor
    else:
        if cv.valor > 0:
            investimento.valor -= valor
            investimento.quantidade -= quantidade
        else:
            investimento.valor += valor
            investimento.quantidade += quantidade
    investimento.save(user=request.user)
    cv.delete()
    messages.success(request, 'Deletada com sucesso!')
    return redirect('detalhes_ticker', tipo_investimento, ticker)