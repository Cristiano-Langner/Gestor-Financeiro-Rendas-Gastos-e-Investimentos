from apps.investimentos.views import delete_acao, delete_fii, delete_bdr, delete_cripto, delete_rendafixa, delete_div, delete_cv
from apps.investimentos.views import acoes, fiis, bdrs, criptos, rendafixa, consolidar_carteira, detalhes_ticker
from django.urls import path

urlpatterns = [
    path('fiis', fiis, name='fiis'),
    path('bdrs', bdrs, name='bdrs'),
    path('acoes', acoes, name='acoes'),
    path('criptos', criptos, name='criptos'),
    path('rendafixa', rendafixa, name='rendafixa'),
    path('delete_fii/<int:fii_id>/', delete_fii, name='delete_fii'),
    path('delete_bdr/<int:bdr_id>/', delete_bdr, name='delete_bdr'),
    path('delete_acao/<int:acao_id>/', delete_acao, name='delete_acao'),
    path('delete_cripto/<int:cripto_id>/', delete_cripto, name='delete_cripto'),
    path('consolidar_carteira/', consolidar_carteira, name='consolidar_carteira'),
    path('detalhes_ticker/<str:tipo_investimento>/<str:ticker>/', detalhes_ticker, name='detalhes_ticker'),
    path('delete_rendafixa/<int:rendafixa_id>/', delete_rendafixa, name='delete_rendafixa'),
    path('delete_cv/<str:tipo_investimento>/<str:ticker>/<int:cv_id>/', delete_cv, name='delete_cv'),
    path('delete_div/<str:tipo_investimento>/<str:ticker>/<int:div_id>/', delete_div, name='delete_div'),
]