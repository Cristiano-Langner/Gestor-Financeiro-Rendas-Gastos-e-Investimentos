from django import forms
from apps.rendas_gastos.models import MetodoPagamento, OpcoesGastos, OpcoesRendas

class BaseRendasGastos(forms.Form):
    valor=forms.DecimalField(
        label='Valor', 
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
    metodo_pagamento = forms.ChoiceField(
        label='Pagamento',
        choices=MetodoPagamento.choices,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
class RendasForm(BaseRendasGastos):
    categoria = forms.ChoiceField(
        label='Categoria',
        choices=OpcoesRendas.choices,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
class GastosForm(BaseRendasGastos):
    categoria = forms.ChoiceField(
        label='Categoria ',
        choices=OpcoesGastos.choices,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )