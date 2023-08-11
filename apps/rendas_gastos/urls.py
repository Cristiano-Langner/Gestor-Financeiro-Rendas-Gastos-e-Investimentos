from django.urls import path
from apps.rendas_gastos.views import index

urlpatterns = [
    path('', index, name='index'),
]