# Gestor Financeiro - Rendas, Gastos e Investimentos

Este projeto oferece aos usuários a capacidade de registrar suas receitas, despesas e investimentos em ações, BDRs, fundos imobiliários e criptomoedas. Ele fornece uma visão abrangente das finanças do usuário por meio de gráficos e tabelas informativas. Todo o aplicativo foi desenvolvido com a poderosa estrutura Django, abrangendo tanto o desenvolvimento do backend quanto do frontend, garantindo uma experiência completa e eficiente.

Sinta-se a vontade em utilizar e fazer suas próprias melhorias. É um projeto que pretendo continuar atualizando e melhorando com o tempo. Espero que aproveite!

## Instalação

1. Certifique-se de ter o Python 3.11 ou uma versão superior instalado em seu sistema.

2. Crie um ambiente virtual (opcional, mas recomendado) e após habilite o ambiente de acordo com seu sitema operacional:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows

3. Instale as dependências do projeto usando 'pip':
    ```bash
    pip install -r requirements.txt

4. Crie as tabelas que representam os modelos do aplicativo:
    ```bash
    python manage.py makemigrations

5. Faça as migrações do banco de dados:
    ```bash
    python manage.py migrate

6. É preciso coletar os arquivos estáticos para que o django possa usá-los, use o comando abaixo e confirme digitando "yes" quando solicitado:
    ```bash
    python manage.py collectstatic

7. Agora será necessário criar o usuário. Insira o nome, email (não precisa ser real) e a senha. Caso apareça alguma mensagem de senha muito fraca ou muito parecida com o nome de usuário é só escolher "Y" ou mudar a senha a seu gosto:
    ```bash
    python manage.py createsuperuser

## Uso

Execute o comando abaixo para iniciar o servidor. Em seguida acesse o aplicativo pelo link que irá aparecer no terminal:
   ```bash
    python manage.py runserver
