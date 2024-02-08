from django.urls import path
from . import views
urlpatterns = [
    path('evapotranspiracaoservice', views.getEvapotranspiracaoService),
]
    