from django.urls import path
from . import views
urlpatterns = [
    path('evapotranspiracao', views.getEvapotranpiracaoCSV),
    path('dadosevapotranspiracao', views.getEvapotranpiracao),
    path('dadosevapotranspiracaodb', views.getEvapotranpiracaoDB),
]
    