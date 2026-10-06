from django.contrib import admin
from .models import DemandeEtude, PlanType


@admin.register(DemandeEtude)
class DemandeEtudeAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'type_projet', 'ville_terrain', 'statut', 'date_creation')
    list_filter = ('statut', 'type_projet')
    search_fields = ('nom_complet', 'telephone', 'email', 'ville_terrain')
    date_hierarchy = 'date_creation'


@admin.register(PlanType)
class PlanTypeAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_rendu', 'superficie', 'ordre')
    list_filter = ('type_rendu',)
    ordering = ('ordre',)
