from django.db import models
from decimal import Decimal
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class MetodoPagamento(models.TextChoices):
    DEPÓSITO = "Depósito"
    DINHEIRO = "Dinheiro"
    DÉBITO = "Débito"
    CRÉDITO = "Crédito"
    PIX = "Pix"
    BOLETO = "Boleto"
    OUTROS = "Outros"
    
class OpcoesRendas(models.TextChoices):
    SALÁRIO = "Salário"
    AÇÕES = "Ações"
    BDRS = "BDRs"
    FIIS = "FIIs"
    RENDA_FIXA = "Renda Fixa"
    CASHBACK = "Cashback"
    OUTROS = "Outros"
    
class OpcoesGastos(models.TextChoices):
    ALUGUEL = "Aluguel"
    MERCADO ="Mercado"
    LUZ = "Luz"
    ÁGUA = "Água"
    GASOLINA = "Gasolina"
    PET = "Pet"
    INTERNET = "Internet"
    CELULAR = "Celular"
    LANCHES = "Lanches"
    SAÚDE = "Saúde"
    TRANSPORTE = "Transporte"
    EDUCAÇÃO = "Educação"
    ASSINATURAS = "Assinaturas"
    VIAJENS = "Viagens"
    VESTUÁRIO = "Vestuário"
    INVESTIMENTOS = "Investimentos"
    DOAÇÕES = "Doações"
    CARRO = "Carro"
    SEGUROS = "Seguros"
    RESTAURANTE = "Restaurante"
    CASA = "Casa"
    OUTROS = "Outros"
    
class BaseTransaction(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
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
        return f"Rendas [categoria={self.categoria}]"
    class Meta:
        verbose_name_plural = "Rendas"
        
class Gastos(BaseTransaction):
    categoria = models.CharField(max_length=100, choices=OpcoesGastos.choices, default=OpcoesGastos.OUTROS)
    
    def __str__(self):
        return f"Gastos [categoria={self.categoria}]"
    class Meta:
        verbose_name_plural = "Gastos"