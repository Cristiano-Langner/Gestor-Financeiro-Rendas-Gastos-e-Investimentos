from django.urls import path
from apps.investimentos.views import investimentos

urlpatterns = [
    path('investimentos', investimentos, name='investimentos'),
]