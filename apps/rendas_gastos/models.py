from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from decimal import Decimal

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
    VA_VR = "VA_VR"
    FREELA = "Freela"
    VENDA_ATIVOS = "Venda ativos"
    CASHBACK = "Cashback"
    OUTROS = "Outros"
    
class OpcoesGastos(models.TextChoices):
    ÁGUA = "Água"
    ALUGUEL = "Aluguel"
    ASSINATURAS = "Assinaturas"
    CARRO = "Carro"
    CASA = "Casa"
    CELULAR = "Celular"
    DOAÇÕES = "Doações"
    EDUCAÇÃO = "Educação"
    GÁS = "Gás"
    GASOLINA = "Gasolina"
    INVESTIMENTOS = "Investimentos"
    INTERNET = "Internet"
    LANCHES = "Lanches"
    LUZ = "Luz"
    MERCADO = "Mercado"
    PET = "Pet"
    PRESENTE = "Presente"
    RESTAURANTE = "Restaurante"
    SAÚDE = "Saúde"
    SEGUROS = "Seguros"
    TRANSPORTE = "Transporte"
    Vestuário = "Vestuário"
    VIAGENS = "Viagens"
    OUTROS = "Outros"
    
class BaseTransaction(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    data = models.DateField(null=False, blank=False, default=timezone.now)
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