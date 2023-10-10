from django import forms
from apps.investimentos.models import OpcoesAcoes, OpcoesBdrs, OpcoesCriptos, OpcoesFiis, OpcoesRendaFixa

class BaseInvestimentos(forms.Form):
    ticker=forms.CharField(
        label='Ticker ',
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
        label='Valor unidade ', 
        required=True,
        max_digits=14,
        decimal_places=8, 
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: 1000.00',
            }
        )
    )
    quantidade = forms.DecimalField(
    label='Quantidade ',
    required=True,
    max_digits=14,
    decimal_places=8,
    widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ex.: 5.00'
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
        label='Categoria ',
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
        label='Categoria ',
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
        label='Categoria ',
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
        label='Categoria ',
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
        label='Categoria ',
        choices=OpcoesRendaFixa.choices,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
class DividendoForm(forms.Form):
    valor = forms.DecimalField(
        label='Valor do Dividendo',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: 10.00',
            }
        )
    )
    data = forms.DateField(
        label='Data do Dividendo',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: DD/MM/AAAA',
                'type': 'date',
            }
        )
    )
    
class VendaForm(forms.Form):
    quantidade = forms.DecimalField(
        label='Quantidade ',
        required=True,
        max_digits=14,
        decimal_places=8,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: 5.00'
            }
        )
    )
    data = forms.DateField(
        label='Data do Dividendo',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: DD/MM/AAAA',
                'type': 'date',
            }
        )
    )