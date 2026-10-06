from django.urls import path
from . import views

app_name = 'vitrine'

urlpatterns = [
    path('', views.index, name='index'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),
]
