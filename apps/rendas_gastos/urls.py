from apps.rendas_gastos.views import index, rendas, gastos, limpar_filtros, delete_renda_gasto
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('rendas', rendas, name='rendas'),
    path('gastos', gastos, name='gastos'),
    path('limpar_filtros/<str:pagina>/', limpar_filtros, name='limpar_filtros'),
    path('delete_renda_gasto/<str:tipo>/<int:obj_id>/', delete_renda_gasto, name='delete_renda_gasto'),
]