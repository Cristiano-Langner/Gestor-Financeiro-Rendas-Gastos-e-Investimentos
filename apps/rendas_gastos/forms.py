from django import forms
from apps.rendas_gastos.models import MetodoPagamento, OpcoesGastos, OpcoesRendas

class BaseRendasGastos(forms.Form):
    valor_renda=forms.DecimalField(
        label='Valor da renda', 
        required=True, 
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: 1000.00',
                'step': '0.01'
            }
        )
    )
    descricao_renda=forms.CharField(
        label='descricao', 
        required=True, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sua descrição',
            }
        ),
    )
    data_renda = forms.DateField(
        label='Data da renda',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: DD/MM/AAAA',
                'type': 'date',
            }
        )
    )
    metodo_pagamento_renda = forms.ChoiceField(
        label='Método de pagamento',
        choices=MetodoPagamento.choices,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
class RendasForm(BaseRendasGastos):
    categoria_renda = forms.ChoiceField(
        label='Categoria da renda',
        choices=OpcoesRendas.choices,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
class GastosForm(BaseRendasGastos):
    categoria_gasto = forms.ChoiceField(
        label='Categoria do gasto',
        choices=OpcoesGastos.choices,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )