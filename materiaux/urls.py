from django.urls import path
from . import views

app_name = 'materiaux'

urlpatterns = [
    path('', views.index, name='index'),
    path('materiaux/', views.materiaux, name='materiaux'),
    path('equipements/', views.equipements, name='equipements'),
    path('engins/', views.engins, name='engins'),
]
