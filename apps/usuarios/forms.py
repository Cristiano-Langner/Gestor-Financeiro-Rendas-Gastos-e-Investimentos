from django.core.validators import MaxLengthValidator
from django import forms

class LoginForms(forms.Form):
    nome_login=forms.CharField(
        label='Nome de Login', 
        required=True, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: João Silva',
            }
        )
    )
    senha=forms.CharField(
        label='Senha', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sua senha',
            }
        ),
    )

class CadastroForms(forms.Form):
    nome_cadastro=forms.CharField(
        label='Nome', 
        required=True, 
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: João Silva',
            }
        ),
        validators=[
            MaxLengthValidator(limit_value=100, message='O nome não pode ter mais de 20 caracteres'),
        ]
    )
    email=forms.EmailField(
        label='Email',
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: joaosilva@xpto.com',
            }
        )
    )
    senha_1=forms.CharField(
        label='Senha', 
        required=True, 
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sua senha',
            }
        ),
        validators=[
            MaxLengthValidator(limit_value=70, message='A senha não pode ter mais de 50 caracteres'),
        ]
    )
    senha_2=forms.CharField(
        label='Confirme a sua senha', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sua senha novamente',
            }
        ),
    )

    def clean_nome_cadastro(self):
        nome = self.cleaned_data.get('nome_cadastro')
        if nome and ' ' in nome:
            raise forms.ValidationError('Espaços não são permitidos nesse campo')
        return nome

    def clean_senha_2(self):
        senha_1 = self.cleaned_data.get('senha_1')
        senha_2 = self.cleaned_data.get('senha_2')
        if senha_1 and senha_2 and senha_1 != senha_2:
            raise forms.ValidationError('As senhas não coincidem')
        if len(senha_1) < 8:
            raise forms.ValidationError('A senha deve conter no mínimo 8 caracteres')
        return senha_2
    
class TrocaSenhaForm(forms.Form):
    senha_atual = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a senha atual',
            }))
    nova_senha_1=forms.CharField(
        label='Nova senha', 
        required=True, 
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a nova senha',
            }
        ),
        validators=[
            MaxLengthValidator(limit_value=70, message='A senha não pode ter mais de 50 caracteres'),
        ]
    )
    nova_senha_2=forms.CharField(
        label='Confirme a nova senha', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a nova senha novamente',
            }
        ),
    )
    
    def clean_nova_senha_2(self):
        nova_senha_1 = self.cleaned_data.get('nova_senha_1')
        nova_senha_2 = self.cleaned_data.get('nova_senha_2')
        if nova_senha_1 and nova_senha_2 and nova_senha_1 != nova_senha_2:
            raise forms.ValidationError('As senhas não coincidem')
        if len(nova_senha_2) < 8:
            raise forms.ValidationError('A senha deve conter no mínimo 8 caracteres')
        return nova_senha_2