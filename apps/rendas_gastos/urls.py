from django.urls import path
from apps.rendas_gastos.views import index, rendas, gastos

urlpatterns = [
    path('', index, name='index'),
    path('rendas', rendas, name='rendas'),
    path('gastos', gastos, name='gastos'),
]