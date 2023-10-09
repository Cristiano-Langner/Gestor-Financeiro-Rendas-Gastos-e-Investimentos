from apps.investimentos.models import Acoes, Fiis, Bdrs, Criptos, RendasFixa, HistoricoCompra, HistoricoDividendo
from apps.investimentos.models import AcoesConsolidadas, FiisConsolidadas, BdrsConsolidadas, CriptosConsolidadas
from apps.investimentos.forms import AcoesForm, FiisForm, BdrsForm, CriptosForm, RendaFixaForm, DividendoForm
from apps.investimentos.forms import OpcoesAcoes, OpcoesBdrs, OpcoesCriptos, OpcoesFiis, OpcoesRendaFixa
from django.shortcuts import render, redirect, get_object_or_404
from apps.rendas_gastos.utils import check_authentication
from django.core.paginator import Paginator
from decimal import Decimal, ROUND_DOWN
from collections import defaultdict
from django.contrib import messages
from django.db.models import Sum
import yfinance

#Responsável pela página das ações.
def acoes(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form_invest(request, AcoesForm, Acoes, 'Ação registrada com sucesso!')
    context_view, acoes_cadastradas, invest_ticker_dict = investimento_view(request, Acoes)
    total_acoes = acoes_cadastradas.aggregate(total=Sum('valor'))['total']
    categorias = OpcoesAcoes.choices
    grafico = graph(categorias, acoes_cadastradas)
    acoes_cadastradas = acoes_cadastradas.order_by('-data')
    paginator = Paginator(acoes_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tickers_consolidados,  tickers_consolidados_total= import_ativos(request, AcoesConsolidadas, Acoes)
    context = {
        'form': form,
        'acoes_cadastradas': acoes_cadastradas,
        'total_acoes': total_acoes,
        'opcoes_acoes': OpcoesAcoes.choices,
        'page_obj': page_obj,
        'context_view': context_view,
        'grafico': grafico,
        'invest_ticker_dict': invest_ticker_dict,
        'tickers_consolidados': tickers_consolidados,
        'tickers_consolidados_total': tickers_consolidados_total
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
    total_fiis = fiis_cadastrados.aggregate(total=Sum('valor'))['total']
    categorias = OpcoesFiis.choices
    grafico = graph(categorias, fiis_cadastrados)
    fiis_cadastrados = fiis_cadastrados.order_by('-data')
    paginator = Paginator(fiis_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tickers_consolidados, tickers_consolidados_total = import_ativos(request, FiisConsolidadas, Fiis)
    context = {
        'form': form,
        'fiis_cadastrados': fiis_cadastrados,
        'total_fiis': total_fiis,
        'opcoes_fiis': OpcoesFiis.choices,
        'page_obj': page_obj,
        'context_view': context_view,
        'grafico': grafico,
        'invest_ticker_dict': invest_ticker_dict,
        'tickers_consolidados': tickers_consolidados,
        'tickers_consolidados_total': tickers_consolidados_total
    }
    return render(request, 'investimentos/fiis.html', context)

#Responsável pela página das BDRs.
def bdrs(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form_invest(request, BdrsForm, Bdrs, 'BDR registrado com sucesso!')
    context_view, bdrs_cadastrados, invest_ticker_dict = investimento_view(request, Bdrs)
    total_bdrs = bdrs_cadastrados.aggregate(total=Sum('valor'))['total']
    categorias = OpcoesBdrs.choices
    grafico = graph(categorias, bdrs_cadastrados)
    bdrs_cadastrados = bdrs_cadastrados.order_by('-data')
    paginator = Paginator(bdrs_cadastrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tickers_consolidados, tickers_consolidados_total = import_ativos(request, BdrsConsolidadas, Bdrs)
    context = {
        'form': form,
        'bdrs_cadastrados': bdrs_cadastrados,
        'total_bdrs': total_bdrs,
        'opcoes_bdrs': OpcoesBdrs.choices,
        'page_obj': page_obj,
        'context_view': context_view,
        'grafico': grafico,
        'invest_ticker_dict': invest_ticker_dict,
        'tickers_consolidados': tickers_consolidados,
        'tickers_consolidados_total': tickers_consolidados_total
    }
    return render(request, 'investimentos/bdrs.html', context)

#Responsável pela página das cripto moedas.
def criptos(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form_invest(request, CriptosForm, Criptos, 'Cripto moeda registrada com sucesso!')
    context_view, criptos_cadastradas, invest_ticker_dict = investimento_view(request, Criptos)
    total_criptos = criptos_cadastradas.aggregate(total=Sum('valor'))['total']
    categorias = OpcoesCriptos.choices
    grafico = graph(categorias, criptos_cadastradas)
    criptos_cadastradas = criptos_cadastradas.order_by('-data')
    paginator = Paginator(criptos_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tickers_consolidados, tickers_consolidados_total = import_ativos(request, CriptosConsolidadas, Criptos)
    context = {
        'form': form,
        'criptos_cadastradas': criptos_cadastradas,
        'total_criptos': total_criptos,
        'opcoes_criptos': OpcoesCriptos.choices,
        'page_obj': page_obj,
        'context_view': context_view,
        'grafico': grafico,
        'invest_ticker_dict': invest_ticker_dict,
        'tickers_consolidados': tickers_consolidados,
        'tickers_consolidados_total': tickers_consolidados_total
    }
    return render(request, 'investimentos/criptos.html', context)

#Responsável pela página de renda fixa.
def rendafixa(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = process_form_invest(request, RendaFixaForm, RendasFixa, 'Renda fixa registrada com sucesso!')
    context_view, rendasfixa_cadastradas, invest_ticker_dict = investimento_view(request, RendasFixa)
    total_rendasfixa = rendasfixa_cadastradas.aggregate(total=Sum('valor'))['total']
    categorias = OpcoesRendaFixa.choices
    grafico = graph(categorias, rendasfixa_cadastradas)
    rendasfixa_cadastradas = rendasfixa_cadastradas.order_by('-data')
    paginator = Paginator(rendasfixa_cadastradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'rendasfixa_cadastradas': rendasfixa_cadastradas,
        'total_rendasfixa': total_rendasfixa,
        'opcoes_rendasfixa': OpcoesRendaFixa.choices,
        'page_obj': page_obj,
        'context_view': context_view,
        'grafico': grafico,
        'invest_ticker_dict': invest_ticker_dict
    }
    return render(request, 'investimentos/rendafixa.html', context)

def detalhes_ticker(request, tipo_investimento, ticker):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        form = cadastrar_dividendo(request, ticker, tipo_investimento)
    dividendos_cadastrados = HistoricoDividendo.objects.filter(created_by=request.user, ticker=ticker)
    compras_cadastradas = HistoricoCompra.objects.filter(created_by=request.user, ticker=ticker)
    dividendos_cadastrados = dividendos_cadastrados.order_by('-data')
    somados_por_mes = dividendos_por_mes(dividendos_cadastrados)
    compras_cadastradas = compras_cadastradas.order_by('-data')
    somados_compras_por_mes = compras_por_mes(compras_cadastradas)
    paginator = Paginator(dividendos_cadastrados, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_div = dividendos_cadastrados.aggregate(total=Sum('valor'))['total']
    total_compra = compras_cadastradas.aggregate(total=Sum('valor'))['total']
    context = {
        'tipo_investimento': tipo_investimento,
        'ticker': ticker,
        'form': form,
        'somados_por_mes': somados_por_mes,
        'somados_compras_por_mes': somados_compras_por_mes,
        'page_obj': page_obj,
        'total_div': total_div,
        'total_compra': total_compra
    }
    return render(request, 'investimentos/ticker.html', context)

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
            ja_cadastrado = created_class.objects.filter(ticker=ticker, created_by=request.user).first()
            if ja_cadastrado:
                ja_cadastrado.valor += valor_total
                ja_cadastrado.quantidade += quantidade
                ja_cadastrado.preco_medio = ((ja_cadastrado.valor)/ja_cadastrado.quantidade)
                if data > ja_cadastrado.data: ja_cadastrado.data = data
                ja_cadastrado.save(user=request.user)
                historico_compra = HistoricoCompra.objects.create(ticker=ticker, valor=valor_total, quantidade=quantidade,
                                                    data=data, created_by=request.user)
                historico_compra.save()
                messages.success(request, f'Compra do {ticker} adicionada.')
            else:
                novo = created_class.objects.create(ticker=ticker, valor=valor_total, quantidade=quantidade,
                                                    preco_medio=preco_medio, data=data,
                                                    categoria=categoria, created_by=request.user)
                novo.save(user=request.user)
                historico_compra = HistoricoCompra.objects.create(ticker=ticker, valor=valor_total, quantidade=quantidade,
                                                    data=data, created_by=request.user)
                historico_compra.save()
                messages.success(request, success_message)
    form = form_class()
    return form

def cadastrar_dividendo(request, ticker, tipo_investimento):
    if request.method == 'POST':
        form = DividendoForm(request.POST)
        if form.is_valid():
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
        if tipo_investimento == 'fiis':
            ativo_cadastrado = Fiis.objects.filter(ticker=ticker, created_by=request.user).first()
            ativo_cadastrado.dividendo = ativo_cadastrado.dividendo + valor
            ativo_cadastrado.save(user=request.user)
    else:
        form = DividendoForm()
    return form

#Função calcula os valores que foram investidos, recebidos e somados de cada ativo financeiro.
def investimentos_total_view(request):
    investido_acoes_user = Acoes.objects.filter(created_by=request.user)
    investido_acoes = round(sum(float(acao.valor) for acao in investido_acoes_user), 2)
    dividendo_acoes = round(sum(float(acao.dividendo) for acao in investido_acoes_user), 2)
    total_acoes = round(investido_acoes + dividendo_acoes, 2)
    investido_fiis_user = Fiis.objects.filter(created_by=request.user)
    investido_fiis = round(sum(float(fii.valor) for fii in investido_fiis_user), 2)
    dividendo_fiis = round(sum(float(fii.dividendo) for fii in investido_fiis_user), 2)
    total_fiis = round(investido_fiis + dividendo_fiis, 2)
    investido_bdrs_user = Bdrs.objects.filter(created_by=request.user)
    investido_bdrs = round(sum(float(bdr.valor) for bdr in investido_bdrs_user), 2)
    dividendo_bdrs = round(sum(float(bdr.dividendo) for bdr in investido_bdrs_user), 2)
    total_bdrs = round(investido_bdrs + dividendo_bdrs, 2)
    investido_criptos_user = Criptos.objects.filter(created_by=request.user)
    dividendo_criptos = 0
    for ticker in investido_criptos_user:
        cotacao_consolidada = CriptosConsolidadas.objects.filter(ticker=ticker)
        if cotacao_consolidada is not None:
            valor_reais = round(float(cotacao_consolidada.preco_medio) * float(cotacao_consolidada.dividendo), 2)
        else:
            valor_reais = round(float(ticker.preco_medio) * float(ticker.dividendo), 2)
        dividendo_criptos += valor_reais
    investido_criptos = round(sum(float(cripto.valor) for cripto in investido_criptos_user), 2)
    total_criptos = round(investido_criptos + dividendo_criptos, 2)
    investido_rendasfixa_user = RendasFixa.objects.filter(created_by=request.user)
    investido_rendasfixa = round(sum(float(rendafixa.valor) for rendafixa in investido_rendasfixa_user), 2)
    dividendo_rendasfixa = round(sum(float(rendafixa.dividendo) for rendafixa in investido_rendasfixa_user), 2)
    total_rendasfixa = round(investido_rendasfixa + dividendo_rendasfixa, 2)
    investido_acoes_consolidado_user = AcoesConsolidadas.objects.filter(created_by=request.user)
    investido_acoes_consolidado = round(sum(float(acao.valor) * float(acao.quantidade) for acao in investido_acoes_consolidado_user), 2)
    investido_fiis_consolidado_user = FiisConsolidadas.objects.filter(created_by=request.user)
    investido_fiis_consolidado = round(sum(float(fii.valor) * float(fii.quantidade) for fii in investido_fiis_consolidado_user), 2)
    investido_bdrs_consolidado_user = BdrsConsolidadas.objects.filter(created_by=request.user)
    investido_bdrs_consolidado = round(sum(float(bdr.valor) * float(bdr.quantidade) for bdr in investido_bdrs_consolidado_user), 2)
    investido_criptos_consolidado_user = CriptosConsolidadas.objects.filter(created_by=request.user)
    investido_criptos_consolidado = round(sum(float(cripto.valor) * float(cripto.quantidade) for cripto in investido_criptos_consolidado_user), 2)
    lucro_acao = round((investido_acoes_consolidado - investido_acoes) + dividendo_acoes, 2)
    lucro_fii = round((investido_fiis_consolidado - investido_fiis) + dividendo_fiis, 2)
    lucro_bdr = round((investido_bdrs_consolidado - investido_bdrs) + dividendo_bdrs, 2)
    lucro_cripto = round((investido_criptos_consolidado - investido_criptos) + dividendo_criptos, 2)
    total_lucro = round((lucro_acao + lucro_fii + lucro_bdr + lucro_cripto), 2)
    total_dividendos = round(dividendo_acoes + dividendo_fiis + dividendo_bdrs + dividendo_criptos, 2)
    total_comprado = round((investido_acoes + investido_fiis + investido_bdrs + investido_criptos), 2)
    total_consolidado = round((investido_acoes_consolidado + investido_fiis_consolidado + investido_bdrs_consolidado + investido_criptos_consolidado), 2)
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
        'total_consolidado': total_consolidado
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

def dividendos_por_mes(dividendos_cadastrados):
    totais_por_mes = defaultdict(float)
    for dividendo in dividendos_cadastrados:
        mes_ano = dividendo.data.strftime('%Y-%m')
        total_mes = float(dividendo.valor)
        totais_por_mes[mes_ano] += total_mes
    totais_dict_ordenado = {k: round(v, 2) for k, v in sorted(totais_por_mes.items(), key=lambda item: item[0])}
    return totais_dict_ordenado

def compras_por_mes(compras_cadastradas):
    totais_por_mes = defaultdict(float)
    for valor in compras_cadastradas:
        mes_ano = valor.data.strftime('%Y-%m')
        total_mes = float(valor.valor)
        totais_por_mes[mes_ano] += total_mes
    totais_dict_ordenado = {k: round(v, 2) for k, v in sorted(totais_por_mes.items(), key=lambda item: item[0])}
    return totais_dict_ordenado

def consolidar_carteira(request):
    if request.method == 'POST':
        cotacoes = {}
        investido_acoes = Acoes.objects.filter(created_by=request.user)
        investido_fiis = Fiis.objects.filter(created_by=request.user)
        investido_bdrs = Bdrs.objects.filter(created_by=request.user)
        investido_criptos = Criptos.objects.filter(created_by=request.user)
        dados_acoes = defaultdict(list)
        dados_fiis = defaultdict(list)
        dados_bdrs = defaultdict(list)
        dados_criptos = defaultdict(list)
        acoes = Acoes.objects.values('ticker', 'quantidade', 'preco_medio', 'dividendo')
        fiis = Fiis.objects.values('ticker', 'quantidade', 'preco_medio', 'dividendo')
        bdrs = Bdrs.objects.values('ticker', 'quantidade', 'preco_medio', 'dividendo')
        criptos = Criptos.objects.values('ticker', 'quantidade', 'preco_medio', 'dividendo')
        Valores_acoes = preencher_dicionario(dados_acoes, acoes)
        Valores_fiis = preencher_dicionario(dados_fiis, fiis)
        Valores_bdrs = preencher_dicionario(dados_bdrs, bdrs)
        Valores_criptos = preencher_dicionario(dados_criptos, criptos)
        ticker_acoes = [str(item).split('=')[1][:-1] for item in investido_acoes]
        ticker_fiis = [str(item).split('=')[1][:-1] for item in investido_fiis]
        ticker_bdrs = [str(item).split('=')[1][:-1] for item in investido_bdrs]
        ticker_criptos = [str(item).split('=')[1][:-1] for item in investido_criptos]
        tickers_acoes = [ticker + ".SA" for ticker in ticker_acoes]
        tickers_fiis = [ticker + ".SA" for ticker in ticker_fiis]
        tickers_bdrs = [ticker + ".SA" for ticker in ticker_bdrs]
        tickers_criptos = [ticker + "-USD" for ticker in ticker_criptos]
        cotacoes_acoes = obter_cotacao(request, tickers_acoes, cotacoes, AcoesConsolidadas)
        cotacoes_acoes_unido = unir_dados(cotacoes_acoes, Valores_acoes)
        cotacoes = {}
        cotacoes_fiis = obter_cotacao(request, tickers_fiis, cotacoes, FiisConsolidadas)
        cotacoes_fiis_unido = unir_dados(cotacoes_fiis, Valores_fiis)
        cotacoes = {}
        cotacoes_bdrs = obter_cotacao(request, tickers_bdrs, cotacoes, BdrsConsolidadas)
        cotacoes_bdrs_unido = unir_dados(cotacoes_bdrs, Valores_bdrs)
        cotacoes = {}
        cotacoes_criptos = obter_cotacao_cripto(request, tickers_criptos, cotacoes, CriptosConsolidadas)
        cotacoes_criptos_unido = unir_dados(cotacoes_criptos, Valores_criptos)
        salvar_consolidacao(request, cotacoes_acoes_unido, AcoesConsolidadas)
        salvar_consolidacao(request, cotacoes_fiis_unido, FiisConsolidadas)
        salvar_consolidacao(request, cotacoes_bdrs_unido, BdrsConsolidadas)
        salvar_consolidacao(request, cotacoes_criptos_unido, CriptosConsolidadas)
    return redirect('index')
    
def obter_cotacao(request, tickers, cotacoes, class_name):
    for ticker in tickers:
        try:
            valor = yfinance.Ticker(ticker)
            cotacoes[ticker] = valor.info["regularMarketPreviousClose"]
        except Exception as e:
            cotacao_consolidada = class_name.objects.filter(ticker=ticker, created_by=request.user).first()
            cotacao_salva = cotacao_consolidada.valor
            if cotacao_salva:
                cotacoes[ticker] = cotacao_salva
            else:
                cotacoes[ticker] = 0
        cotacoes = {chave.replace(".SA", ""): valor for chave, valor in cotacoes.items()}
    return cotacoes

def obter_cotacao_cripto(request, tickers, cotacoes, class_name):
    cotacao_dolar = yfinance.Ticker("USDBRL=X")
    historico = cotacao_dolar.history(period="1d")
    cotacao_dolar = historico["Close"].iloc[-1]
    cotacao_dolar = round(cotacao_dolar, 2)
    for ticker in tickers:
        try:
            valor = yfinance.Ticker(ticker)
            cotacoes[ticker] = valor.info["regularMarketPreviousClose"]*cotacao_dolar
        except Exception as e:
            cotacao_consolidada = class_name.objects.filter(ticker=ticker, created_by=request.user).first()
            cotacao_salva = cotacao_consolidada.valor
            if cotacao_salva:
                cotacoes[ticker] = cotacao_salva
            else:
                cotacoes[ticker] = 0
        cotacoes = {chave.replace("-USD", ""): valor for chave, valor in cotacoes.items()}
    return cotacoes

def preencher_dicionario(dados, lista):
    for item in lista:
        ticker = item['ticker']
        quantidade = item['quantidade']
        preco_medio = item['preco_medio']
        dividendo = item['dividendo']
        dados[ticker].append(quantidade)
        dados[ticker].append(preco_medio)
        dados[ticker].append(dividendo)
    return dados

def unir_dados(cotacoes, lista):
    tabela_tickers = {}
    for ticker, valor in cotacoes.items():
        if ticker in lista:
            preco_medio = Decimal(lista[ticker][1])
            quantidade = lista[ticker][0]
            valor_atual = Decimal(valor)
            lucro = (valor_atual * quantidade) - (preco_medio * quantidade)
            valor_atual = valor_atual.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
            lucro = lucro.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
            lista[ticker].append(valor_atual)
            lista[ticker].append(lucro)
    for ticker, valores in lista.items():
        tabela_tickers[ticker] = {
            'quantidade': valores[0],
            'preco_medio': valores[1],
            'dividendo': valores[2],
            'valor': valores[3],
            'lucro': valores[4],
        }
    return tabela_tickers

def salvar_consolidacao(request, consolidar, class_name):
    if consolidar:
        dados_existentes = class_name.objects.filter(created_by=request.user)
        if dados_existentes:
            dados_existentes.delete()
        for ticker, dados in consolidar.items():
            consolidado = class_name.objects.create(
                ticker=ticker,
                quantidade=dados['quantidade'],
                preco_medio=dados['preco_medio'],
                dividendo=dados['dividendo'],
                valor=dados['valor'],
                lucro=dados['lucro'],
                created_by=request.user
            )
            consolidado.save(user=request.user)

def import_ativos(request, db, class_name):
    ativos = db.objects.all()
    dicionario_tabela = {}
    dicionario_tabela_total = {}
    total_valor = 0
    total_preco_medio = 0
    total_dividendos = 0
    total_lucro = 0
    for ativo in ativos:
        ticker = ativo.ticker
        valor = ativo.valor
        quantidade = ativo.quantidade
        dividendo = ativo.dividendo
        preco_medio = ativo.preco_medio
        ativo_class = class_name.objects.filter(ticker=ticker, created_by=request.user).first()
        dividendo_ticker = ativo_class.dividendo
        lucro = ativo.lucro + dividendo_ticker
        dados_ativo = {
            'valor': valor,
            'quantidade': quantidade,
            'dividendo': dividendo,
            'preco_medio': preco_medio,
            'lucro': lucro
        }
        total_valor += valor
        total_preco_medio += preco_medio
        total_dividendos += dividendo
        total_lucro += lucro
        dicionario_tabela[ticker] = dados_ativo
    dicionario_tabela_total['total_valor'] = total_valor
    dicionario_tabela_total['total_preco_medio'] = total_preco_medio
    dicionario_tabela_total['total_dividendos'] = total_dividendos
    dicionario_tabela_total['total_lucro'] = total_lucro
    return dicionario_tabela, dicionario_tabela_total

#Função para deletar uma ação.
def delete_acao(request, acao_id):
    acao = get_object_or_404(Acoes, pk=acao_id)
    ticker = acao.ticker
    acao.delete()
    historico_delete = HistoricoCompra.objects.filter(ticker=ticker)
    historico_delete.delete()
    dividendos_delete = HistoricoDividendo.objects.filter(ticker=ticker)
    dividendos_delete.delete()
    messages.success(request, 'Ação deletada com sucesso!')
    return redirect('acoes')

#Função para deletar um fundo imobiliário.
def delete_fii(request, fii_id):
    fii = get_object_or_404(Fiis, pk=fii_id)
    ticker = fii.ticker
    fii.delete()
    historico_delete = HistoricoCompra.objects.filter(ticker=ticker)
    historico_delete.delete()
    dividendos_delete = HistoricoDividendo.objects.filter(ticker=ticker)
    dividendos_delete.delete()
    messages.success(request, 'Fundo imobiliário deletado com sucesso!')
    return redirect('fiis')

#Função para deletar um BDR.
def delete_bdr(request, bdr_id):
    bdr = get_object_or_404(Bdrs, pk=bdr_id)
    ticker = bdr.ticker
    bdr.delete()
    historico_delete = HistoricoCompra.objects.filter(ticker=ticker)
    historico_delete.delete()
    dividendos_delete = HistoricoDividendo.objects.filter(ticker=ticker)
    dividendos_delete.delete()
    messages.success(request, 'BDR deletado com sucesso!')
    return redirect('bdrs')

#Função para deletar uma cripto moeda.
def delete_cripto(request, cripto_id):
    cripto = get_object_or_404(Criptos, pk=cripto_id)
    ticker = cripto.ticker
    cripto.delete()
    historico_delete = HistoricoCompra.objects.filter(ticker=ticker)
    historico_delete.delete()
    dividendos_delete = HistoricoDividendo.objects.filter(ticker=ticker)
    dividendos_delete.delete()
    messages.success(request, 'Cripto moeda deletada com sucesso!')
    return redirect('criptos')

#Função para deletar uma renda fixa.
def delete_rendafixa(request, rendafixa_id):
    rendafixa = get_object_or_404(RendasFixa, pk=rendafixa_id)
    rendafixa.delete()
    messages.success(request, 'Renda fixa deletada com sucesso!')
    return redirect('rendasfixa')

def delete_div(request, tipo_investimento, ticker, div_id,):
    dividendo = get_object_or_404(HistoricoDividendo, pk=div_id)
    dividendo.delete()
    messages.success(request, 'Dividendo deletado com sucesso!')
    return redirect('detalhes_ticker', tipo_investimento, ticker)