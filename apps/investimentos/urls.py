from django.urls import path
from apps.investimentos.views import acoes, fiis, bdrs, criptos, rendasfixa
from apps.investimentos.views import delete_acao, delete_fii, delete_bdr, delete_cripto, delete_rendafixa

urlpatterns = [
    path('acoes', acoes, name='acoes'),
    path('fiis', fiis, name='fiis'),
    path('bdrs', bdrs, name='bdrs'),
    path('criptos', criptos, name='criptos'),
    path('rendasfixa', rendasfixa, name='rendasfixa'),
    path('delete_acao/<int:acao_id>/', delete_acao, name='delete_acao'),
    path('delete_fii/<int:fii_id>/', delete_fii, name='delete_fii'),
    path('delete_bdr/<int:bdr_id>/', delete_bdr, name='delete_bdr'),
    path('delete_cripto/<int:cripto_id>/', delete_cripto, name='delete_cripto'),
    path('delete_rendafixa/<int:rendafixa_id>/', delete_rendafixa, name='delete_rendafixa'),
]