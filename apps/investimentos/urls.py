from apps.investimentos.views import acoes, fiis, bdrs, criptos, rendafixa, consolidar_carteira, detalhes_ticker
from apps.investimentos.views import delete_div, delete_cv, delete_investimento
from django.urls import path

urlpatterns = [
    path('fiis', fiis, name='fiis'),
    path('bdrs', bdrs, name='bdrs'),
    path('acoes', acoes, name='acoes'),
    path('criptos', criptos, name='criptos'),
    path('rendafixa', rendafixa, name='rendafixa'),
    path('delete_investimento/<str:tipo_investimento>/<int:invest_id>/', delete_investimento, name='delete_investimento'),
    path('consolidar_carteira/', consolidar_carteira, name='consolidar_carteira'),
    path('detalhes_ticker/<str:tipo_investimento>/<str:ticker>/', detalhes_ticker, name='detalhes_ticker'),
    path('delete_cv/<str:tipo_investimento>/<str:ticker>/<int:cv_id>/', delete_cv, name='delete_cv'),
    path('delete_div/<str:tipo_investimento>/<str:ticker>/<int:div_id>/', delete_div, name='delete_div'),
]