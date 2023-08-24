from django import forms
from apps.investimentos.models import OpcoesAcoes, OpcoesBdrs, OpcoesCriptos, OpcoesFiis, OpcoesRendaFixa

class BaseInvestimentos(forms.Form):
    nome=forms.CharField(
        label='Nome: ', 
        required=True, 
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome',
            }
        ),
    )
    ticker=forms.CharField(
        label='Ticker: ',
        required=True, 
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ticker',
            }
        ),
    )
    valor=forms.DecimalField(
        label='Valor: ', 
        required=True, 
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: 1000.00',
                'step': '0.01'
            }
        )
    )
    quantidade = forms.IntegerField(
        label='Quantidade: ',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: 5'
            }
        )
    )
    dividendo=forms.DecimalField(
        label='Dividendo: ', 
        required=True, 
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: 1000.00',
                'step': '0.01'
            }
        )
    )
    data = forms.DateField(
        label='Data',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: DD/MM/AAAA',
                'type': 'date',
            }
        )
    )
    
class AcoesForm(BaseInvestimentos):
    categoria = forms.ChoiceField(
        label='Categoria: ',
        choices=OpcoesAcoes.choices,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
class FiisForm(BaseInvestimentos):
    categoria = forms.ChoiceField(
        label='Categoria: ',
        choices=OpcoesFiis.choices,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
class BdrsForm(BaseInvestimentos):
    categoria = forms.ChoiceField(
        label='Categoria: ',
        choices=OpcoesBdrs.choices,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
class CriptosForm(BaseInvestimentos):
    categoria = forms.ChoiceField(
        label='Categoria: ',
        choices=OpcoesCriptos.choices,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
class RendaFixaForm(BaseInvestimentos):
    categoria = forms.ChoiceField(
        label='Categoria: ',
        choices=OpcoesRendaFixa.choices,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )