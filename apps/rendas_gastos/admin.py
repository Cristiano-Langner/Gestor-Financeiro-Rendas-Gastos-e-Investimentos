from django.contrib import admin
from apps.rendas_gastos.models import Gastos, Rendas

class Gasto(admin.ModelAdmin):
    list_display = ('id', 'valor', 'data', 'metodo_pagamento', 'categoria', 'created_by', 'modified_by')
    list_display_links = ('id', 'valor')
    search_fields = ('categoria',)
    list_per_page = 20
    
admin.site.register(Gastos, Gasto)

class Renda(admin.ModelAdmin):
    list_display = ('id', 'valor', 'data', 'metodo_pagamento', 'categoria', 'created_by', 'modified_by')
    list_display_links = ('id', 'valor')
    search_fields = ('categoria',)
    list_per_page = 20
    
admin.site.register(Rendas, Renda)