from django.db import models
from decimal import Decimal
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.core.validators import MinValueValidator, MaxValueValidator

class MetodoPagamento(models.TextChoices):
    DEPOSITO = "Depósito"
    DINHEIRO = "Dinheiro"
    DEBITO = "Débito"
    CREDITO = "Crédito"
    PIX = "Pix"
    OUTROS = "Outros"
    
class OpcoesRendas(models.TextChoices):
    SALARIO = "Salário"
    ACOES = "Ações"
    BDRS = "BDRs"
    FIIS = "FIIs"
    OUTROS = "Outros"
    
class OpcoesGastos(models.TextChoices):
    ALUGUEL = "Aluguel"
    MERCADO ="Mercado"
    LUZ = "Luz"
    ÁGUA = "Água"
    GASOLINA = "Gasolina"
    PET = "Pet"
    LANCHES = "Lanches"
    SAUDE = "Saúde"
    TRANSPORTE = "Transporte"
    EDUCACAO = "Educação"
    ASSINATURAS = "Assinaturas"
    VIAJENS = "Viagens"
    VESTUARIO = "Vestuário"
    INVESTIMENTOS = "Investimentos"
    DOACOES = "Doações"
    CARRO = "Carro"
    IMOVEIS = "Imóveis"
    SEGUROS = "Seguros"
    PRESENTES = "Presentes"
    RESTAURANTES = "Restaurantes"
    CASA = "Casa"
    OUTROS = "Outros"
    
class BaseTransaction(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    descricao = models.TextField(null=False, blank=False, default='')
    data = models.DateField(null=False, blank=False, validators=[MaxValueValidator(date.today())], default=date.today())
    metodo_pagamento = models.CharField(max_length=100, choices=MetodoPagamento.choices, default=MetodoPagamento.OUTROS)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False, related_name='%(class)s_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False, related_name='%(class)s_modified_by')
    
    def save(self, user=None, *args, **kwargs):
        self.created_by = user
        self.modified_by = user
        super().save(*args, **kwargs)
        
    def update_modified_by(self, user=None, *args, **kwargs):
        self.modified_by = user
        super().save(*args, **kwargs)
        

    class Meta:
        abstract = True
        
class Rendas(BaseTransaction):
    categoria = models.CharField(max_length=100, choices=OpcoesRendas.choices, default=OpcoesRendas.OUTROS)
    
    def __str__(self):
        return f"Rendas [descricao={self.descricao}]"
    class Meta:
        verbose_name_plural = "Rendas"
        
class Gastos(BaseTransaction):
    categoria = models.CharField(max_length=100, choices=OpcoesGastos.choices, default=OpcoesGastos.OUTROS)
    
    def __str__(self):
        return f"Gastos [descricao={self.descricao}]"
    class Meta:
        verbose_name_plural = "Gastos"