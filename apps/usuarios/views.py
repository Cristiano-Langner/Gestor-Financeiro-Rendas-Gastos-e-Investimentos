from apps.usuarios.forms import LoginForms, CadastroForms, TrocaSenhaForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth

#Responsável pela página de login.
def login(request):
    form = LoginForms()
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            nome = form['nome_login'].value()
            senha = form['senha'].value()
        usuario = auth.authenticate(
            request,
            username=nome,
            password=senha
        )
        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, f'{nome} logado(a) com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Erro ao efetuar login')
            return redirect('login')
    return render(request, 'usuarios/login.html', {'form': form})

#Responsável pela página de cadastro.
def cadastro(request):
    form = CadastroForms()
    if request.method == 'POST':
        form = CadastroForms(request.POST)
        if form.is_valid():
            nome=form['nome_cadastro'].value()
            email=form['email'].value()
            senha=form['senha_1'].value()
            if User.objects.filter(username=nome).exists():
                messages.error(request, 'Usuário já existente')
                return redirect('cadastro')
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            usuario.save()
            messages.success(request, 'Cadastro efetuado com sucesso!')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Erro no campo "{form.fields[field].label}": {error}')
    return render(request, 'usuarios/cadastro.html', {'form': form})

#Efetua o logoutd do usuário.
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect('login')

#Responsável pela página de configurações.
@login_required(login_url='login')
def config(request):
    if request.method == 'POST':
        form = TrocaSenhaForm(request.POST)
        if form.is_valid():
            senha_atual = form.cleaned_data['senha_atual']
            nova_senha_1 = form.cleaned_data['nova_senha_1']
            nova_senha_2 = form.cleaned_data['nova_senha_2']
            if request.user.check_password(senha_atual) and nova_senha_1 == nova_senha_2:
                request.user.set_password(nova_senha_1)
                request.user.save()
                messages.success(request, 'Senha alterada com sucesso!')
                return redirect('config')
            else:
                messages.error(request, 'Erro. Verifique se a senha atual esta correta ou se a senha nova esta idêntica.')
    else:
        form = TrocaSenhaForm()
    perguntas_respostas = [
        {"pergunta": "O que estou vendo na página inicial?", "resposta": "Na página inicial você poderá conferir o resumo de suas rendas, gastos e dos seus investimentos através de tabelas e gráficos."},
        {"pergunta": "Para que serve o botão Consolidar Carteira na página inicial?", "resposta": "Serve para buscar os dados dos ativos dos seus investimentos cadastrados através do Yahoo Finance."},
        {"pergunta": "Como eu sei qual ticker colocar para o investimento?", "resposta": "O nome do ticker é para ser o mesmo nome utilizado para as negociações do ativo, em caso de dúvida pesquise na internet o nome do ticker do seu ativo em questão."},
        {"pergunta": "A consolidação da carteira está demorando muito, o que fazer?", "resposta": "É normal que a consolidação da carteira demore um pouco, mas caso esteja demorando mais que o normal, pode ser devido a alguma instabilidade na comunicação com os dados da Yahoo Finance, nesse caso recomenda-se atualizar a página e tentar novamente mais tarde."},
        {"pergunta": "Consolidei a carteira, mas alguns ou todos os valores estão zerados.", "resposta": "Geralmente isso acontece quando foi impossível obter os dados do servidor do Yahoo Finance, nesse caso recomenda-se tentar mais tarde. Também pode ser algum problema no nome do ticker cadastrado, por favor verifique se o ticker está correto."},
        {"pergunta": "Como funciona o cadastro de rendas e gastos?", "resposta": "No topo da página de rendas e gastos você verá os campos de informações a serem preenchidos, logo abaixo tem um botão de cadastrar renda ou gasto. Basta somente preencher as informações e clicar em cadastrar."},
        {"pergunta": "Como funciona o filtro das rendas e gastos?", "resposta": "O filtro é bem simples, basta apenas escolher o que deseja filtrar e clicar no botão Filtrar, caso queira remover todos os filtros da pesquisa clique em Limpar Filtros."},
    ]
    return render(request, 'usuarios/config.html', {'form': form, 'perguntas_respostas': perguntas_respostas})

#Página de erro 404.
def pagina_erro_404(request):
    return render(request, 'usuarios/404.html', status=404)

#Página de erro 500.
def pagina_erro_500(request):
    return render(request, 'usuarios/500.html', status=500)