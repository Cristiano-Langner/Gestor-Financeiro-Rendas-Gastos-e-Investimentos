from apps.investimentos.forms import AcoesForm, FiisForm, BdrsForm, CriptosForm, RendaFixaForm, DividendoForm, CVForm
from apps.investimentos.models import Acoes, Fiis, Bdrs, Criptos, RendasFixa, HistoricoCompra, HistoricoDividendo
from apps.investimentos.forms import OpcoesAcoes, OpcoesBdrs, OpcoesCriptos, OpcoesFiis, OpcoesRendaFixa
from django.shortcuts import render, redirect, get_object_or_404
from apps.rendas_gastos.utils import check_authentication
from django.core.paginator import Paginator
from collections import defaultdict
from django.contrib import messages
from django.db.models import Sum
from decimal import ROUND_DOWN
import yfinance as yf
import datetime

#Responsável pela página das ações.
def acoes(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        if request.method == 'POST':
            veio_rendafixa = False
            process_form_invest(request, AcoesForm, Acoes, 'Ação registrada com sucesso!', veio_rendafixa)
        form = AcoesForm()
        context_view, acoes_cadastradas, invest_ticker_dict = investimento_view(request, Acoes)
        total_acoes = acoes_cadastradas.aggregate(total=Sum('valor'))['total']
        categorias = OpcoesAcoes.choices
        grafico = graph(categorias, acoes_cadastradas)
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
            'grafico': grafico,
            'invest_ticker_dict': invest_ticker_dict
        }
    return render(request, 'investimentos/acoes.html', context)

