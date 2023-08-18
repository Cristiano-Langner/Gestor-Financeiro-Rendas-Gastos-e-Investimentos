from django.contrib import messages

def check_authentication(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return False
    return True