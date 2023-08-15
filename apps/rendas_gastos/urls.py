from django.urls import path
from apps.rendas_gastos.views import index, rendas, gastos, delete_renda, delete_gasto

urlpatterns = [
    path('', index, name='index'),
    path('rendas', rendas, name='rendas'),
    path('gastos', gastos, name='gastos'),
    path('delete_renda/<int:renda_id>/', delete_renda, name='delete_renda'),
    path('delete_gasto/<int:gasto_id>/', delete_gasto, name='delete_gasto'),
]