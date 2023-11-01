from apps.usuarios.views import pagina_erro_404, pagina_erro_500
from django.urls import path, include
from django.contrib import admin
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.investimentos.urls')),
    path('', include('apps.rendas_gastos.urls')),
    path('', include('apps.usuarios.urls')),
]

urlpatterns += [
    re_path(r'^.*/$', pagina_erro_404),
    re_path(r'^.*/$', pagina_erro_500),
]