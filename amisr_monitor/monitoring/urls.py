from django.urls import path
from .views import home, descargar_csv

urlpatterns = [
    path('', home, name='home'),
    path('descargar/<str:anio>/<str:mes>/', descargar_csv, name='descargar_csv'),
]
