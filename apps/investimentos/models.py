from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from decimal import Decimal
    
class OpcoesAcoes(models.TextChoices):
    ORDINARIAS = "Ordinárias"
    PREFERENCIAIS = "Preferenciais"
    ESPECIAIS = "Especiais"
    OUTROS = "Outros"
    
class OpcoesFiis(models.TextChoices):
    PAPÉIS = "Papéis"
    SHOPPINGS = "Shoppings"
    LAJES_CORPORATIVAS = "Lajes Corporativas"
    GALPÕES_LOGÍSTICOS = "Galpões Logísticos"
    AGRO = "Agro"
    HOTÉIS = "Hotéis"
    EDUCACIONAL = "Educacional"
    HOSPITAIS = "Hospitais"
    AGÊNCIAS_BANCÁRIAS = "Agências Bancárias"
    FUNDOS = "Fundos"
    DESENVOLVIMENTO_IMOBILIÁRIO = "Desenvolvimento Imobiliário"
    RECEBÍVEIS_IMOBILIÁRIOS = "Recebíveis Imobiliários"
    HIBRIDO = "Hibrido"
    OUTROS = "Outros"
    
class OpcoesBdrs(models.TextChoices):
    NÍVEL_1 = "Nível 1"
    NÍVEL_2 = "Nível 2"
    NÍVEL_3 = "Nível 3"
    OUTROS = "Outros"
    
class OpcoesCriptos(models.TextChoices):
    STABLECOIN = "Stablecoin"
    ALTCOIN = "Altcoin"
    DEFI = "Defi"
    PROTOCOL_TOKEN = "Protocol token"
    SECURITY_TOKEN = "Security token"
    GAMING_TOKEN = "Gaming token"
    ENERGY_TOKEN = "Energy token"
    EXCHANGE_TOKEN = "Exchange token"
    UTILITY_TOKEN = "Utility token"
    FAN_TOKEN = "Fan token"
    WEB_3_0 = "Web 3.0"
    PRIVACY_COIN = "Privacy coin"
    OUTROS = "Outros"
    
class OpcoesRendaFixa(models.TextChoices):
    CONTA_REMUNERADA = "Conta Remunerada"
    TESOURO_SELIC = "Tesouro Selic"
    TESOURO_PREFIXADO = "Tesouro Prefixado"
    TESOURO_IPCA = "Tesouro IPCA"
    CDB = "CDB"
    LCI = "LCI"
    LCA = "LCA"
    LC = "LC"
    DEBENTURES = "Debêntures"
    FUNDOS_RF = "Fundos de Renda Fixa"
    CRI = "CRI"
    CRA = "CRA"
    OUTROS = "Outros"
    
class BaseTransaction(models.Model):
    ticker = models.CharField(max_length=10,null=False,blank=False)
    valor_mercado = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_total_mercado = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    quantidade = models.IntegerField(default=0)
    dividendo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    preco_medio = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    data = models.DateField(null=False, blank=False, default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False, related_name='%(class)s_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False, related_name='%(class)s_modified_by')
    def save(self, user=None, *args, **kwargs):
        self.created_by = user
        self.modified_by = user
        super().save(*args, **kwargs)
    def update_modified_by(self, user=None, *args, **kwargs):
        self.modified_by = user
        super().save(*args, **kwargs)
    def clean_ticker(self):
        ticker = self.cleaned_data['ticker']
        return ticker.upper()
    class Meta:
        abstract = True

class Acoes(BaseTransaction):
    categoria = models.CharField(max_length=100, choices=OpcoesAcoes.choices, default=OpcoesAcoes.OUTROS)
    def __str__(self):
        return f"Ações [ticker={self.ticker}]"
    class Meta:
        verbose_name_plural = "Ações"

class Fiis(BaseTransaction):
    categoria = models.CharField(max_length=100, choices=OpcoesFiis.choices, default=OpcoesFiis.OUTROS)
    def __str__(self):
        return f"Fundos Imobiliários [ticker={self.ticker}]"
    class Meta:
        verbose_name_plural = "Fundos Imobiliários"

class Bdrs(BaseTransaction):
    categoria = models.CharField(max_length=100, choices=OpcoesBdrs.choices, default=OpcoesBdrs.OUTROS)
    def __str__(self):
        return f"Brazilian Depositary Receipts [ticker={self.ticker}]"
    class Meta:
        verbose_name_plural = "BDRs"

class Criptos(BaseTransaction):
    valor_mercado = models.DecimalField(max_digits=14, decimal_places=8, default=Decimal('0.00'))
    valor = models.DecimalField(max_digits=14, decimal_places=8, default=Decimal('0.00'))
    quantidade = models.DecimalField(max_digits=14, decimal_places=8, default=0.0)
    dividendo = models.DecimalField(max_digits=14, decimal_places=8, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    preco_medio = models.DecimalField(max_digits=14, decimal_places=8, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    categoria = models.CharField(max_length=100, choices=OpcoesCriptos.choices, default=OpcoesCriptos.OUTROS)
    def __str__(self):
        return f"Criptos [ticker={self.ticker}]"
    class Meta:
        verbose_name_plural = "Criptos"

class RendasFixa(models.Model):
    ticker = models.CharField(max_length=10,null=False,blank=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    dividendo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    data = models.DateField(null=False, blank=False, default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False, related_name='%(class)s_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False, related_name='%(class)s_modified_by')
    categoria = models.CharField(max_length=100, choices=OpcoesRendaFixa.choices, default=OpcoesRendaFixa.OUTROS)
    def __str__(self):
        return f"Renda Fixa [ticker={self.ticker}]"
    class Meta:
        verbose_name_plural = "Renda Fixa"
    def save(self, user=None, *args, **kwargs):
        self.created_by = user
        self.modified_by = user
        super().save(*args, **kwargs)
    def update_modified_by(self, user=None, *args, **kwargs):
        self.modified_by = user
        super().save(*args, **kwargs)
    def clean_ticker(self):
        ticker = self.cleaned_data['ticker']
        return ticker.upper()

class HistoricoCompra(models.Model):
    ticker = models.CharField(max_length=10)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(default=0)
    data = models.DateField(null=False, blank=False, default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False, related_name='%(class)s_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False, related_name='%(class)s_modified_by')
    def __str__(self):
        return f"{self.ticker} - {self.quantidade} - {self.data}"
    
class HistoricoDividendo(models.Model):
    ticker = models.CharField(max_length=10)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(null=False, blank=False, default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False, related_name='%(class)s_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False, related_name='%(class)s_modified_by')
    def __str__(self):
        return f"{self.ticker} - {self.valor} - {self.data}"