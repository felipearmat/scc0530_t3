from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('mapa_arquivo/', views.APIMapaArquivo.as_view(), name='mapa_arquivo'),
    path('busca_mapa/', views.APIBuscaMapa.as_view(), name='busca_mapa'),
]