#Responsável pela página dos fundos imobiliários.
def fiis(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        if request.method == 'POST':
            veio_rendafixa = False
            process_form_invest(request, FiisForm, Fiis, 'Fundo imobiliário registrado com sucesso!', veio_rendafixa)
        form = FiisForm()
        context_view, fiis_cadastrados, invest_ticker_dict = investimento_view(request, Fiis)
        total_fiis = fiis_cadastrados.aggregate(total=Sum('valor'))['total']
        categorias = OpcoesFiis.choices
        grafico = graph(categorias, fiis_cadastrados)
        fiis_cadastrados = fiis_cadastrados.order_by('-data')
        paginator = Paginator(fiis_cadastrados, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'form': form,
            'fiis_cadastrados': fiis_cadastrados,
            'total_fiis': total_fiis,
            'opcoes_fiis': OpcoesFiis.choices,
            'page_obj': page_obj,
            'context_view': context_view,
            'grafico': grafico,
            'invest_ticker_dict': invest_ticker_dict
        }
    return render(request, 'investimentos/fiis.html', context)

#Responsável pela página das BDRs.
def bdrs(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        if request.method == 'POST':
            veio_rendafixa = False
            process_form_invest(request, BdrsForm, Bdrs, 'BDR registrado com sucesso!', veio_rendafixa)
        form = BdrsForm()
        context_view, bdrs_cadastrados, invest_ticker_dict = investimento_view(request, Bdrs)
        total_bdrs = bdrs_cadastrados.aggregate(total=Sum('valor'))['total']
        categorias = OpcoesBdrs.choices
        grafico = graph(categorias, bdrs_cadastrados)
        bdrs_cadastrados = bdrs_cadastrados.order_by('-data')
        paginator = Paginator(bdrs_cadastrados, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'form': form,
            'bdrs_cadastrados': bdrs_cadastrados,
            'total_bdrs': total_bdrs,
            'opcoes_bdrs': OpcoesBdrs.choices,
            'page_obj': page_obj,
            'context_view': context_view,
            'grafico': grafico,
            'invest_ticker_dict': invest_ticker_dict
        }
    return render(request, 'investimentos/bdrs.html', context)

#Responsável pela página das cripto moedas.
def criptos(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        if request.method == 'POST':
            veio_rendafixa = False
            process_form_invest(request, CriptosForm, Criptos, 'Cripto moeda registrada com sucesso!', veio_rendafixa)
        form = CriptosForm()
        context_view, criptos_cadastradas, invest_ticker_dict = investimento_view(request, Criptos)
        total_criptos = criptos_cadastradas.aggregate(total=Sum('valor'))['total']
        categorias = OpcoesCriptos.choices
        grafico = graph(categorias, criptos_cadastradas)
        criptos_cadastradas = criptos_cadastradas.order_by('-data')
        paginator = Paginator(criptos_cadastradas, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'form': form,
            'criptos_cadastradas': criptos_cadastradas,
            'total_criptos': total_criptos,
            'opcoes_criptos': OpcoesCriptos.choices,
            'page_obj': page_obj,
            'context_view': context_view,
            'grafico': grafico,
            'invest_ticker_dict': invest_ticker_dict
        }
    return render(request, 'investimentos/criptos.html', context)

#Responsável pela página de renda fixa.
def rendafixa(request):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        if request.method == 'POST':
            veio_rendafixa = True
            process_form_invest(request, RendaFixaForm, RendasFixa, 'Renda fixa registrada com sucesso!', veio_rendafixa)
        form = RendaFixaForm()
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
        if request.method == 'POST':
            cadastrar_dividendo(request, ticker, tipo_investimento)
            cadastrar_cv(request, ticker, tipo_investimento)
        form = DividendoForm()
        form_cv = CVForm()
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

#Função que faz a verificação da válidade dos dados, alguns tratamentos de dados e salvamentos das informações.
def process_form_invest(request, form_class, created_class, success_message, origem):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid() and not origem:
            ticker = form.cleaned_data['ticker']
            valor = form.cleaned_data['valor']
            quantidade = form.cleaned_data['quantidade']
            data = form.cleaned_data['data']
            categoria = form.cleaned_data['categoria']
            preco_medio = valor if valor > 0 else 0
            valor_total = valor * quantidade
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

def cadastrar_cv(request, ticker, tipo_investimento):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        if request.method == 'POST':
            form_cv = CVForm(request.POST)
            if form_cv.is_valid():
                valor = form_cv.cleaned_data['valor']
                data = form_cv.cleaned_data['data']
                quantidade = form_cv.cleaned_data['quantidade']
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

def cadastrar_dividendo(request, ticker, tipo_investimento):
    if request.method == 'POST':
        form = DividendoForm(request.POST)
        if form.is_valid() and 'dividendo' in request.POST:
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
            elif tipo_investimento == 'rendasfixa':
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
    investido_rendasfixa_user = RendasFixa.objects.filter(created_by=request.user)
    investido_rendasfixa = round(sum(float(rendafixa.valor) for rendafixa in investido_rendasfixa_user), 2)
    dividendo_rendasfixa = round(sum(float(rendafixa.dividendo) for rendafixa in investido_rendasfixa_user), 2)
    total_rendasfixa = round(investido_rendasfixa + dividendo_rendasfixa, 2)
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
        cotacao_consolidada = Criptos.objects.filter(ticker=ticker)
        if cotacao_consolidada:
            valor_reais = round(float(cotacao_consolidada.preco_medio) * float(cotacao_consolidada.dividendo), 2)
        else:
            valor_reais = round(float(ticker.preco_medio) * float(ticker.dividendo), 2)
        dividendo_criptos += valor_reais
    investido_criptos = round(sum(float(cripto.valor) for cripto in investido_criptos_user), 2)
    total_criptos = round(investido_criptos + dividendo_criptos, 2)
    investido_acoes_consolidado = round(sum(float(acao.valor_mercado) * float(acao.quantidade) for acao in investido_acoes_user), 2)
    investido_fiis_consolidado = round(sum(float(fii.valor_mercado) * float(fii.quantidade) for fii in investido_fiis_user), 2)
    investido_bdrs_consolidado = round(sum(float(bdr.valor_mercado) * float(bdr.quantidade) for bdr in investido_bdrs_user), 2)
    investido_criptos_consolidado = round(sum(float(cripto.valor_mercado) * float(cripto.quantidade) for cripto in investido_criptos_user), 2)
    lucro_acao = round((investido_acoes_consolidado - investido_acoes) + dividendo_acoes, 2)
    lucro_fii = round((investido_fiis_consolidado - investido_fiis) + dividendo_fiis, 2)
    lucro_bdr = round((investido_bdrs_consolidado - investido_bdrs) + dividendo_bdrs, 2)
    lucro_cripto = round((investido_criptos_consolidado - investido_criptos) + dividendo_criptos, 2)
    total_lucro = round((dividendo_rendasfixa + lucro_acao + lucro_fii + lucro_bdr + lucro_cripto), 2)
    total_dividendos = round(dividendo_rendasfixa + dividendo_acoes + dividendo_fiis + dividendo_bdrs + dividendo_criptos, 2)
    total_comprado = round((investido_rendasfixa + investido_acoes + investido_fiis + investido_bdrs + investido_criptos), 2)
    total_consolidado = round((investido_rendasfixa + investido_acoes_consolidado + investido_fiis_consolidado + investido_bdrs_consolidado + investido_criptos_consolidado), 2)
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
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
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
    
def obter_cotacao(request, cotacoes, dados, class_name, data_atual):
    for ticker in dados:
        ticker_temporario = ticker.replace(".SA", "")
        dados_salvos = class_name.objects.filter(ticker=ticker_temporario, created_by=request.user).first()
        if dados_salvos:
            data_inicial = dados_salvos.data
            try:
                dados = yf.download(ticker)
                cotacoes[ticker] = round(dados["Close"][-1], 2)
            except Exception as e:
                print("Erro:", str(e))
    cotacoes = {chave.replace(".SA", ""): valor for chave, valor in cotacoes.items()}
    return cotacoes

def obter_cotacao_cripto(request, cotacoes, dados, class_name, data_atual):
    cotacao_dolar = yf.download("BRL=X")
    cotacao_dolar = round(cotacao_dolar["Close"][-1], 2)
    print(cotacao_dolar)
    for ticker in dados:
        ticker_temporario = ticker.replace("-USD", "")
        dados_salvos = class_name.objects.filter(ticker=ticker_temporario, created_by=request.user).first()
        if dados_salvos:
            data_inicial = dados_salvos.data
            try:
                dados = yf.download(ticker)
                cotacoes[ticker] = (round(dados["Close"][-1], 2)) * cotacao_dolar
            except Exception as e:
                print("Erro:", str(e))
    cotacoes = {chave.replace("-USD", ""): valor for chave, valor in cotacoes.items()}
    return cotacoes

def salvar_consolidacao(request, dados, class_name):
    for ticker, cotacao in dados.items():
        investimento = class_name.objects.filter(ticker=ticker, created_by=request.user).first()
        if investimento:
            quantidade = investimento.quantidade
            investimento.valor_mercado = cotacao
            investimento.valor_total_mercado = cotacao * quantidade
            investimento.save(user=request.user)

#Função para deletar um investimento.
def delete_investimento(request, tipo_investimento, invest_id):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
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

def delete_div(request, tipo_investimento, ticker, div_id,):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        dividendo = get_object_or_404(HistoricoDividendo, pk=div_id)
        dividendo.delete()
        messages.success(request, 'Dividendo deletado com sucesso!')
        return redirect('detalhes_ticker', tipo_investimento, ticker)

def delete_cv(request, tipo_investimento, ticker, cv_id,):
    if not check_authentication(request):
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    else:
        cv = get_object_or_404(HistoricoCompra, pk=cv_id)
        cv.delete()
        messages.success(request, 'Compra/venda deletada com sucesso!')
        return redirect('detalhes_ticker', tipo_investimento, ticker)