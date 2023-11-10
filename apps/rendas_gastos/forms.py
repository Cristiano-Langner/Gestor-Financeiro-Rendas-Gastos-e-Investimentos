from apps.rendas_gastos.models import MetodoPagamento, OpcoesGastos, OpcoesRendas, Rendas, Gastos
from django import forms

class BaseRendasGastos(forms.ModelForm):
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
    class Meta:
        abstract = True
    
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
    descricao = forms.CharField(
        label='Descrição',
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite informação',
            }
        )
    )
    class Meta:
        model = Rendas
        fields = '__all__'
    
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
    descricao = forms.CharField(
        label='Descrição',
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite informação',
            }
        )
    )
    class Meta:
        model = Gastos
        fields = '__all__'