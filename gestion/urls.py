from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('', views.index, name='index'),
    path('acd/', views.acd, name='acd'),
    path('locative/', views.locative, name='locative'),
    path('louer/', views.louer, name='louer'),
    path('vendre/', views.vendre, name='vendre'),
    path('bien/<int:pk>/', views.detail_bien, name='detail_bien'),
]
