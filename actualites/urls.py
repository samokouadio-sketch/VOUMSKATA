from django.urls import path
from . import views

app_name = 'actualites'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.detail, name='detail'),
]
