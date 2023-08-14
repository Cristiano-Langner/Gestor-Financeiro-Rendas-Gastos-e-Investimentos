from django.urls import path
from apps.rendas_gastos.views import index, rendas, gastos, delete_renda

urlpatterns = [
    path('', index, name='index'),
    path('rendas', rendas, name='rendas'),
    path('gastos', gastos, name='gastos'),
    path('delete_renda/<int:renda_id>/', delete_renda, name='delete_renda'),
]