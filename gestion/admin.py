from django.contrib import admin
from .models import Proprietaire, Bien, DemandeGestion


@admin.register(Proprietaire)
class ProprietaireAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'telephone', 'email')
    search_fields = ('nom_complet', 'telephone', 'email')


@admin.register(Bien)
class BienAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_bien', 'transaction', 'ville', 'prix', 'statut', 'proprietaire')
    list_filter = ('transaction', 'type_bien', 'statut', 'ville')
    search_fields = ('titre', 'ville', 'quartier')


@admin.register(DemandeGestion)
class DemandeGestionAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'objectif', 'type_bien', 'adresse_bien', 'statut', 'date_creation')
    list_filter = ('statut', 'objectif', 'type_bien')
    search_fields = ('nom_complet', 'telephone', 'adresse_bien')
    date_hierarchy = 'date_creation'
