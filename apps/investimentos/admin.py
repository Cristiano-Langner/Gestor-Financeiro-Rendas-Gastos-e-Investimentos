from apps.investimentos.models import Acoes, Fiis, Bdrs, Criptos, RendasFixa, HistoricoCompra, HistoricoDividendo
from apps.investimentos.models import AcoesConsolidadas, FiisConsolidadas, BdrsConsolidadas, CriptosConsolidadas
from django.contrib import admin

class Acao(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'valor', 'quantidade', 'dividendo', 'preco_medio',  'data', 'categoria', 'created_by', 'modified_by')
    list_display_links = ('id', 'ticker')
    search_fields = ('ticker',)
    list_per_page = 20
    
admin.site.register(Acoes, Acao)

class Fii(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'valor', 'quantidade', 'dividendo', 'preco_medio',  'data', 'categoria', 'created_by', 'modified_by')
    list_display_links = ('id', 'ticker')
    search_fields = ('ticker',)
    list_per_page = 20
    
admin.site.register(Fiis, Fii)

class Bdr(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'valor', 'quantidade', 'dividendo', 'preco_medio',  'data', 'categoria', 'created_by', 'modified_by')
    list_display_links = ('id', 'ticker')
    search_fields = ('ticker',)
    list_per_page = 20
    
admin.site.register(Bdrs, Bdr)

class Cripto(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'valor', 'quantidade', 'dividendo', 'preco_medio',  'data', 'categoria', 'created_by', 'modified_by')
    list_display_links = ('id', 'ticker')
    search_fields = ('ticker',)
    list_per_page = 20
    
admin.site.register(Criptos, Cripto)

class RendaFixa(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'valor', 'quantidade', 'dividendo', 'preco_medio',  'data', 'categoria', 'created_by', 'modified_by')
    list_display_links = ('id', 'ticker')
    search_fields = ('ticker',)
    list_per_page = 20
    
admin.site.register(RendasFixa, RendaFixa)

class Historico(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'valor', 'quantidade', 'data', 'created_by', 'modified_by')
    list_display_links = ('id', 'ticker')
    search_fields = ('ticker',)
    list_per_page = 20
    
admin.site.register(HistoricoCompra, Historico)

class HistoricoDiv(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'valor', 'data', 'created_by', 'modified_by')
    list_display_links = ('id', 'ticker')
    search_fields = ('ticker',)
    list_per_page = 20
    
admin.site.register(HistoricoDividendo, HistoricoDiv)

class AcaoConsolidada(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'valor', 'quantidade', 'dividendo', 'preco_medio', 'created_by', 'modified_by')
    list_display_links = ('id', 'ticker')
    search_fields = ('ticker',)
    list_per_page = 20
    
admin.site.register(AcoesConsolidadas, AcaoConsolidada)

class FiiConsolidada(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'valor', 'quantidade', 'dividendo', 'preco_medio', 'created_by', 'modified_by')
    list_display_links = ('id', 'ticker')
    search_fields = ('ticker',)
    list_per_page = 20
    
admin.site.register(FiisConsolidadas, FiiConsolidada)

class BdrConsolidada(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'valor', 'quantidade', 'dividendo', 'preco_medio', 'created_by', 'modified_by')
    list_display_links = ('id', 'ticker')
    search_fields = ('ticker',)
    list_per_page = 20
    
admin.site.register(BdrsConsolidadas, BdrConsolidada)

class CriptoConsolidada(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'valor', 'quantidade', 'dividendo', 'preco_medio', 'created_by', 'modified_by')
    list_display_links = ('id', 'ticker')
    search_fields = ('ticker',)
    list_per_page = 20
    
admin.site.register(CriptosConsolidadas, CriptoConsolidada)