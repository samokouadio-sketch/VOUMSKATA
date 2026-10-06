from django.urls import path
from . import views

app_name = 'realisations'

urlpatterns = [
    path('', views.index, name='index'),
    path('methode/', views.methode, name='methode'),
    path('<slug:slug>/', views.detail, name='detail'),
]
