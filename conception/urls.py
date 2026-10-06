from django.urls import path
from . import views

app_name = 'conception'

urlpatterns = [
    path('', views.index, name='index'),
    path('plans-3d/', views.plans_3d, name='plans_3d'),
    path('etude-conseil/', views.etude_conseil, name='etude_conseil'),
    path('devis/', views.devis, name='devis'),
]
